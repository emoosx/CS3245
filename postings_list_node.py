class PostingsListNode:

    def __init__(self, value=None):
        self.val = int(value)
        self.pointers = None
        self.next = None

    def appendNode(self, node):
        if hasattr(node, "pointers"):
            self.next = node
        else:
            raise "invalid node"
