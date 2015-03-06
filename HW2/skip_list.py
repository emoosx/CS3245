from skip_list_node import SkipListNode
import math


class SkipList:

    def __init__(self):
        self.root = None
        self.last = None
        self.length = 0

    def __len__(self):
        return self.length

    def __iadd__(self, other):
        self.append(other)

    def append(self, value):
        if self.root is None:
            self.root = SkipListNode(value)
            self.last = self.root
        else:
            new_node = SkipListNode(value)
            self.last.next = new_node
            self.last = new_node
        self.length += 1

    def generate_skips(self):
        """A generators to generate pairs of nodes to be linked together as skip nodes"""
        start = 1
        length = len(self)
        skip_length = int(math.floor(math.sqrt(length)))
        target = start + skip_length
        while start < length and target < length:
            yield(start, target)
            start = target
            target = start + skip_length


    def create_skip_pointers(self):
        """ Create skip pointers with number paris generated from generate_skips"""
        current = 1
        node = self.root
        for a, b in self.generate_skips():
            while a > current:
                node = node.next
                current += 1
            target_node = node


            while b > current:
                target_node = target_node.next
                current += 1

            node.pointer = target_node
            node = target_node

        current = self.root
        while(current != self.last):
            current.print_node()
            current = current.next
            
