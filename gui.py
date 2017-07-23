import sys
import os
import curses
from jsonparser import JSONParser
import menu
import traceback
import menudispatcher


class WinManager:
    def __init__(self):
        self.windows = []
        # self.current = curses.initscr()
        self.current = None
        self.idx = 0
        self.issplit = False
        self.z_index = []

    def setsplit(self):
        self.issplit = True

    def unsetsplit(self):
        self.issplit = False

    def addwindow(self, window):
        self.windows.append(window)

    def listwindows(self):
        for window in self.windows:
            return self.windows

    def cyclewindows(self):
        # if self.current == self.windows[self.idx]:
        if self.idx < len(self.windows) - 1:
            self.idx += 1
        else:
            self.idx = 0
        self.current = self.windows[self.idx]

    def getcurrent(self):
        return self.current

    def getnext(self):
        if self.idx < len(self.windows) - 1:
            return self.windows[self.idx + 1]
        else:
            return self.windows[0]

    def setcurrent(self, current):
        self.current = current

    def addz(self, win):
        self.z_index.append(win)

    def popz(self):
        if self.z_index:
            self.z_index.pop()
        else:
            pass

    def getz(self):
        return self.z_index[-1]


class Win(object):
    winmanager = WinManager()

    def __init__(self, scr):
        super(Win, self).__init__()
        self.scr = scr
        self.scr.clear()
        self.list     = []
        self.maxy, self.maxx = self.scr.getmaxyx()
        self.row      = 0           # current row
        self.idx      = 0           # current sub
        self.page     = 0
        self.len      = 0
        self.y        = 0           # top border
        self.x        = 0           # left border
        self.isactive = False

    def getentry(self):
        if self.idx < len(self.list):
            return self.list[self.row]
        else:
            pass

    def setactive(self):
        self.active = True

    def setpassive(self):
        self.active = False

    def updscr(self):
        self.scr.clear()
        self.scr.box()

    def getscr(self):
        return self.scr

    def processdata(self, l):
        if isinstance(l, list):
            return l
        elif isinstance(l, dict):
            return self.dicttolist(l)

    def dicttolist(self, d):
        # Calculate length of the longest string in the keys of the dict
        maxlength = len(max(d.keys(), key=len))
        l = []
        for k, v in d.items():
            b = maxlength - len(str(k))
            desc = str(k) + b * " " + "         " + str(v)
            l.append(desc)
        return l

    def _addstr(self, y, x, string, attr=curses.A_NORMAL):
        self.scr.clear()
        self.scr.addstr(y, x, string, attr) # "+1" because of window border
        self.scr.refresh()
        # self.updscr()

    def addline(self, **kwargs):
        # y = kwargs.get('y', self.y + self.row)
        y = kwargs.get('y', self.y + self.row)
        x = kwargs.get('x', self.x)
        if self.idx < len(self.list):
            string = kwargs.get('string', self.list[self.idx])
            attr = kwargs.get('attr', curses.A_NORMAL)
            if isinstance(string, str):
                self.scr.addstr(y, x, string, attr)
            elif isinstance(string, list):
                self.scr.addstr(y, x, string[0][0], attr)
        else:
            pass


    def printsubs(self):
        downl = self.page * self.maxy
        upl = (self.page + 1) * self.maxy

        for i, sub in enumerate(self.list[downl:upl]):
            # if isinstance(sub, list):
            #     sub = sub[0]
            #     self.list[i] = sub
            self.addline(y=self.y + i, string=str(sub))

        self.addline(attr=curses.A_STANDOUT)
        self.scr.refresh()

    def lastrow(self):
        if self.maxy * (self.page+1) < self.len:
            return self.maxy - 1
        return self.len - self.page * self.maxy - 1

    def move(self, i):
        if i >= 0 and i <= self.lastrow():
            self.addline()
            self.setrow(i)
            self.addline(attr=curses.A_STANDOUT)
        elif i >= self.maxy:
            self.page += 1
            self.updscr()
            self.setrow(0)
            self.printsubs()
        elif i < 0 and self.page > 0:
            self.page -= 1
            self.updscr()
            self.setrow(self.maxy-1)
            self.printsubs()

    def setrow(self, n):
        self.row = n
        self.idx = self.page * self.maxy + self.row

    def updscr(self):
        self.scr.clear()

    def otherkey(self, c):
        pass

    def actions(self):
        while True:
            c = self.scr.getch()
            if c == ord('o'):
                pass
            elif c == ord('x'):
                root.end()
                root.scr.erase()
                root.doublewin.lw.erase()
                root.doublewin.rw.erase()
                curses.endwin()
            elif c in (ord('k'), curses.KEY_UP):
                self.move(self.row-1)
            elif c in (ord('j'), curses.KEY_DOWN):
                # Test
                current = self.getentry()
                # status_bar.display(str(current))
                status_bar.print_content(str(current))

                self.move(self.row+1)
            elif c in (ord('g'), curses.KEY_HOME, curses.KEY_PPAGE):
                self.move(0)
            elif c in (ord('G'), curses.KEY_END, curses.KEY_NPAGE):
                self.move(self.lastrow())
            elif c in (ord('r'), ord('R')):
                self.scr.refresh()
            else:
                self.otherkey(c)

    def render(self):
        content = []
        choice = self.getentry()
        content = menu.generatemenu(choice)
        if not content:
            if self.eval_choice(choice): # == True:
                pass
            else:
                content = menudispatcher.dispatch_leave(choice)
                # Debug
                from logger import log
                log("debug.log", "content = "+str(content))
        # subwin() also takes the optional parameters
        # "nlines" and "ncols" like so:
        # dwin = SubWin(self.scr.subwin(len(self.list)+2, int(self.maxx), 20, 0),
        #               self.printsubs, entry)
        if content:
            dwin = SubWin(self.scr.subwin(10, 0),
                          self.printsubs, content)
            # self.winmanager.addz(dwin.getscr())
            self.winmanager.addz(dwin)
            dwin.settitle(choice)
            dwin.len = len(content)
            dwin.printsubs()

            if dwin.list is []:
                dwin.scr.addstr(1, 1, 'Default text')
                # self.src.getch()
                dwin.end()
            else:
                dwin.printsubs()
                dwin.actions()

    def eval_choice(self, choice):
        if choice == "Progress bar":
            import time

            self.scr.clear()
            pb = ProgressBar()
            for i in pb.render(self.scr, range(15), "Computing:", 40):
                time.sleep(0.1)
        else:
            pass


class ProgressBar:
    def __init__(self):
        pass

    def sketch(self, it, prefix = "", size = 60):
        """
        Displays the progress bar on stdout. Not suitable for
        a curses environment
        """
        count = len(it)
        def _show(_i):
            x = int(size*_i/count)
            sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i,
                                                   count))
            sys.stdout.flush()

        _show(0)
        for i, item in enumerate(it):
            yield item
            _show(i+1)
        sys.stdout.write("\n")
        sys.stdout.flush()


    def render(self, win, it, prefix = "", size = 60):
        """
        Actually renders the progress bar in the specified curses window.
        """
        curses.curs_set(0) # Set cursor invisibley
        count = len(it)
        def _show(_i):
            x = int(size*_i/count)
            win.addstr("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
            win.refresh()
            curses.delay_output(9999)
            win.clear()

        _show(0)
        for i, item in enumerate(it):
            yield item
            _show(i+1)
        win.addstr("\n")
        win.refresh()
        curses.delay_output(9999)
        win.clear()
        curses.curs_set(1)

class Root(Win):
    def __init__(self, scr):
        super(Root, self).__init__(scr)
        self.scr      = scr
        self.list     = []
        self.maxy, self.maxx = self.scr.getmaxyx()
        self.scr.clear()
        self.row      = 0
        self.idx      = 0
        self.page     = 0
        self.len      = 0
        self.y        = 0
        self.x        = 0
        self.isactive = True
        self.winmanager.addz(self)

        self.llist = ["dog", "cat", "bee"]
        self.rlist = ["car", "train", "ship", "airplane"]
        self.doublewin = DoubleWin(self.llist, self.rlist, self.printsubs)

        # Init pwd
        if len(sys.argv)>1:
            dir = os.path.abspath(sys.argv[1])
        else:
            dir = os.getcwd()

        # Curses initialization
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(1)

    def get_maxy(self):
        return self.maxy

    def get_win(self):
        return self.scr

    def createlists1(self):
        data = urllib.urlopen("http://api.ihackernews.com/page")
        parser = JSONParser(data)
        d = parser.convert_to_python()
        length = len(d["items"])
        for i in range(length):
            self.llist.append(d["items"][i]["title"].encode("ascii", "xmlcharrefreplace"))
        data.close()

    def createlists(self):
        self.llist = ["blue", "red", "green", "yellow"]

    def updscr(self):
        self.scr.clear()
        status_bar.draw()

    def shell(self):
        curses.endwin()
        os.system("cd %s; %s"%(self.dir,shell))
        # os.system("cd ~")
        self.scr.keypad(1)

        # curses.nocbreak()
        # self.scr.keypad(0)
        # curses.echo()
        # curses.endwin()


    def otherkey(self, c):
        if c in (ord('f'), curses.KEY_ENTER, 10):
            root.setpassive()
            self.render()
        elif c == ord('h'):
            root.setpassive()
            self.printhelp()
        elif c in(ord('d'), ord('D')):
            # if self.winmanager.issplit == True:
            #     self.winmanager.unsetsplit()
            # else:
            #     self.winmanager.setsplit()
            if self.winmanager.issplit == False:
                self.winmanager.setsplit()

            if root.isactive:
                self.doublewin.drawDoubleWin()
                # self.winmanager.setsplit = True
                root.setpassive()
        elif c == ord('s'):
            curses.def_prog_mode()
            curses.reset_shell_mode()
            self.shell()

    # def render(self):
    #     content = []
    #     # content.append(self.getentry())
    #     choice = self.getentry()
    #     content = menu.generatemenu(choice)
    #     # for entry in c:
    #     #     content.append(entry)
    #     print "Content = ", content, 20*"-"
    #     # subwin() also takes the optional parameters
    #     # "nlines" and "ncols" like so:
    #     # dwin = SubWin(self.scr.subwin(len(self.list)+2, int(self.maxx), 20, 0),
    #     #               self.printsubs, entry)
    #     dwin = SubWin(self.scr.subwin(10, 0),
    #                   self.printsubs, content)
    #     dwin.settitle(choice)
    #     dwin.len = len(content)
    #     dwin.printsubs()

    #     if dwin.list is []:
    #         dwin.scr.addstr(1, 1, 'Default text')
    #         # self.src.getch()
    #         dwin.end()
    #     else:
    #         dwin.printsubs()
    #         dwin.actions()

    def printhelp(self):
        # Help page
        self.shortkeys = {
            "Page Up":           "Scroll up",
            "Page Down":         "Scroll down",
            "Home key":          "Scroll to the top",
            "End key ":          "Scroll to the bottom",
            }

        helppage = SubWin(self.scr.subwin(len(self.shortkeys)+2,
                        int(self.maxx), 0, 0),  self.printsubs, self.shortkeys)
        helppage.settitle("Help page")
        helppage.updscr()

        if helppage.list is []:
            helppage.scr.addstr(1, 1, 'No help available')
            # self.src.getch()
            helppage.end()
        else:
            helppage.printsubs()
            helppage.actions()

    # Deprecated (class base solution preferred)
    def draw_sb(self, sb_text):
        sb = SubWin(self.scr.subwin(len(self.sb_text)+2,
                                    int(self.maxx), int(self.maxy)-len(self.sb_text)-2,
                                    0), self.printsubs, self.sb_text, set_no_title=True)
        # sb.settitle("Something")
        sb.updscr(draw_box=False)
        sb.printsubs()
        # sb.actions()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        sb._addstr(0, 0, "foobar", attr=curses.color_pair(1))


    def end(self):
        curses.nocbreak()
        self.scr.keypad(0)
        curses.echo()
        curses.endwin()
        sys.exit()


class SubWin(Win):
    def __init__(self, scr, ppsubs, listt, set_no_title=False):
        super(SubWin, self).__init__(scr)
        self.scr   = scr
        self.list  = self.processdata(listt)
        self.maxy, self.maxx = self.scr.getmaxyx()
        self.maxx -= 1
        self.maxy -= 1
        self.scr.clear()
        self.row   = 0
        self.idx   = 0
        self.page  = 0
        self.len   = len(self.list)
        self.y     = 1
        self.x     = 1
        self.set_no_title = set_no_title
        self.title = "Default title"
        self.scr.erase()
        self.scr.box()
        self.set_no_title = set_no_title
        if not self.set_no_title:
            self.scr.addstr(0, 3, self.title)
        self.parent_printsubs = ppsubs
        self.scr.keypad(1)
        self.anchor = (self.y, self.x)

    def getscr(self):
        return self.scr

    def updscr(self, draw_box=True):
        self.scr.clear()
        if draw_box:
            self.scr.box()
        if not self.set_no_title:
            self.scr.addstr(0, 3, self.title)

    def settitle(self, title, set_title=True):
        if isinstance(title, str):
            if not self.set_no_title:
                self.title = title
            self.updscr()
        else:
            pass # TODO: Error handling

    def otherkey(self, c):
        # TODO: Remove/Improve
        if c in (ord('e'), curses.KEY_ENTER, 10):
            root.doublewin.rw.addstr(2,2, "Foooooooooooooooooooo")
            root.doublewin.rw.move(2, 2)
            self.render() # Try to render another submenu
        elif c in (ord('a'), ord('A')):
            self.src.addstr(2, 2, "Baaaaaaaaaaaaaaaaaaaaaaaaaaaaaar")
        if c == ord('q'):
            root.setactive()
            if self.winmanager.issplit:
                self.winmanager.unsetsplit()
            root.doublewin.setpassive()
            root.setactive()
            # Manage window order
            self.winmanager.popz()
            if self.winmanager.z_index:
                precessor = self.winmanager.getz()
                # precessor.refresh()
                precessor.updscr()
                precessor.printsubs()
                precessor.actions()
            else:
                self.scr.clear()
                self.scr.refresh()
                root.doublewin.end()
                root.updscr()
                root.printsubs()
                root.actions()
        elif c == ord('t'):
            root.doublewin.end()
            root.updscr()
            root.printsubs()
            root.actions()
            # if self.winmanager.issplit:
            #     self.winmanager.unsetsplit()
            #     root.doublewin.end()
        elif c == ord('i'):
            if self.winmanager.issplit:
                # current = self.winmanager.getcurrent()
                win = self.winmanager.getnext()
                self.winmanager.cyclewindows()
                win.printsubs()
                win.actions()
                # current = self.winmanager.getnext().getscr()
                # self.winmanager.cyclewindows()
                # self.scr = current
                # # current.move(2, 2)
                # current.refresh()

            # if self.winmanager.issplit:
            #     self.winmanager.unsetsplit()
            # elif self.winmanager.issplit == False:
            #     self.winmanager.setsplit()

    def end(self):
        self.scr.erase()
        self.parent_printsubs()


class DoubleWin(Win):
    def __init__(self, leftlist, rightlist, ppsubs, scr=curses.initscr()):
        super(DoubleWin, self).__init__(scr)
        self.list = []
        self.scr = scr
        self.leftlist = leftlist
        self.rightlist = rightlist
        self.length = max(len(self.leftlist), len(self.rightlist))
        self.maxy, self.maxx = self.scr.getmaxyx()
        # self.scr = SubWin(self.scr.subwin(self.len+2, int(self.maxx), 20, 0), self.printsubs, self.list)
        # self.maxy, self.maxx = super(DoubleWin, self).scr.getmaxyx()
        # super(DoubleWin, self).__init__(curses.newwin(0, 0, 0, 0))
        # self.maxy, self.maxx = Win.getscr().getmaxyx()

        # self.maxx -= 1
        # self.maxy -= 1
        # self.row   = 0
        # self.idx   = 0
        # self.page  = 0
        # self.y     = 1
        # self.x     = 1

        self.title = "Default title"
        self.anchor = (self.y, self.x)

        self.parent_printsubs = ppsubs

        self.list = self.leftlist
        # self.lw = curses.newwin(len(self.leftlist)+2, int(self.maxx/2), 20, 0)
        # self.list = self.rightlist
        # self.rw = curses.newwin(len(self.rightlist)+2, int(self.maxx/2), 20,
        #                         int(self.maxx/2))

        self.border = 2
        self.lw = curses.newwin(self.length + self.border, int(self.maxx/2), 0, 0)
        # self.list = self.rightlist
        # self.winmanager.addwindow(self.lw)

        self.rw = curses.newwin(self.length + self.border, int(self.maxx/2), 0,
                                int(self.maxx/2))
        # self.winmanager.addwindow(self.rw)

        self.list = self.leftlist
        self.leftwin = SubWin(self.lw, self.printsubs, self.leftlist)
        self.leftwin.settitle("Frontpage")
        self.winmanager.addwindow(self.leftwin)

        # self.list = self.rightlist
        self.rightwin = SubWin(self.rw, self.printsubs, self.rightlist)
        self.rightwin.settitle("Something")
        self.winmanager.addwindow(self.rightwin)

    def initleftwin(self):
        self.list = self.leftlist
        self.scr = self.lw
        self.leftwin.updscr

    def initrightwin(self):
        self.list = self.rightlist
        self.scr = self.rw
        self.rightwin.updscr

    def drawDoubleWin(self):
        self.leftwin.updscr()
        self.rightwin.updscr()
        self.list = self.leftlist
        self.rightwin.printsubs()
        # self.list = self.rightlist
        self.leftwin.printsubs()
        self.leftwin.actions()
        self.rightwin.actions()

    def updscr(self):
        # Left window
        self.lw.clear()
        self.lw.box()
        self.lw.addstr(0, 3, self.title)

        # Right window
        self.rw.clear()
        self.rw.box()
        self.rw.addstr(0, 3, self.title)

    def end1(self):
        # Left window
        if self.scr.getyx() < int(self.maxx/2):
            self.lw.erase()
        # Right window
        elif self.scr.getyx() >= int(self.maxx/2):
            self.rw.erase()
        self.parent_printsubs()

    def end(self):
        self.lw.clear()
        self.lw.refresh()

        self.rw.clear()
        self.rw.refresh()

        root.doublewin.scr.clear()
        root.doublewin.scr.refresh()

        # self.lw.clear()
        # self.lw.refresh()
        # self.rw.clear()
        # self.rw.refresh()

        # root.scr.refresh()

        # self.leftwin.scr.erase()
        # self.rightwin.scr.erase()


class StatusBar(Win):
    def __init__(self, scr, sb_text):
        super(StatusBar, self).__init__(scr)
        self.sb_text = sb_text
        self.parent_scr = scr
        self.scr = self.parent_scr.subwin(len(self.sb_text), int(self.maxx),
                                          int(self.maxy)-len(self.sb_text)-2, 0)
        self.maxy, self.maxx = self.scr.getmaxyx()
        # self.updscr()
        self.win = SubWin(self.scr, self.printsubs, self.sb_text, set_no_title=True)
        curses.start_color()
        self.color = curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)


    def get_scr(self):
        return self.scr

    def updscr(self, draw_box=True):
        self.scr.clear()
        if not draw_box: # TODO: Remove "not"
            self.scr.box()
        # if not self.set_no_title:
        #     self.scr.addstr(0, 3, self.title)

    def display(self, *args):
        self.scr.clear()
        # self.sb_text = []
        for arg in args:
            self.sb_text.append(str(arg))
        if len(self.sb_text) > 5:
            self.flush()
        if len(self.sb_text) > 0:
            self.scr.mvderwin(root.get_maxy()-len(self.sb_text)-1, 0)
            self.scr.resize(len(self.sb_text)+1, int(self.maxx))
        self.draw()

    def print_content(self, string):
        self.sb_text = []
        self.sb_text.append(str(string))
        self.scr.addstr(0, 0, self.sb_text[0], curses.color_pair(1))
        self.scr.refresh()

    def flush(self):
        self.sb_text = ["default"]
        self.scr.clear()

    def draw(self):
        self.updscr(draw_box=False)
        self.printsubs()
        attr = self.color

        t = ""
        for s in self.sb_text:
            t += str(s)+"\n"
        t.rstrip("\n")
        # self._addstr(0, 0, t, attr=curses.color_pair(1))
        self.scr.addstr(0, 0, t, curses.color_pair(1))


curses.def_shell_mode()
root = Root(curses.initscr())

# Add a status bar
content = ["something"]
status_bar = StatusBar(root.get_win(), content)
# status_bar.display("foo", "bar", "baz", "barfoo", "", "foobar")
status_bar.print_content("foo")



entries = menu.generatemenu("Menu")

for i, a in enumerate(entries):
    # root.list.append(str(i) + "  " + str(a))
    root.list.append(str(a))
    root.len += 1

try:
    if root.list:
        root.printsubs()
        root.actions()
except:
    # root.scr.erase()
    # root.end()
    curses.endwin()
    # traceback.print_tb(sys.exc_info()[2])
    exception_info = sys.exc_info()
    # print ''.join(traceback.format_list(traceback.extract_stack()))
    print ''.join(traceback.format_exception(*exception_info))

