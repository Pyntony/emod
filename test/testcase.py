#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import sys
import os

# Assuming that the test directory is inside the emod directory, this will allow
# emod to be imported if the script is run either from the emod directory
# (test/testcase.py) or from the testing directory.
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

class read_rules(unittest.TestCase):
    out = ['!!<sys-apps/portage-2.1.4_rc1\n',
    # This is the output that read_rules() should give for both file and directory
    # structures
           '!=net-fs/samba-2*\n',
           '!app-text/dos2unix\n',
           '*/*\n',
           '*/*::gentoo\n',
           '*/zlib\n',
           '<=media-libs/libgd-1.6\n',
           '<media-libs/libgd-1.6\n',
           '=*/*-*9999*\n',
           '=*/*-*_beta*\n',
           '=dev-libs/glib-2*\n',
           '=media-libs/libgd-1.6\n',
           '=x11-libs/qt-3.3*:3\n',
           '>=media-libs/libgd-1.6\n',
           '>=x11-libs/qt-3.3.8:3\n',
           '>media-libs/libgd-1.6\n',
           'dev-lang/perl:*\n',
           'dev-lang/perl:0/5.12\n',
           'dev-lang/perl:0/5.12=\n',
           'dev-lang/perl:0=\n',
           'dev-lang/perl:=\n',
           'dev-libs/glib:*\n',
           'dev-libs/glib:2/2.30\n',
           'dev-libs/glib:2/2.30=\n',
           'dev-libs/glib:2=\n',
           'dev-libs/glib:=\n',
           'dev-libs/icu:*\n',
           'dev-libs/icu:0/0\n',
           'dev-libs/icu:0/0=\n',
           'dev-libs/icu:0/49\n',
           'dev-libs/icu:0/49=\n',
           'dev-libs/icu:0=\n',
           'dev-libs/icu:=\n',
           'kde-base/kdelibs::kde-testing\n',
           'net-*/*\n',
           'net-im/empathy::gnome\n',
           'net-misc/dhcp\n',
           'net-misc/dhcp-3.0_p2\n',
           'sys-apps/*\n',
           'sys-apps/sed\n',
           'sys-apps/sed-4.0.5\n',
           'sys-apps/sed::gentoo\n',
           'sys-libs/zlib\n',
           'sys-libs/zlib-1.1.4-r1\n',
           'x11-libs/qt:3\n',
           '~net-libs/libnet-1.0.2a\n',
           '~x11-libs/qt-3.3.8:3\n']

    maxDiff = None # disable line limit on diffs

    def test_read_rules_expr_file(self):
           """read_rules must return valid output"""
           infile = 'package.expressions.file'
           self.assertEqual(emod.read_rules(infile), self.out)

    def test_read_rules_expr_dir(self):
        """read_rules must return valid output for directory."""
        infile = 'package.expressions.dir'
        self.assertEqual(emod.read_rules(infile), self.out)

class save_rules(unittest.TestCase):
    rules = ['!!<sys-apps/portage-2.1.4_rc1\n',
            # rules to be saved by the test methods
           '!=net-fs/samba-2*\n',
           '!app-text/dos2unix\n',
           '*/*\n',
           '*/*::gentoo\n',
           '*/zlib\n',
           '<=media-libs/libgd-1.6\n',
           '<media-libs/libgd-1.6\n',
           '=*/*-*9999*\n',
           '=*/*-*_beta*\n',
           '=dev-libs/glib-2*\n',
           'dev-libs/glib:2/2.30=\n',
           '=media-libs/libgd-1.6\n',
           '=x11-libs/qt-3.3*:3\n',
           'dev-libs/icu:0/49\n',
           'dev-libs/icu:0/49=\n',
           'dev-libs/icu:0=\n',
           '>=media-libs/libgd-1.6\n',
           '>=x11-libs/qt-3.3.8:3\n',
           '>media-libs/libgd-1.6\n',
           'dev-lang/perl:*\n',
           'dev-lang/perl:0/5.12\n',
           'dev-lang/perl:0/5.12=\n',
           'dev-libs/glib:*\n',
           'dev-libs/glib:2/2.30\n',
           'dev-lang/perl:=\n',
           'dev-lang/perl:0=\n',
           'dev-libs/icu:*\n',
           'dev-libs/icu:=\n',
           'kde-base/kdelibs::kde-testing\n',
           'net-*/*\n',
           'net-im/empathy::gnome\n',
           'dev-libs/glib:2=\n',
           'dev-libs/glib:=\n',
           'dev-libs/icu:0/0\n',
           'dev-libs/icu:0/0=\n',
           'net-misc/dhcp-3.0_p2\n',
           'sys-apps/*\n',
           'sys-apps/sed\n',
           'sys-apps/sed-4.0.5\n',
           'net-misc/dhcp\n',
           'sys-apps/sed::gentoo\n',
           'sys-libs/zlib\n',
           'sys-libs/zlib-1.1.4-r1\n',
           'x11-libs/qt:3\n',
           '~net-libs/libnet-1.0.2a\n',
           '~x11-libs/qt-3.3.8:3\n']

    sorted_rules = sorted(rules)

    maxDiff =  None # Disable diff limit

    def test_save_rules_file(self):
        """save_rules should save rules in a file correctly."""
        outfile = 'package.expressions.file.tmp'
        # Create the file so save_rules() can detect the structure type.
        open(outfile, 'a').close()
        emod.save_rules(outfile, self.rules)
        testfile = open(outfile, 'r')

        try:
            self.assertEqual(testfile.readlines(), self.sorted_rules)
        finally:
            # Clean up
            testfile.close()
            os.remove(outfile)

if __name__ == '__main__':
    unittest.main()
