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

import codecs
import os
from collections import deque

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

RADKFILE = os.path.join(__location__, 'radkfile')
PRADFILE = os.path.join(__location__, 'pradfile')
KRTKFILE = os.path.join(__location__, 'kRTKfile')
MAX_UNDO = 10

class InvalidRadical(Exception): pass

class Model(object):
    """Maintains the state of the primitive to kanji lookup."""
    def __init__(self):
        """Initializes with empty state."""
        super(Model, self).__init__()
        self._radfilters = set()
        self._radk_map = dict()
        self._prad_map = dict()
        self._kRTK_map = dict()
        self._result_set = set()
        self._changed = True
        self._undo_radfilters_stack = deque()

    def load_files(self):
        """Loads primitive, radical, kanji, RTK mappings."""
        self.load_radkfile()
        self.load_pradfile()
        self.load_kRTKfile()

    def load_radkfile(self):
        """Loads radical to kanji mapping."""
        is_first_rad = True
        rad = None
        strokes = None
        image = None
        klist = list()

        with codecs.open(RADKFILE, 'r', 'euc-jp') as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('#'):
                    continue
                elif line.startswith('$'):
                    r_comps = line.split(' ')
                    if len(r_comps) < 3:
                        raise InvalidRadical()
                    else:
                        if is_first_rad:
                            is_first_rad = False
                        else:
                            self._radk_map[rad] = klist
                            klist = list()

                        rad = r_comps[1]
                        strokes = r_comps[2]
                        image = r_comps[3] if len(r_comps) >= 4 else None
                else:
                    klist.extend(list(line))
                # print line
            self._radk_map[rad] = klist

    def load_pradfile(self):
        """Loads primitive to radicals mapping."""
        with codecs.open(PRADFILE, 'r', 'euc-jp') as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('#'):
                    continue
                prad_comps = line.split(' ')
                if len(prad_comps) <= 1:
                    continue
                rads = list(prad_comps[0])
                for idx in xrange(1, len(prad_comps)):
                    self._prad_map[prad_comps[idx]] = rads
                # print line

    def load_kRTKfile(self):
        """Loads kanji to RTK keywords mapping."""
        with codecs.open(KRTKFILE, 'r', 'utf-16') as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('#'):
                    continue
                kRTK_comps = line.split('\t')
                if len(kRTK_comps) <= 1:
                    continue
                k = kRTK_comps[0]
                RTKs = kRTK_comps[1:]
                self._kRTK_map[k] = RTKs
                # print line

    def keyword_to_primitive(self, keyword):
        """Returns list of radicals corresp. to keyword."""
        return self.primitive_to_radicals(keyword)

    def kanji_to_keyword(self, kanji):
        """Returns list of RTK keywords for a kanji."""
        return list(self._kRTK_map[kanji]) if kanji in self._kRTK_map else list()

    def primitive_to_radicals(self, primitive):
        """Returns list of radicals corresp. to primitive."""
        if primitive in self._prad_map:
            return list(self._prad_map[primitive])
        return list()

    def filter_with_primitive(self, primitive):
        """Add radicals associated with a primitive to the filter."""
        if primitive in self._prad_map:
            self._changed = True
            self._add_to_undo_stack()
            self._radfilters |= set(self._prad_map[primitive])
            return list(self._prad_map[primitive])
        return list()

    def unfilter_primitive(self, primitive):
        """Remove radicals associated with a primitive from the filter."""
        if primitive in self._prad_map:
            self._changed = True
            self._add_to_undo_stack()
            self._radfilters -= set(self._prad_map[primitive])
            return list(self._prad_map[primitive])
        return list()

    def clear_filters(self):
        """Clear all radicals from the filter."""
        self._changed = True
        self._add_to_undo_stack()
        self._radfilters.clear()

    def _add_to_undo_stack(self):
        """Save the current radical filters to the undo stack."""
        self._undo_radfilters_stack.append(set(self._radfilters))
        if len(self._undo_radfilters_stack) > MAX_UNDO:
            self._undo_radfilters_stack.popleft()


    def undo(self):
        """Recover the radical filter before the latest change."""
        if len(self._undo_radfilters_stack) > 0:
            self._changed = True
            self._radfilters = self._undo_radfilters_stack.pop()
            return True
        return False

    def get_rad_filters(self):
        """Returns the current list of radicals in the filter."""
        return list(self._radfilters)

    def results(self):
        """Lazily returns a list of kanji matching the radical filter."""
        if self._changed == True:
            kres = set()
            if len(self._radfilters) > 0:
                rads = set(self._radfilters)
                r = rads.pop()
                kres = set(self._radk_map[r])
                for r in rads:
                    kres &= set(self._radk_map[r])
            self._result_set = kres
            self._changed = False
        return list(self._result_set)

def main():
    m = Model()
    m.load_files()
    # print m._radk_map
    # print m._prad_map
    print m._prad_map['moon']
    print m._prad_map['angel']
    print m.filter_with_primitive('sun')
    print m.filter_with_primitive('mountain')
    print m.filter_with_primitive('field')
    print m.filter_with_primitive('donexits')
    m.clear_filters()
    print m.filter_with_primitive('angel')
    print m.unfilter_primitive('mouth')
    print m.results()
            

if __name__ == '__main__':
    main()
