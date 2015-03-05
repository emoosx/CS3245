from skip_list_node import SkipListNode


class SkipList:

    def __init__(self):
        self.root = None
        self.last = None
        self.length = 0

    def __len__(self):
        return self.length

    def append(self, value):
        if self.root is None:
            self.root = SkipListNode(value)
            self.last = self.root
        else:
            new_node = SkipListNode(value)
            self.last.next = new_node
            self.last = new_node
        self.length += 1
