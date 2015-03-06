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


    def test_append(self):
        self.skip_list.append(1)
        self.skip_list.append(2)
        self.skip_list.append(3)
        self.skip_list.append(4)
        eq_(self.skip_list.root.val(), 1)
        eq_(len(self.skip_list), 4)
        eq_(self.skip_list.last.val(), 4)


    def test_generate_skips(self):
        for i in range(30):
            self.skip_list.append(i)
        skip_pairs = [(a, b) for (a, b) in self.skip_list.generate_skips()]
        eq_(skip_pairs, [(1, 6), (6, 11), (11, 16), (16, 21), (21, 26)])


    # def test_create_skip_pointers(self):
    #     for i in range(30):
    #         self.skip_list.append(i)
    #     self.skip_list.create_skip_pointers()
    #     eq_(1, 2)
            
        
        
