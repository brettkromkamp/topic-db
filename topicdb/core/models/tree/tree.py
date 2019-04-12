"""
Tree class. Part of the StoryTechnologies project.

July 02, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""
from typing import Dict, Optional, Generator

from topicdb.core.models.topic import Topic
from topicdb.core.models.tree.node import Node
from topicdb.core.models.tree.treeconstant import TreeConstant


class Tree:
    # Based on this implementation: http://www.quesucede.com/page/show/id/python-3-tree-implementation

    def __init__(self) -> None:
        self.__nodes: Dict = {}

    @property
    def nodes(self) -> Dict:
        return self.__nodes

    def add_node(self, identifier: str, parent: Optional[str] = None, topic: Optional[Topic] = None) -> Node:
        node = Node(identifier, parent, topic)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    def display(self, identifier: str, depth: int = 0) -> None:
        children = self[identifier].children
        if depth is TreeConstant.ROOT:
            print("{0}".format(identifier))
        else:
            print("\t" * depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            self.display(child, depth)  # Recursive call.

    def traverse(self, identifier: str, mode: TreeConstant = TreeConstant.DEPTH) -> Generator:
        # Python generator. Loosely based on an algorithm from 'Essential LISP'
        # by John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241.

        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode is TreeConstant.DEPTH:
                queue = expansion + queue[1:]  # Depth-first traversal.
            elif mode is TreeConstant.BREADTH:
                queue = queue[1:] + expansion  # Breadth-first traversal.

    def __getitem__(self, key: str) -> Node:
        return self.__nodes[key]

    def __setitem__(self, key: str, item: Node) -> None:
        self.__nodes[key] = item

    def __len__(self) -> int:
        return len(self.__nodes)
