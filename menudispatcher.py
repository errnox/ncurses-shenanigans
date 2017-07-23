from logger import log
import commands
import os
from menu import generate_leave_list


def dispatch_leave(choice):
    for t in generate_leave_list():
        if t[0] == choice:
            command = t[1]
            # result = commands.getstatusoutput(command)
            f = os.popen(t[1])
            result = f.readlines()
            for i, line in enumerate(result):
                result[i] = line.rstrip("\n")
            # # Debug
            # from logger import log
            # log("debug.log", str(result))
            return result
        else:
            pass

