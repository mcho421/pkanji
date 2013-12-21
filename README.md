pkanji Readme
==============================================================================

What is pkanji?
---------------
pkanji is a command line program that allows you to do an RTK-style primitive
to kanji lookup. pkanji is aimed towards users who have completed Heisig's
Remembering the Kanji book.

Web applications that allow you to search kanji by radicals (such as 
jisho.org) require visual selection of radicals from a list which can be a 
slow process. Users familiar with RTK should be able to identify the names of 
the primitives that compose a kanji. pkanji allows the selection of radicals 
use as a filter by simply typing the names of the primitives.

The map between primitives and radicals can be customized by the user. One can
also define new primitives and how they map to radicals.

pkanji uses the radkfile by the Electronic Dictionary Research group to power
the lookup.

Installation
------------
These instructions are for Windows users. The instructions should be similar
for Mac and Linux.

- Windows users make sure your command prompt can display Japanese characters.
  One way this can be achieved is by setting your system locale to Japanese.

1) Unzip pkanji.

2) In the pkanji directory, run pkanji.exe.

3) OPTIONAL. Put the pkanji directory in your PATH. This will allow you to
   to quickly open pkanji from the Run dialog (Win+R) by typing "pkanji".

- Note: If pkanji crashes unexpectedly, try running pkanji-pause.bat to
        to diagnose the problem.

How to use
----------
Typical usage would involve:
1) Type the name of the primitives contained in the kanji one per line.
   See the "pradfile" file for all the inputtable primitives.
2) Press enter on a blank line to search. This should give an indexed 
   list of kanji that contain those primitives.
3) Type the number corresponding to the kanji to copy to clipboard.
4) Type "q" to quit, or "c" to clear and repeat the process.

To modify the primitive to radical map, modify the "pradfile" file. See the
comments in the file for further instructions.

For more information, type "help" or "actions" in the program.

Official Repository
-------------------
https://github.com/mcho421/pkanji

Contact
-------
Mathew Chong
mathewchong7@gmail.com

Credits
-------
RTK Keywords for kanji and primitives (kRTKfile, pradfile):
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


