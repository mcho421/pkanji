#!/usr/bin/env python

# Copyright (C) 2013  Mathew Chong

# This file is part of pkanji.

# pkanji is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pkanji is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pkanji.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from sys import exit
import subprocess
import platform
from Tkinter import Tk
from _version import __version__
from helptext import HELPTEXT, LICENSETEXT, COPYRIGHTTEXT, CREDITTEXT
from model import Model

if platform.system() != 'Windows':
    import sys
    import codecs
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

PROMPT = '$ '
MAX_WIDTH = 70

CLEAR_COMMANDS = frozenset(['reset', 'clear', 'c'])
UNFILTER_COMMANDS = frozenset(['-', 'unf', 'sub', 'rm', 'unfilter', 'minus', 'subtract', 'remove'])
RESULTS_COMMANDS = frozenset(['', '=', 'results', 'search', 'lookup'])
UNDO_COMMANDS = frozenset(['u', 'undo'])
FILTER_COMMANDS = frozenset(['+', 'filter', 'plus', 'add'])
QUIT_COMMANDS = frozenset(['quit', 'q', 'exit', 'close'])
HELP_COMMANDS = frozenset(['help', 'h'])
ACTIONS_COMMANDS = frozenset(['actions'])
LICENSE_COMMANDS = frozenset(['license', 'licence'])
COPYRIGHT_COMMANDS = frozenset(['copyright'])
CREDITS_COMMANDS = frozenset(['credits'])


ACTIONTEXT = '''Help [ {help} ]
    Display the help text.

Actions [ {actions} ]
    Display this list of actions.

License [ {license} ]
    Display software license.

Copyright [ {copyright} ]
    Display software copyright.

Credits [ {credits} ]
    Display credits.

Clear [ {clear} ]
    Clear all radical filters.

Results [ {results} ]
    Returns the kanji results after applying the filters. By default,
    an Enter on a blank line is interpreted as a result action.

Undo [ {undo} ]
    Undo a filter operation.

Filter [ {filter} ]
    Takes one argument. Adds the radicals associated with the 
    primitive to the filter. By default, an action that doesn't match
    any of these actions is interpreted as a filter action.

Unfilter [ {unfilter} ]
    Takes one argument. Removes the radicals associated with the 
    primitive from the filter.

Quit [ {quit} ]
    Quit this program.
'''.format(
        clear=' | '.join(CLEAR_COMMANDS),
        unfilter=' | '.join(UNFILTER_COMMANDS),
        results=' | '.join(RESULTS_COMMANDS),
        undo=' | '.join(UNDO_COMMANDS),
        filter=' | '.join(FILTER_COMMANDS),
        quit=' | '.join(QUIT_COMMANDS),
        help=' | '.join(HELP_COMMANDS),
        license=' | '.join(LICENSE_COMMANDS),
        copyright=' | '.join(COPYRIGHT_COMMANDS),
        credits=' | '.join(CREDITS_COMMANDS),
        actions=' | '.join(ACTIONS_COMMANDS))

class Quit(Exception): pass

# The following uses the Command Pattern to implement commands:

class HelpCommand(object):
    """Displays the help text."""
    def __init__(self):
        super(HelpCommand, self).__init__()

    def execute(self):
        print(HELPTEXT)

class LicenseCommand(object):
    """Displays the license text."""
    def __init__(self):
        super(LicenseCommand, self).__init__()

    def execute(self):
        print(LICENSETEXT)

class CopyrightCommand(object):
    """Displays the copyright text."""
    def __init__(self):
        super(CopyrightCommand, self).__init__()

    def execute(self):
        print(COPYRIGHTTEXT)

class CreditsCommand(object):
    """Displays the credit text."""
    def __init__(self):
        super(CreditsCommand, self).__init__()

    def execute(self):
        print(CREDITTEXT)

class ActionsCommand(object):
    """Displays the list of possible user actions."""
    def __init__(self):
        super(ActionsCommand, self).__init__()

    def execute(self):
        print(ACTIONTEXT)

class ClearCommand(object):
    """Clears all radicals from the filter."""
    def __init__(self, model):
        super(ClearCommand, self).__init__()
        self.model = model

    def execute(self):
        self.model.clear_filters()
        print('All radical filters cleared')

class UndoCommand(object):
    """Undo the radical filter to the previous state."""
    def __init__(self, model):
        super(UndoCommand, self).__init__()
        self.model = model

    def execute(self):
        if self.model.undo():
            print(u'Current radical filters: {}'.format(u''.join(self.model.get_rad_filters())))
        else:
            print('Cannot undo')

class ResultsCommand(object):
    """Computes the kanji that match the radical filter."""
    def __init__(self, model):
        super(ResultsCommand, self).__init__()
        self.model = model

    def execute(self):
        res = self.model.results()
        numk = len(res)
        numd = len(str(numk))
        totalwidth = numd + 1 + 2
        maxlinek = max(MAX_WIDTH // (totalwidth + 1), 1)
        print('{} Matches found (to select, type the number corresponding to the kanji):'.format(numk))
        for i, k in enumerate(res):
            if i % maxlinek == 0 and i != 0:
                print()
            print(u'{:{width}d}:{}'.format(i+1, k, width=numd), end=' ')
        print()
        # print(u''.join(res))

class FilterCommand(object):
    """Adds the radicals assoc. with a primitive to the filter."""
    def __init__(self, model, keyword):
        super(FilterCommand, self).__init__()
        self.model = model
        self.keyword = keyword

    def execute(self):
        ktp = self.model.keyword_to_primitive(self.keyword)
        if ktp:
            self.model.filter_with_primitive(self.keyword)
            print(u'Added to radical filter: {} - {}'.format(self.keyword, u''.join(ktp)))
        else:
            print('Invalid primitive "{}"'.format(self.keyword))
        print(u'Current radical filters: {}'.format(u''.join(self.model.get_rad_filters())))

class UnfilterCommand(object):
    """Removes the radicals assoc. with a primitive from the filter."""
    def __init__(self, model, keyword):
        super(UnfilterCommand, self).__init__()
        self.model = model
        self.keyword = keyword

    def execute(self):
        ktp = self.model.unfilter_primitive(self.keyword)
        if ktp:
            print(u'Removed from radical filter: {} - {}'.format(self.keyword, u''.join(ktp)))
        else:
            print('Invalid primitive "{}"'.format(self.keyword))
        print(u'Current radical filters: {}'.format(u''.join(self.model.get_rad_filters())))

class SelectionCommand(object):
    """Selects a kanji and adds it to the clipboard."""
    def __init__(self, model, selection):
        super(SelectionCommand, self).__init__()
        self.model = model
        self.selection = selection

    def execute(self):
        res = self.model.results()
        if self.selection > len(res) or self.selection <= 0:
            print('Selection is out of range: {}'.format(self.selection))
        else:
            kanji = res[self.selection - 1]
            copy_to_clipboard(kanji)
            RTK_string = ''
            if self.model.kanji_to_keyword(kanji):
                RTK_keyword_string = u'/'.join(self.model.kanji_to_keyword(kanji))
                RTK_string = ' ({})'.format(RTK_keyword_string)
            print(u'Copied to clipboard: "{}"{}'.format(kanji, RTK_string))

def copy_to_clipboard(text):
    """Copy text to the clipboard."""
    if platform.system() == 'Darwin':
        subprocess.Popen(["pbcopy", "w"], stdin=subprocess.PIPE).communicate(text.encode('utf8'))
    elif platform.system() == 'Linux':
        subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE).communicate(text.encode('utf8'))
    else:
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.quit()

def get_command(model):
    """Get a command to execute."""
    line = raw_input(PROMPT)
    line = line.lower()
    if len(line) >= 2 and line[0] in {'-', '+'}:
        line = line[0] + ' ' + line[1:]
    comps = line.split(' ')

    if comps[0] in CLEAR_COMMANDS:
        return ClearCommand(model)
    elif comps[0] in UNFILTER_COMMANDS:
        if len(comps) < 2:
            print('Not enough arguments to unfilter')
        else:
            return UnfilterCommand(model, comps[1])
    elif comps[0] in FILTER_COMMANDS:
        if len(comps) < 2:
            print('Not enough arguments to filter')
        else:
            return FilterCommand(model, comps[1])
    elif comps[0] in RESULTS_COMMANDS:
        return ResultsCommand(model)
    elif comps[0] in UNDO_COMMANDS:
        return UndoCommand(model)
    elif comps[0].isdigit():
        return SelectionCommand(model, int(comps[0]))
    elif comps[0] in QUIT_COMMANDS:
        raise Quit()
    elif comps[0] in HELP_COMMANDS:
        return HelpCommand()
    elif comps[0] in ACTIONS_COMMANDS:
        return ActionsCommand()
    elif comps[0] in LICENSE_COMMANDS:
        return LicenseCommand()
    elif comps[0] in COPYRIGHT_COMMANDS:
        return CopyrightCommand()
    elif comps[0] in CREDITS_COMMANDS:
        return CreditsCommand()
    else:
        return FilterCommand(model, comps[0])
    return None

def main():
    """Interactive loop."""
    try:
        m = Model()
        m.load_files()
        print('pkanji -- Kanji lookup by RTK-style primitives (v{})'.format(__version__))
        print('Type "help", "actions", "credits", "license" or "copyright" for more info')
        while True:
            command = get_command(m)
            if command:
                command.execute()
    except (Quit, EOFError, KeyboardInterrupt) as e:
        pass
    except IOError as e:
        print(e)
        exit(1)
    except UnicodeEncodeError as e:
        print(e)
        print('Please ensure your console can display Japanese characters.')
        exit(2)

if __name__ == '__main__':
    main()
