#!/usr/bin/env python
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
from codecs import open

from argparse import ArgumentParser, REMAINDER

__version__ = '1.3.0'

class cilist(list):
    """Case insensitive list."""
    def __contains__(self, value):
        return value.upper() in [str(val).upper() for val in self]

class Package(object):
    """portage package file."""
    pkg_types = cilist(['accept_keywords', 'env', 'keywords', 'license',
        'mask', 'properties', 'unmask', 'use'])

    def __init__(self, path, type=None):
        if type == None or not type in self.pkg_types:
            extension = os.path.splitext(path)[-1][1:] # grab the extension
            if extension in self.pkg_types:
                self.type = extension
                self.path = path
            else:
                self.type = 'use'
                self.path = path
        else:
            self.type = type
            self.path = '.'.join((path, type))

        # Raise error if the file does not exist
        if not os.path.exists(self.path):
            raise OSError('File %s not found!' % self.path)

        # Detect package style
        if os.path.isdir(self.path):
            self.style = 'directory'
        elif os.path.isfile(self.path):
            self.style = 'file'
        else:
            raise TypeError('Unknown file type for %s' % path)

        self.rules = None # None means that we have not read the rules yet.

    def read_rules(self):
        """Read the rules from `pkg_file`."""
        pkg_file = self.path
        if not os.path.exists(pkg_file):
            raise IOError('Cannot find %s' % pkg_file)

        # the rules are taken as is if working with a file.
        if self.style == 'file':
            with open(pkg_file, 'r', encoding='utf-8') as f:
                rules = []
                # filter empty lines and comments
                for line in f.readlines():
                    if not line.isspace() and not line.startswith("#"):
                        rules.append(line)

        # directories go by another layout with seperate files for categories
        # with each category file containing atoms for ebuilds that fall into
        # that category
        elif self.style == 'directory':
            rules = []
            for category in os.listdir(pkg_file):
                with open(os.path.join(pkg_file, category), 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                        if not line.isspace() and not line.startswith("#"):
                            rules.append(line)

        self.rules = sorted(rules)
        return self.rules

    def save_rules(self):
        """Save the `rules` to `pkg_file`."""

        rules = sorted(self.rules)
        pkg_file = self.path
        # Save according to the directory format if working with directories.
        if self.style == 'directory':
            if not os.path.exists(pkg_file):
                os.mkdir(pkg_file)

            # seperate categories and ebuilds, then build a dictionary in the
            # {category:"category/ebuild\ncategory/ebuild2\n"} format for writing
            categories = {}
            for rule in rules:
                category, ebuild = rule.split('/', 1)
                category = re.sub('[!~<>=]', '', category)
                if category in categories:
                   categories[category] += rule
                else:
                   categories[category] = rule
            for category in categories:
                category_file = os.path.join(pkg_file, category)
                with open(category_file, 'w', encoding='utf-8') as f:
                    f.write(categories[category])

        # Save normaly if working with a file.
        elif self.style == 'file':
            with open(pkg_file, 'w', encoding='utf-8') as f:
                f.write(''.join(sorted(rules)))

    def convert(self):
        """Convert the package style."""

        # an empty dict will evaluate as False, thats why im checking for None.
        if self.rules == None:
            # Don't delete the old file if we have not read its rules yet.
            print('I need to read the rules before converting the package file')
            return

        # Backup the old file.
        n = 0
        while True:
            bkp_path = '.'.join((self.path, 'bkp', str(n)))
            if not os.path.exists(bkp_path):
                break
            n +=1
        print('Backing up "%s" to "%s".' % (self.path, bkp_path))
        os.rename(self.path, bkp_path)

        if self.style == 'file':
            print('Going from file to directory style')
            self.style = 'directory'

        elif self.style == 'directory':
            self.style = 'file'

# Parse arguments
parser = ArgumentParser(description="Ease your /etc/portage/package.* edition.")
parser.add_argument('-v', '--version', action='version',
        version='%s %s' % (os.path.basename(sys.argv[0]), __version__))
parser.add_argument('atom', type=str, help="Atom to be modified")
parser.add_argument('flags', type=str, help='Flags to be enabled for the atom, flags starting with %% will be deleted',
        metavar='flags', nargs=REMAINDER, default=None)
parser.add_argument('--prune', '-p', action='store_true',
    help="Remove the custom rule of the specified atom.")
parser.add_argument('--type', '-t', type=str, default='use', choices=Package.pkg_types,
    help="Specify the type of rule (default is use).")
parser.add_argument('--convert', default=False, action='store_true',
        help='convert the package file from file to directory or vice versa')
parser.add_argument('--pkg-file', type=str, dest='pkg_file', metavar='file',
    default='/etc/portage/package',
    help='Specify a package file/directory (for testing/debugging)')

def main():
    args = parser.parse_args()
    pkg = Package(args.pkg_file, args.type)
    pkg.read_rules() # rules are stored in Package.rules

    if args.convert:
        pkg.convert()

    if pkg.type in ['mask', 'unmask']:
        # Handle particular case of package.(un)mask that do not accept flags.
        if args.prune:
            try:
                pkg.rules.remove(args.atom)
            except ValueError:
                sys.exit("%s is not %sed." % (args.atom, pkg.type))
        else:
            if args.atom in pkg.rules:
                sys.exit("%s is already %sed." % (args.atom, pkg.type))
            else:
                pkg.rules.append(args.atom)

    else:
        # Retrieve the current flags if the rule exist.
        flags = []
        for rule in pkg.rules:
            if rule.startswith(args.atom + " "):
                sys.stdout.write("Old rule: " + rule)
                flags = rule.split()[1:]
                pkg.rules.remove(rule) # We remove the rule to update it.
                break
        if not flags:
            print("No argument currently defined for %s." % args.atom)

        # 1.Prune flags
        if args.prune:
            flags = []

        # 3.Manage flags
        if args.flags:
            for flag in args.flags:
                # Disable flags that start with %
                if flag.startswith("%"):
                    flag = flag[1:] # Strip the prefix
                    matches = [f for f in flags if flag in (f, f[1:]) ]
                    if matches:
                        for match in matches:
                            flags.remove(match)
                    else:
                        print('Warning: cannot find a match for %s' % flag)

                elif flag in flags:
                    print("Warning: %s is already enabled!" % flag)
                else:
                    flags.append(flag)

        # Update the rule
        if flags:
            flags.sort()
            rule = args.atom + ' ' + ' '.join(flags) + '\n'
            sys.stdout.write("New rule: " + rule)
            pkg.rules.append(rule)

    # Save changes
    try:
        pkg.save_rules()
    except IOError:
        sys.exit('Unable to write to "%s". Are you root?' % pkg.path)
