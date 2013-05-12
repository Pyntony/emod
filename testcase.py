#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
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
