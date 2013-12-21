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

HELPTEXT = '''pkanji allows you to do an RTK-style primitive to kanji lookup.

Type "actions" to see all commands.

Typical usage:
1. Type the name of the primitives contained in the kanji one per line.
2. Press enter on a blank line to search. This should give an indexed 
   list of kanji that contain those primitives.
3. Type the number corresponding to the kanji to copy to clipboard.
4. Type "q" to quit, or "c" to clear and repeat the process.

Modifying the primitive to radical map: 
Modify the "pradfile" file. See the file for further instructions.
'''

LICENSETEXT = '''pkanji is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pkanji is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pkanji.  If not, see <http://www.gnu.org/licenses/>.
'''

COPYRIGHTTEXT = '''pkanji  Copyright (C) 2013  Mathew Chong'''

CREDITTEXT = '''RTK Keywords for kanji and primitives (kRTKfile, pradfile):
    Mapping between keywords to kanji and primitives. These files are
    used to facilitate the selection of radicals and to identify the
    RTK keyword for a kanji.

    Copyright for kRTKfile belongs to James W. Heisig. pradfile
    contains some of Heisig's mappings, and some original mappings
    from the users of the Reviewing the Kanji community.


Kanji-radical information (radkfile, kradfile):
    A compositional breakdown of kanji into radicals. These files are
    used to power the core radical to kanji lookup.

    Copyright held by the Electronic Dictionary Research Group. 
    More details and licence can be found at http://www.edrdg.org/
'''