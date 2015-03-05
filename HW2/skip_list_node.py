class SkipListNode:

    def __init__(self, value, pointer=None, next=None):
        self.value = value;
        self.pointer = pointer;
        self.next = next;

    def __str__(self):
        return str(self.value)

    def val(self):
        return self.value
