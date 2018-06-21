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

# some discussion here - https://docs.oracle.com/middleware/1212/core/MAVEN/maven_version.htm#MAVEN8855
# more here - https://github.com/spring-projects/spring-build-gradle/wiki/Spring-project-versioning

        self.assertEqual("4.997", upgrade("4.0.1", "3.999, 2.998, 4.997"))
        self.assertEqual("4.997", upgrade("4.0.1", "4.997, 3.999, 2.998"))
        self.assertEqual("4.996", upgrade("4.0.1", "3.999, 4.996, 4.9.9"))
        self.assertEqual("4.9.1.1, 5.3.2", upgrade("4.0.1", "3.9.1, 4.9.1, 4.9.0, 4.9.1.1, 5.3.2"))
        self.assertEqual("4.0.9, 4.9.1.1, 6.3.2", upgrade("4.0.1", "3.9.1, 4.9.1, 4.0.9, 4.9.1.1, 5.2, 6.3.2")) # three upgrade choices - N, N.N and N.N.N based
        self.assertEqual("4.1-RC2", upgrade("4.0.1", "4.1-beta1, 4.1-RC1, 4.1-RC2"))
        self.assertEqual("4.1.0.RC2", upgrade("4.0.1", "4.1.0.beta1, 4.1.0.RC1, 4.1.0.RC2"))
        self.assertEqual("4.1", upgrade("4.0.1", "4.1-beta1, 4.1-RC1, 4.1"))
        self.assertEqual("4.1-beta2", upgrade("4.0.1", "4.1-beta1, 4.1-alpha1, 4.1-alpha2, 4.1-beta1"))
        self.assertEqual("4.1-beta", upgrade("4.0.1", "4.1-beta, 4.1-alpha1, 4.1-alpha2"))
        self.assertEqual("4.1-beta2", upgrade("4.0.1", "4.1-beta, 4.1-beta1, 4.1-beta2"))
        self.assertEqual("4.1-alpha2", upgrade("4.0.1", "4.1-alpha, 4.1-alpha1, 4.1-alpha2"))
        self.assertEqual("4.1-FINAL", upgrade("4.0.1", "4.1-alpha, 4.1-beta, 4.1-FINAL"))
        self.assertEqual("4.1-final", upgrade("4.0.1", "4.1-alpha, 4.1-beta, 4.1-final"))
        self.assertEqual("4.1-RELEASE", upgrade("4.0.1", "4.1-alpha, 4.1-beta, 4.1-RELEASE"))
        self.assertEqual("4.1-release", upgrade("4.0.1", "4.1-alpha, 4.1-beta, 4.1-release"))
        self.assertEqual("4.1.M1", upgrade("4.0.1", "4.1-alpha, 4.1-beta, 4.1.M1"))
        self.assertEqual("4.1", upgrade("4.0.1", "4.1-alpha, 4.1-beta, 4.1.M1, 4.1"))

if __name__ == '__main__':
    unittest.main()
