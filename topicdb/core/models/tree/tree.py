"""
Tree class. Part of the StoryTechnologies Builder project.

July 02, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.tree.node import Node
from topicdb.core.models.tree.treeconstant import TreeConstant


class Tree:
    # Based on this implementation: http://www.quesucede.com/page/show/id/python-3-tree-implementation

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None, topic=None):
        node = Node(identifier, parent, topic)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    def display(self, identifier, depth=0):
        children = self[identifier].children
        if depth is TreeConstant.root:
            print("{0}".format(identifier))
        else:
            print("\t"*depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            self.display(child, depth)  # Recursive call.

    def traverse(self, identifier, mode=TreeConstant.depth):
        # Python generator. Loosely based on an algorithm from 'Essential LISP' by John R. Anderson, Albert T. Corbett,
        # and Brian J. Reiser, page 239-241

        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode is TreeConstant.depth:
                queue = expansion + queue[1:]  # Depth-first traversal.
            elif mode is TreeConstant.breadth:
                queue = queue[1:] + expansion  # Width-first traversal.

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def __len__(self):
        return len(self.__nodes)
