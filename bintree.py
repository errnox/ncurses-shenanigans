_LEFT = 0
_RIGHT = 1
_VALUE = 2
_SORT_KEY = -1

class BinarySearchTree(object):
    def __init__(self, sort_key=None):
        self._root = [] # = empty node
        self._sort_key = sort_key
        self._len = 0 # keep track of how many items we contain.

# ------------------------------------------------------------------------------
# Public Methods
# ------------------------------------------------------------------------------


    def insert(self, value):
        # Get the sort key for this value.
        if self._sort_key is None:
            sort_key = value
        else:
            sort_key = self._sort_key(value)
        # Walk down the tree until an empty node is found
        node = self._root
        while node:
            if sort_key < node[_SORT_KEY]:
                node = node[_LEFT]
            else:
                node = node[_RIGHT]
        # Put the value in the empty node.
        if sort_key is value:
            node[:] = [[], [], value]
        else:
            node[:] = [[], [], value, sort_key]
        self._len += 1

    def minimum(self):
        return self._extreme_node(_LEFT)[_VALUE]

    def maximum(self):
        return self._extreme_node(_RIGHT)[_VALUE]

    def find(self, sort_key):
        return self._find(sort_key)[_VALUE]

    def pop_min(self):
        return self._pop_node(self._extreme_node(_LEFT))

    def pop_max(self):
        return self._pop_node(self._extreme_node(_RIGHT))

    def pop(self, sort_key):
        return self._pop_node(self._find(sort_key))

    def values(self, reverse=False):
        if reverse:
            return self._iter(_RIGHT, _LEFT)
        else:
            return self._iter(_LEFT, _RIGHT)
    __iter__ = values

    def __len__(self):
        return self._len

    def __nonzero__(self):
        return self._len>0

    def __repr__(self):
        return '<BST: (%s)>' % ', '.join('%r' % v for v in self)

    def __str__(self):
        return self.pprint()

    def pprint(self, max_depth=10, frame=True, show_key=True):
        t,m,b = self._pprint(self._root, max_depth, show_key)
        lines = t+[m]+b
        if frame:
            width = max(40, max(len(line) for line in lines))
            s = '+-'+'MIN'.rjust(width, '-')+'-+\n'
            s += ''.join('| %s |\n' % line.ljust(width) for line in lines)
            s += '+-'+'MAX'.rjust(width, '-')+'-+\n'
            return s
        else:
            return '\n'.join(lines)


# ------------------------------------------------------------------------------
# Private Helper Methods
# ------------------------------------------------------------------------------


    def _extreme_node(self, side):
        if not self._root:
            raise IndexError('Empty Binary Search Tree!')
        node = self._root
        # Walk down the specified side of the tree.
        while node[side]:
            node = node[side]
        return node

    def _find(self, sort_key):
        node = self._root
        while node:
            node_key = node[_SORT_KEY]
            if sort_key < node_key:
                node = node[_LEFT]
            elif sort_key > node_key:
                node = node[_RIGHT]
            else:
                return node
        raise KeyError("Key %r not found in BST" % sort_key)

    def _pop_node(self, node):
        value = node[_VALUE]
        if node[_LEFT]:
            if node[_RIGHT]:
                # This node has a left child and a right child; find
                # the node's successor, and replace the node's value
                # with its successor's value.  Then replace the
                # sucessor with its right child (the sucessor is
                # guaranteed not to have a left child).  Note: node
                # and successor may not be the same length (3 vs 4)
                # because of the key-equal-to-value optimization; so
                # we have to be a little careful here.
                successor = node[_RIGHT]
                while successor[_LEFT]: successor = successor[_LEFT]
                node[2:] = successor[2:]
                successor[:] = successor[_RIGHT]
            else:
                node[:] = node[_LEFT]
        else:
            if node[_RIGHT]:
                node[:] = node[_RIGHT]
            else:
                del node[:]
        self._len -= 1
        return value

    def _iter(self, pre, post):
        stack = []
        node = self._root
        while stack or node:
            if node: # descend
                stack.append(node)
                node = node[pre]
            else: # ascend
                node = stack.pop()
                yield node[_VALUE]
                node = node[post]

    def _pprint(self, node, max_depth, show_key, spacer=2):
        """
        Returns a (top_lines, mid_line, bot_lines) tuple,
        """
        if max_depth == 0:
            return ([], '- ...', [])
        elif not node:
            return ([], '- EMPTY', [])
        else:
            top_lines = []
            bot_lines = []
            mid_line = '-%r' % node[_VALUE]
            if len(node) > 3: mid_line += ' (key=%r)' % node[_SORT_KEY]
            if node[_LEFT]:
                t,m,b = self._pprint(node[_LEFT], max_depth-1,
                                     show_key, spacer)
                indent = ' '*(len(b)+spacer)
                top_lines += [indent+' '+line for line in t]
                top_lines.append(indent+'/'+m)
                top_lines += [' '*(len(b)-i+spacer-1)+'/'+' '*(i+1)+line
                              for (i, line) in enumerate(b)]
            if node[_RIGHT]:
                t,m,b = self._pprint(node[_RIGHT], max_depth-1,
                                     show_key, spacer)
                indent = ' '*(len(t)+spacer)
                bot_lines += [' '*(i+spacer)+'\\'+' '*(len(t)-i)+line
                              for (i, line) in enumerate(t)]
                bot_lines.append(indent+'\\'+m)
                bot_lines += [indent+' '+line for line in b]
            return (top_lines, mid_line, bot_lines)

