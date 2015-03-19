from postings_list_node import PostingsListNode
import math


class PostingsList:
    def __init__(self, lst=None):
        self.root = None
        self.last = None
        self.length = 0
        if lst is not None:
            for i in lst:
                self.append(i)

    def __getitem__(self, index):
        if index >= self.length:
            raise Exception("Invalid index %d, %d" % (index, self.length))
        else:
            node = self.root
            c = 0
            while c < index:
                node = node.next
                c += 1
            return node

    def __len__(self):
        return self.length

    def __getslice__(self, start, end):
        node = self[start]
        val = []
        val.append(node.val)
        while start < end:
            node = node.next
            start += 1
            val.append(node.val)
        return val

    def __iadd__(self, other):
        self.append(other)

    def __str__(self):
        return " ".join(str(k[1]) for k in enumerate(self.get_list()))

    def __repr__(self):
        return str(self.get_list())

    def append(self, value):
        if self.root is None:
            self.root = PostingsListNode(value)
            self.last = self.root
        else:
            node = PostingsListNode(value)
            self.last.appendNode(node)
            self.last = node
        self.length += 1

    def get_list(self):
        lst = []
        nd = self.root
        while nd is not None:
            lst.append(nd.val)
            nd = nd.next
        return lst

    def generate_pairs(self):
        """ A generator to generate pair of skip nodes to be linked. """
        init = 1
        target = init + math.floor(math.sqrt(len(self)))
        while init < len(self) and target < len(self):
            yield (init, target)
            init = target
            target = init + math.floor(math.sqrt(len(self)))

    def generate_skips(self):
        """ Link nodes using the info from generated pairs"""
        current = 1
        node = self.root
        for init, target in self.generate_pairs():
            while init > current:
                node = node.next
                current += 1
            target_node = node
            node.pointers = []
            while target > current:
                target_node = target_node.next
                current += 1
            node.pointers.append(target_node)
            node = target_node
