# Introduction 

This is a suite of scripts for manipulation of text files using Python.

The programs are generic so should work in a variety of contexts. 

# Getting Started

These scripts can be run with Python.

In Bupa, this is only possible if you have a Virtual Machine with Anaconda or equalivalent package installed.

# Scripts available

## Cleanse TXT

This script is used to replace commonly encountered abberrant characters and remove anything that can't be distinguished as text, numerals or common punctuation.

This program imports a text file and exports another of the same name with the prefix "_cleansed" following the name.

Where characters are not recognised, an exception report is created with the prefix "_exceptions" following the name. This file only includes lines with unicode backslash strings present. The aim is to eliminate all exceptions before importing the data into a new master spreadsheet.

All output files are saved in the same directory as the original file. The original file is untouched so the content can be compared before and after transformation using Notepad++ compare.

# Contribute

If you want to contribute to this list of scripts, clone the VSTS repo and test your updates locally before pushing to master.

Please do not post routines that have hardcoded data references that can't work in most situations.
