from nose.tools import eq_
from skip_list import SkipList


class TestSkipList:

    def setup(self):
        self.skip_list = SkipList()

    def test_root(self):
        self.skip_list.append(3)
        eq_(self.skip_list.root.val(), 3)
        eq_(len(self.skip_list), 1)
        eq_(self.skip_list.root, self.skip_list.last)

    def test_print_node(self):
        self.skip_list.append(3)
        eq_(str(self.skip_list.root), str(3))


    def test_append(self):
        self.skip_list.append(1)
        self.skip_list.append(2)
        self.skip_list.append(3)
        self.skip_list.append(4)
        eq_(self.skip_list.root.val(), 1)
        eq_(len(self.skip_list), 4)
        eq_(self.skip_list.last.val(), 4)
