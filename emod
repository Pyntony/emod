#!/usr/bin/env python3
#-*-coding:UTF-8-*-

"""emod is a utility for Gentoo Linux based systems which can edit flags of a
particular ebuild. This was originally developped to avoid forgetting a ">" when
running "echo app-dummy/example -qt gtk >> /etc/portage/package.use" for
instance and then overwrite the file. But this also enables to edit already
existing flags and sorts the lines in alphabetical order.

This tool was written with the following aims:
(1) The tool serves the user rather than the user serving the tool ;
(2) The tool is easy to maintain ;
(3) The tool is optimized.

If you think that any of these is not respected, feel free to let me know.
Please don't hesitate to improve it as well, but keep these aims in mind!

Note: As I didn't find any name for the following, I called:
    a rule: a line of a package.* file.
    a flag: an entitie that follows the atom in a rule.
            Namely: use flags, keywords, licenses, conf files and properties.

Note 2: For convenience, files are supposed to be well-written when emod is run.

"""

import os, re, sys
from shutil import rmtree

from argparse import ArgumentParser

__author__  = "Antoine Pinsard"
__email__   = "antoine.pinsard@member.fsf.org"
__version__ = "1.2"
__date__    = "2013-02-19"

class cilist(list):
    """Case insensitive list."""
    def __contains__(self, value):
        return value.upper() in [str(val).upper() for val in self]

# There are two possible structures for /etc/portage/package.* files
# It can either be a file containing all rules or a directory containing
# files named after the package category, containing themselves all rules
# for packages in the named category.
# As we don't want to force using a structure rather than the other (aim (1)),
# emod enables to choose the one to use with option --style.
# file_to_directory and directory_to_file functions enable to do the conversion
# if needed.

def file_to_directory(pkg_file):
    """Convert `pkg_file` from a file to a directory."""
    # Create the directory.
    # We first create a temporary directory not to erase the current file in
    # case of a crash or else.
    n = 0
    while os.path.exists("%s.bkp.%d" % (pkg_file, n)):
        n += 1
    tmp_dir = "%s.tmp.%d" % (pkg_file, n)
    try:
        os.mkdir(tmp_dir, 0o755)
    except OSError:
        sys.exit('Unable to create directory %s, are you root?' % tmp_dir)


    rules = read_rules(pkg_file)
    save_rules(tmp_dir, rules)

    # Remove the old file and rename the directory.
    try:
        os.remove(pkg_file)
        os.rename(tmp_dir, pkg_file)
    except OSError:
        sys.exit("Failed to replace the current file, are you root?")

def directory_to_file(pkg_dir):
    """Convert `pkg_dir` from a directory to a file."""
    # Create the temporary file.
    n = 0
    while os.path.exists("%s.bkp.%d" % (pkg_dir, n)):
        n += 1
    tmp_file = "%s.tmp.%d" % (pkg_dir, n)
    # Create the temporary file
    try:
        open(tmp_file, 'a').close()
    except IOError:
        sys.exit('Unable to create file %s, are you root?' % tmp_file)

    rules = read_rules(pkg_dir)
    save_rules(tmp_file, rules)

    # Remove the old directory and rename the file.
    try:
        rmtree(pkg_dir)
        os.rename(tmp_file, pkg_dir)
    except OSError:
        sys.exit("Failed to replace the current directory, are you root?")

def read_rules(pkg_file):
    """Read the rules of a package file depending on weather it is a file or directory."""
    if not os.path.exists(pkg_file):
        raise IOError('Cannot find %s' % pkg_file)

    # the rules are taken as is if working with a file.
    if os.path.isfile(pkg_file):
        with open(pkg_file, 'r', encoding='utf-8') as f:
            return f.readlines()

    # directories go by another layout with seperate files for categories
    # with each category file containing rules for atoms that fall into
    # that category
    if os.path.isdir(pkg_file):
        rules = []
        for category in os.listdir(pkg_file):
            with open(os.path.join(pkg_file, category), 'r') as f:
                rules += f.readlines()
        return rules

def save_rules(pkg_file, rules):
    """Save rules depending on weather it is a file or directory."""

    # Save according to the directory format if working with directories.
    if os.path.isdir(pkg_file):
        # seperate categories and atoms, then build a dictionary in the
        # {category:"category/atom\ncategory/atom2\n"} format for writing
        categories = {}
        for rule in rules:
            category, atom = rule.split('/')
            if category in categories:
               categories[category] += '/'.join((category,atom))
            else:
               categories[category] = '/'.join((category,atom))
        for category in categories:
            with open(os.path.join(pkg_file, category), 'w', encoding='utf-8') as f:
                f.write(categories[category])


    # Save normaly if working with a file.
    elif os.path.isfile(pkg_file):
        with open(pkg_file, 'w', encoding='utf-8') as f:
            f.write(''.join(rules))

PKG_TYPES = cilist(['accept_keywords', 'env', 'keywords', 'license', 'mask',
    'properties', 'unmask', 'use'])

PKG_STYLES = cilist(['default', 'directory', 'file'])
"""Available options for the --style option.

Read a few lines earlier to get more detail.

default:
    Will use the existing structure. If the package.* file doesn't exist yet,
    the default behavior will be --style=directory.
directory:
    Will use the directory structure.
file:
    Will use the file structure.

"""

# Parse arguments
parser = ArgumentParser(description="Ease your /etc/portage/package.* edition.")
parser.add_argument('atom', type=str, help="[<|>][=]ebuild")
parser.add_argument('--enable', '-e', type=str, nargs='+', metavar='flag',
    help="A list of flags to enable for the specified atom.")
parser.add_argument('--disable', '-d', type=str, nargs='+', metavar='flag',
    help="A list of flags to disable for the specified atom.")
parser.add_argument('--prune', '-p', action='store_true',
    help="Remove the custom rule of the specified atom.")
parser.add_argument('--type', '-t', type=str, default="use", choices=PKG_TYPES,
    help="Specify the type of rule (default is use).")
parser.add_argument('--style', type=str, default="default", choices=PKG_STYLES,
    help="Enable to force working with directory or file.")
parser.add_argument('--pkg-file', type=str, dest='pkg_file', metavar='file',
    default='/etc/portage/package',
    help='Specify a package file/directory (for testing/debugging)')
args = parser.parse_args()

category  = re.sub('[<=>]', '', args.atom.split('/')[0])
pkg_style = args.style.lower()

# Detect the package type if the full path is given ex (/etc/portage/package.use)
extension = os.path.splitext(args.pkg_file)[-1][1:] # grab the extension
if extension in PKG_TYPES:
    pkg_type = extension
    PKG_FILE = args.pkg_file
else:
    pkg_type  = args.type.lower()
    PKG_FILE = '.'.join((args.pkg_file, pkg_type))

# First determine if PKG_FILE exists and whether it is a file or a
# directory.
cur_pkg_style = 'default'
if os.path.exists(PKG_FILE):
    if os.path.isdir(PKG_FILE):
        cur_pkg_style = 'directory'
    else:
        cur_pkg_style = 'file'

# Determine if it needs a conversion.
if cur_pkg_style == 'directory' and pkg_style == 'file':
    directory_to_file(PKG_FILE)
elif cur_pkg_style == 'file' and pkg_style == 'directory':
    file_to_directory(PKG_FILE)
elif pkg_style == 'default':
    if cur_pkg_style == 'file':
        pkg_style = 'file'
    else:
        pkg_style = 'directory'

# Switch to the right file if PKG_FILE is a directory
if pkg_style == 'directory':
    if not os.path.exists(PKG_FILE):
        try:
            os.mkdir(PKG_FILE, mode=0o755)
        except OSError:
            sys.exit("Unable to create directory %s, are you root?" % PKG_FILE)
        PKG_FILE = os.path.join(PKG_FILE, category)

rules = read_rules(PKG_FILE)

if pkg_type in ['mask', 'unmask']:
    # Handle particular case of package.(un)mask that do not accept flags.
    if args.prune:
        try:
            rules.remove(args.atom)
        except ValueError:
            sys.exit("%s is not %sed." % (args.atom, pkg_type))
    else:
        if args.atom in rules:
            sys.exit("%s is already %sed." % (args.atom, pkg_type))
        else:
            rules.append(args.atom)
            rules.sort()
else:
    # Retrieve the current flags if the rule exist.
    flags = []
    for rule in rules:
        if rule.startswith(args.atom + " "):
            sys.stdout.write("Old rule: " + rule)
            flags = rule.split()[1:]
            rules.remove(rule) # We remove the rule to update it.
            break
    if not flags:
        print("No argument currently defined for %s." % args.atom)

    # 1.Prune flags
    if args.prune:
        flags = []

    # 2.Disable flags
    if args.disable:
        for flag in args.disable:
            try:
                flags.remove(flag)
            except ValueError:
                print("warning: %s is not enabled!" % flag)

    # 3.Enable flags
    if args.enable:
        for flag in args.enable:
            if flag in flags:
                print("warning: %s is already enabled!" % flag)
            else:
                flags.append(flag)

    # Update the rule
    if flags:
        flags.sort()
        rule = args.atom + ' ' + ' '.join(flags) + '\n'
        sys.stdout.write("New rule: " + rule)
        rules.append(rule)
        rules.sort()

# Save changes
try:
    save_rules(PKG_FILE, rules)
except IOError:
    sys.exit("Unable to write in %s, are you root?" % PKG_FILE)
