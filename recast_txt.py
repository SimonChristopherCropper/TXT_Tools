#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
-----------------------------   recast_txt()   ------------------------------

This script is used to replace commonly encountered abberrant characters
and remove anything that can't be distinguished as text, numerals or
common punctuation.

This program imports a text file and exports another of the same name
with the prefix "_recast" following the name.

Where characters are not recognised, an exception report is created.

The program is run by typing "python recast_txt.py" in the Ancaconda
console. A dialog will appear allowing you to select a file to recast.

Programmed by Simon Christopher Cropper 11 April 2019

"""

#***********************************************************************
#***********************     GPLv3 License      ************************
#***********************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************

#-----------------------------------------------------------------------------
#--- DEFINITIONS AND VARIABLES
#-----------------------------------------------------------------------------

# import modules
import re
import os
import tkinter as tk
from tkinter import filedialog

#-----------------------------------------------------------------------
#--- DIRECTORY DIALOG
#-----------------------------------------------------------------------

ROOT = tk.Tk()
ROOT.withdraw()
ROOT.filename = filedialog.askopenfilename(filetypes=(
    ("CSV Files", "*.csv"),
    ("Text File", "*.txt"),
    ("All Files", "*.*")), title="Choose a file.")

#-----------------------------------------------------------------------
#--- CLEANUP NAMES
#-----------------------------------------------------------------------

INPUT_PATH, INPUT_FILE_NAME = os.path.split(ROOT.filename)
INPUT_FILE_NAME, INPUT_FILE_EXTENSION = os.path.splitext(INPUT_FILE_NAME)
OUTPUT_FILEPATH = INPUT_PATH + '/' + INPUT_FILE_NAME + \
                "_recast" + INPUT_FILE_EXTENSION
EXCEPTIONS_FILEPATH = INPUT_PATH + os.sep + INPUT_FILE_NAME + \
                "_exceptions" + INPUT_FILE_EXTENSION

#-----------------------------------------------------------------------
#--- GLOBAL VARIABLES
#-----------------------------------------------------------------------

RECAST_ENCODING = "ascii"

#-----------------------------------------------------------------------------
#--- CORE PROGRAM
#-----------------------------------------------------------------------------

# Continue if a file has been selected
if ROOT.filename:

    # Get text from each file listed in shortlist
    START_STRING = open(ROOT.filename, encoding=RECAST_ENCODING, errors="backslashreplace").read()

    # make a copy so we can see if any text has changed. If nothing changes we
    # should not save.
    FINISH_STRING = START_STRING

    # Look into the file and see if any date flags present and replace with
    # the date modified
    # https://www.utf8-chartable.de/unicode-utf8-table.pl?start=8192&number=128&utf8=string-literal

    # A list of obvious SUBSTITUTIONS where context is not lost
    SUBSTITUTIONS = {

        # Single curley or oblique quotes
        r'\\xe2\\x80\\x98' : "'",
        r'\\xe2\\x80\\x99' : "'",
        r'\\xc2\\x81[fgh]' : "'",
        r'\\xc2\\xa1\\xc2\\xa5' : "'",
        r'\\xc2\\xa1\\xc2\\xa6' : "'",

        # Double curley or oblique quotes
        r'\\xe2\\x80\\x9c' : '"',
        r'\\xe2\\x80\\x9d' : '"',
        r'\\xc2\\xa1\\xc2\\xa7' : '"',
        r'\\xc2\\xa1\\xc2\\xa8' : '"',

        # hyphens of various lengths (dash, en-dash, em-dash, horizontal bar)
        r'\\xe2\\x80\\x90' : '-',
        r'\\xe2\\x80\\x91' : '-',
        r'\\xe2\\x80\\x92' : '-',
        r'\\xe2\\x80\\x93' : '-',
        r'\\xe2\\x80\\x94' : '-',
        r'\\xe2\\x80\\x95' : '-',
        r'\\xc2\\xad' : '-',

        # Various bullets
        r'\\xc2\\xb7' : '*',
        r'\\xe2\\x80\\x9eh' : '*',
        r'\\xe2\\x80\\xa2' : '*',

        # Eclypse
        r'\\xe2\\x80\\xa6' : '...',

        # Fractions
        r'\\xc2\\xbc' : '1/4',
        r'\\xc2\\xbd' : '1/2',
        r'\\xc2\\xbe' : '3/4',
        r'\\xc2\\xa9' : '(c)',
        r'\\xc2\\xb0[Cc]' : 'degrees celcius',
        r'\\xc2\\xb0' : ' degrees',

        # Characters with cedilla, grave, acute, circumflex, diaeresis
        r'\\xc3\\xa9' : 'e',
        r'\\xc3\\xab' : 'e',
        r'\\xc3\\xa8' : 'e',
        r'\\xc3\\xb1' : 'n',

        # Ambiguous muddled sequences
        r'\\xc3\\xa2\\xe2\\x82\\xac\\xe2\\x84\\xa2' : "'",
        r'\\xc3\\xa2\\xe2\\x82\\xac' : '-',
        r'\\xc2\\x81\\xc5\\x93' : '-',
        r'\\xc6\\x92\\xc2\\xba' : ' ',
        r'\\xc6\\x92' : ' ',
        r'\\xc6\\x92n' : ' ',

        r'\\xc3\\x9f' : ' ',
        r'\\xc2\\xac' : ' ',
        r'\\xe2\\x80\\x9e\\xc3\\x91' : ' ',
        r'\\xc2\\xa1\\xc3\\xaa' : ' ',
        r'\\xc2\\xa1V' : '-'}

    for UnicodeStr, ReplaceStr in SUBSTITUTIONS.items():
        FINISH_STRING = re.sub(UnicodeStr, ReplaceStr, FINISH_STRING)

    # check if the START_STRING and endstring is different, if yes save

    if FINISH_STRING == START_STRING:

        # Good news, no abberrant characters found
        print("No clean-up required")

    else:

        # Cleaned data stored in output file
        OF = open(OUTPUT_FILEPATH, "w", encoding=RECAST_ENCODING)
        OF.write(FINISH_STRING)
        OF.close()
        print("The recast data is stored in the file {}".format(OUTPUT_FILEPATH))

        #---------------------------------------------------------------------
        #--- ADDITIONAL CHECKS
        #---------------------------------------------------------------------

        # Create an exception file to contain any lines with abberrant
        # characters not caught with above
        EXCEPTIONS_FILE = open(EXCEPTIONS_FILEPATH, 'w',
                               encoding=RECAST_ENCODING, errors="backslashreplace")

        # Scan output file for any more charcater sequences that
        # need to be adressed
        LINE_NUM = 1
        for line in open(OUTPUT_FILEPATH, "r",
                         encoding=RECAST_ENCODING, errors="backslashreplace"):
            LINE_NUM += 1
            if re.search(r'\\x[a-z0-9]{2}', line):
                EXCEPTIONS_FILE.write(str(LINE_NUM) + " " + line)

        # Close file
        EXCEPTIONS_FILE.close()

        # Check if anything actually found
        if os.path.getsize(EXCEPTIONS_FILEPATH) == 0:

            # Silently remove working file
            os.remove(EXCEPTIONS_FILEPATH)

        else:

            # Let the user know more work required.
            print("WARNING: Exceptions still occur in the recast data")
            print("Open the file '{}' and review the lines \
                  containing unicode.".format(EXCEPTIONS_FILEPATH))

# Capture that dialog exited and returns no list
else:

    print("No file selected. Bye.")
