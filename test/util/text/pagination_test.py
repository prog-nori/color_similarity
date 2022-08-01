import os
import unittest
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))
# from ....src.util.text.pagination
from src.util.text.pagination import Pagination, Page

class PaginationTest(unittest.TestCase):
    def test_1(self):
        """
        1 [2] 3 4 5 ... 15
        """
        return

    def test_2(self):
        """
        1 ... 8 [9] 10 ... 15
        """
        return

    def test_3(self):
        """
        1 ... 11 12 [13] 14 15
        """
        return

    def test_4(self):
        """
        1 [2] 3 ... 15
        """
        return

    def test_5(self):
        """
        1 2 3 4 ... 15
        """
        return
    
    def test_6(self):
        """
        [1] 2 ... 15
        """
        return

    def test_7(self):
        """
        1 ... 14 [15]
        """
        return


if __name__ == '__main__':
    print('start')
    # test()
    unittest.main()
