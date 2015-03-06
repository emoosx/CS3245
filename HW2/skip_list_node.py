class SkipListNode:

    def __init__(self, value, pointer=None, next=None):
        self.value = value;
        self.pointer = pointer;
        self.next = next;

    def __repr__(self):
        return str(self.value) + " -P> " + str(self.pointer)

    def __str__(self):
        return str(self.value)

    def val(self):
        return self.value

    def print_node(self):
        print "Val = %s\tNext = %s\tPointer = %s" % (str(self), str(self.next), str(self.pointer))
