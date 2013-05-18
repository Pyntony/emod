#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest, os, re, sys
from shutil import rmtree, copy, copytree

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

    data_dir = "Data/"
    pkg_file = "package.expressions.file"
    pkg_dir = "package.expressions.dir"

    maxDiff = None # disable line limit on diffs

    def setUp(self):
        """Copy over fresh test files."""
        pkg_file = self.pkg_file
        pkg_dir = self.pkg_dir
        data_dir = self.data_dir

        copy(data_dir+pkg_file, pkg_file)
        copytree(data_dir+pkg_dir, pkg_dir)

    def tearDown(self):
        """Clean up after each test."""
        rmtree(self.pkg_dir)
        os.remove(self.pkg_file)

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

    def test_save_rules_dir(self):
        """save_rules should save rules in a directory correctly."""
        outfile = 'package.expressions.dir.tmp'

        try:
            # Create the directory.
            os.mkdir(outfile, 0o755)

            emod.save_rules(outfile, self.rules)
            # Using read_rules temporarly untill i can figure out a better way
            # to run this test.
            self.assertEqual(emod.read_rules(outfile), self.sorted_rules)

            # Make sure no filename starts with the symbols !~<>=
            for file in os.listdir(outfile):
                self.assertFalse(re.search('^[!~<>=]+.*$', file))
        finally:
            # Cleanning up
            rmtree(outfile)

class file_to_directory(unittest.TestCase):
    """Unittest for the file_to_directory function."""
    pkg_file = "package.use"
    data_dir = "Data/"

    def tearDown(self):
        """Clean up the created files after running tests."""
        pkg_file = self.pkg_file

        if os.path.exists(pkg_file):
            try:
                os.remove(pkg_file)
            except OSError:
                rmtree(pkg_file)

        try:
            rmtree(pkg_file)
        except OSError:
            pass

    def setUp(self):
        """Copy over a fresh data file."""
        data_dir = self.data_dir
        pkg_file = self.pkg_file

        copy(data_dir+pkg_file, self.pkg_file)

    def test_file_to_directory_creation(self):
        """file_to_directory should create a new file."""

        emod.file_to_directory(self.pkg_file)
        self.assertTrue(os.path.exists(self.pkg_file))

    def test_file_to_directory_type(self):
        """file_to_directory must create a directory."""

        emod.file_to_directory(self.pkg_file)
        self.assertTrue(os.path.isdir(self.pkg_file))

class directory_to_file(unittest.TestCase):
    """Unittest for the directory_to_file function."""
    pkg_dir = "package.use.dir"
    data_dir = "Data/"

    def setUp(self):
        """Set up by copying over a fresh test directory."""
        pkg_dir = self.pkg_dir
        data_dir = self.data_dir

        copytree(data_dir+pkg_dir, pkg_dir)

    def tearDown(self):
        """Clean up after test method."""
        try:
            os.remove(self.pkg_dir)
        except OSError:
            rmtree(self.pkg_dir)

    def test_creation(self):
        """directory_to_file must create a file."""
        emod.directory_to_file(self.pkg_dir)
        self.assertTrue(os.path.exists(self.pkg_dir))

    def test_type(self):
        """directory_to_file must create a file, not a directory."""
        emod.directory_to_file(self.pkg_dir)
        self.assertTrue(os.path.isfile(self.pkg_dir))

if __name__ == '__main__':
    unittest.main()
