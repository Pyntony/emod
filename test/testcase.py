#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import sys
import os.path

# Assuming that the test directory is inside the emod directory, this will allow
# emod to be imported if the script is run either from the emod directory
# (testing/testcase.py) or from the testing directory.
emod_path = os.path.sep.join(sys.path[0].split(os.path.sep)[:-1])
sys.path.append(emod_path)
import emod

class cilist(unittest.TestCase):
    def test_cilist_membership(self):
        """cilist should not consider case for item membership tests."""

        input = emod.cilist(['foo', 'BAR', 'fooBAR'])
        output = ['FOO', 'bar', 'foobar', 'foo', 'BAR', 'FoO', 'FOOBAR']

        for item in output:
            self.assertTrue(item in input)

if __name__ == '__main__':
    unittest.main()
