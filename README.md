# Introduction 

This is a suite of scripts for manipulation of text files using Python.

The programs are generic so should work in a variety of contexts. 

# Getting Started

These scripts can be run with Python 3.

# Scripts available

## Recast TXT

This script is used to replace commonly encountered abberrant characters and remove anything that can't be distinguished as text, numerals or common punctuation.

This program imports a text file and exports another of the same name with the prefix "_cleansed" following the name.

Where characters are not recognised, an exception report is created with the prefix "_exceptions" following the name. This file only includes lines with unicode backslash strings present. 

The aim is to eliminate all exceptions before importing the data into a new master spreadsheet. This can be done by adding to the list of known sequences in the Python code or removing the sequence from the orignal text file.

All output files are saved in the same directory as the original file. The original file is untouched so the content can be compared before and after transformation using Notepad++ compare.

**Note 1** - The text in this routine is cast to ASCII and any character that is not able to be decoded to ASCII, replaced with a unicode backslash sequence. These sequences can be left or translated to an appropriate symbol suitable for the system where the data will be imported. ASCII was chosen as it represented the lowest common denominator in most systems. If the recipient data repository is encoded as UTF-8 the import routine can be adjusted accordingly.

**Note 2** - Aberrant characters can originate from several sources. When moving data, via cut-and-paste, from two known environments (e.g. UTF-8 to CP1252, CP10000 to CP1252) character reconciliation is usually straightforward but in a modern workplace where people can be using many environments (Windows Desktop with CP1252, Macintosh Laptop or iPad with codepage 10,000, Internet based environment coded in UTF-8) and where most computer systems are not codepage aware, you can end up with a subset of characters that can not be interpreted by the system you are operating within at any particular time. This can be further complicated when you move between 7-bit, 8-bit, 16-bit or 32-bit environments where a single character can be represented by a string of 2-3 characters when you try and decode it in the wrong codepage.

# Contribute

If you want to contribute to this list of scripts, clone the VSTS repo and test your changes or updates in a sensible named branch before pushing to master.

Please do not post routines that have hardcoded data references that can't work in most situations.
