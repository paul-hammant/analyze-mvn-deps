# coding=utf-8
import sys
import unittest
from unittest import TestCase
from importlib import reload


from mock import Mock, call
from mockextras import stub
import os

sys.path = [os.path.abspath(os.path.join('..', os.pardir))] + sys.path


def upgrade(current, allVersions):
    return current + ".123"# incorrect
    pass


class TestVersions(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestVersions, self).__init__(methodName)
        reload(sys)
        # sys.setdefaultencoding('utf8')

    def test_these(self):

        self.assertEqual("4.997", upgrade("4.0.1", "3.999, 2.998, 4.997"))
        self.assertEqual("4.997", upgrade("4.0.1", "4.997, 3.999, 2.998"))
        self.assertEqual("4.996", upgrade("4.0.1", "3.999, 4.996, 4.9.9"))
        self.assertEqual("4.9.1.1, 5.3.2", upgrade("4.0.1", "3.9.1, 4.9.1, 4.9.0, 4.9.1.1, 5.3.2"))


if __name__ == '__main__':
    unittest.main()
