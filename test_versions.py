# coding=utf-8
import sys
import unittest
from unittest import TestCase
from importlib import reload

import os
from testing_proxy import recommended_version_upgrades

sys.path = [os.path.abspath(os.path.join('..', os.pardir))] + sys.path


class TestVersions(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestVersions, self).__init__(methodName)
        reload(sys)
        # sys.setdefaultencoding('utf8')

    # some discussion here - https://docs.oracle.com/middleware/1212/core/MAVEN/maven_version.htm#MAVEN8855
    # more here - https://github.com/spring-projects/spring-build-gradle/wiki/Spring-project-versioning

    def test_01(self):

        self.assertEqual("4.997", recommended_version_upgrades("4.0.1", ["3.999", "2.998", "4.997"]))

    def test_02(self):

        self.assertEqual("4.997", recommended_version_upgrades("4.0.1", ["4.997", "3.999", "2.998"]))

    def test_03(self):

        self.assertEqual("4.996", recommended_version_upgrades("4.0.1", ["3.999", "4.996", "4.9.9"]))

    def test_04(self):

        self.assertEqual("5.3.2, 4.9.1.1", recommended_version_upgrades("4.0.1", ["3.9.1", "4.9.1", "4.9.0", "4.9.1.1", "5.3.2"]))

    def test_05(self):

        self.assertEqual("6.3.2, 4.9.1.1, 4.0.9", recommended_version_upgrades("4.0.1", ["3.9.1", "4.9.1", "4.0.9", "4.9.1.1", "5.2", "6.3.2"])) # three upgrade choices - N, N.N and N.N.N based

    def test_06(self):

        self.assertEqual("4.1-RC2", recommended_version_upgrades("4.0.1", ["4.1-beta1", "4.1-RC1", "4.1-RC2"]))

    def test_07(self):

        self.assertEqual("4.1.0.RC2", recommended_version_upgrades("4.0.1", ["4.1.0.beta1", "4.1.0.RC1", "4.1.0.RC2"]))

    def test_08(self):

        self.assertEqual("4.1", recommended_version_upgrades("4.0.1", ["4.1-beta1", "4.1-RC1", "4.1"]))

    def test_09(self):

        self.assertEqual("4.1-beta2", recommended_version_upgrades("4.0.1", ["4.1-beta1", "4.1-alpha1", "4.1-alpha2", "4.1-beta2"]))

    def test_10(self):

        self.assertEqual("4.1-beta", recommended_version_upgrades("4.0.1", ["4.1-beta", "4.1-alpha1", "4.1-alpha2"]))

    def test_11(self):

        self.assertEqual("4.1-beta2", recommended_version_upgrades("4.0.1", ["4.1-beta", "4.1-beta1", "4.1-beta2"]))

    def test_12(self):

        self.assertEqual("4.1-alpha2", recommended_version_upgrades("4.0.1", ["4.1-alpha", "4.1-alpha1", "4.1-alpha2"]))

    def test_13(self):

        self.assertEqual("4.1-FINAL", recommended_version_upgrades("4.0.1", ["4.1-alpha", "4.1-beta", "4.1-FINAL"]))

    def test_14(self):

        self.assertEqual("4.1-final", recommended_version_upgrades("4.0.1", ["4.1-alpha", "4.1-beta", "4.1-final"]))

    def test_15(self):

        self.assertEqual("4.1-RELEASE", recommended_version_upgrades("4.0.1", ["4.1-alpha", "4.1-beta", "4.1-RELEASE"]))

    def test_16(self):

        self.assertEqual("4.1-release", recommended_version_upgrades("4.0.1", ["4.1-alpha", "4.1-beta", "4.1-release"]))

    def test_17(self):

        self.assertEqual("4.1-M1", recommended_version_upgrades("4.0.1", ["4.1-alpha", "4.1-beta", "4.1-M1"]))

    def test_18(self):

        self.assertEqual("4.1", recommended_version_upgrades("4.0.1", ["4.1-alpha", "4.1-beta", "4.1-M1", "4.1"]))

    def test_19(self):

        self.assertEqual("4.1", recommended_version_upgrades("4.0.1", ["4.1alpha", "4.1beta", "4.1M1", "4.1"]))

    def test_20(self):

        self.assertEqual("", recommended_version_upgrades("4.1", ["4.1alpha", "4.1beta", "4.1M1", "4.1"]))

    def test_21(self):

        self.assertEqual("", recommended_version_upgrades("4.12", ['4.0', '4.1', '4.10', '4.11', '4.11-beta-1', '4.12', '4.12-beta-1', '4.12-beta-2', '4.12-beta-3', '4.2', '4.3', '4.3.1', '4.4',
                                                                   '4.5', '4.6', '4.7', '4.8', '4.8.1', '4.8.2', '4.9']))


if __name__ == '__main__':
    unittest.main()
