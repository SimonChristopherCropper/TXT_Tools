#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
-----------------------------   Cleanse_TXT()   ------------------------------

This script is used to replace commonly encountered abberrant characters 
and remove anything that can't be distinguished as text, numerals or 
common punctuation.

This program imports a text file and exports another of the same name 
with the prefix "_cleansed" following the name.

Where characters are not recognised, an exception report is created.

Programmed by Simon Christopher Cropper 11 April 2018

"""

#-----------------------------------------------------------------------------
#--- DEFINITIONS AND VARIABLES                                                
#-----------------------------------------------------------------------------

# import modules
import re
import os
import sys
from tkinter import filedialog
from tkinter import *

#-----------------------------------------------------------------------
#--- DIRECTORY DIALOG
#-----------------------------------------------------------------------

root = Tk()
root.withdraw()
root.filename = filedialog.askopenfilename(
					filetypes =(("CSV Files", "*.csv"),
								("Text File", "*.txt"),
								("All Files","*.*")
								),
					title = "Choose a file.")

#-----------------------------------------------------------------------
#--- CLEANUP NAMES
#-----------------------------------------------------------------------

#input_filepath = sys.argv[1]

input_path, input_file_name = os.path.split(root.filename)
input_file_name, input_file_extension = os.path.splitext(input_file_name)
output_filepath = input_path + '/' + input_file_name + \
				"_cleansed" + input_file_extension
exceptions_filepath = input_path + os.sep + input_file_name + \
				"_exceptions" + input_file_extension

#-----------------------------------------------------------------------------
#--- CORE PROGRAM                                              
#-----------------------------------------------------------------------------

if root.filename:

	# Get text from each file listed in shortlist
	startstring = open(root.filename, encoding="ascii", errors="backslashreplace").read()
	
	# make a copy so we can see if any text has changed. If nothing changes we 
	# should not save.
	finishstring = startstring
	
	# Look into the file and see if any date flags present and replace with 
	# the date modified
	# https://www.utf8-chartable.de/unicode-utf8-table.pl?start=8192&number=128&utf8=string-literal

	# A list of obvious substitutions where context is not lost
	Substitutions = {
	
		# Single curley or oblique quotes
		r'\\xe2\\x80\\x98' : "'" ,
		r'\\xe2\\x80\\x99' : "'" ,
		r'\\xc2\\xa1\\xc2\\xa5' : "'" , 
		r'\\xc2\\xa1\\xc2\\xa6' : "'" ,
		
		# Double curley or oblique quotes
		r'\\xe2\\x80\\x9c' : '"' ,
		r'\\xe2\\x80\\x9d' : '"' ,
		r'\\xc2\\xa1\\xc2\\xa7' : '"' ,
		r'\\xc2\\xa1\\xc2\\xa8' : '"' ,
		
		# hyphens of various lengths (dash, en-dash, em-dash, horizontal bar)
		r'\\xe2\\x80\\x90' : '-' , 
		r'\\xe2\\x80\\x91' : '-' ,
		r'\\xe2\\x80\\x92' : '-' ,
		r'\\xe2\\x80\\x93' : '-' ,
		r'\\xe2\\x80\\x94' : '-' ,
		r'\\xe2\\x80\\x95' : '-' ,
		
		# Various bullets
		r'\\xc2\\xb7' : '*' ,
		r'\\xe2\\x80\\x9eh' : '*' ,
		r'\\xe2\\x80\\x9eh' : '*' ,
		r'\\xe2\\x80\\xa2' : '*' ,
		
		# Eclypse
		r'\\xe2\\x80\\xa6' : '...' ,
		
		# Fractions
		r'\\xc2\\xbd' : '1/2' ,
		
		# Characters with cedilla, grave, acute, circumflex, diaeresis
		r'\\xc3\\xa9' : 'e' ,
		
		# Ambiguous muddled sequences
		r'\\xc3\\xa2\\xe2\\x82\\xac\\xe2\\x84\\xa2' : "'" ,
		r'\\xc3\\xa2\\xe2\\x82\\xac' : '-' ,
		r'\\xc6\\x92' : ' ' ,
		r'\\xc6\\x92n' : ' '  ,
		r'\\xc3\\x9f' : ' ' ,
		r'\\xe2\\x80\\x9e\\xc3\\x91' : ' ' 
			}
			
	for UnicodeStr, ReplaceStr in Substitutions.items():
		finishstring = re.sub(UnicodeStr, ReplaceStr, finishstring)
	
	# check if the startstring and endstring is different, if yes save

	if finishstring == startstring:
	
		# Good news, no abberrant characters found
		print("No clean-up required")
		
	else:
	
		# Cleaned data stored in output file
		o = open(output_filepath,"w", encoding="ascii")
		o.write(finishstring)
		o.close()
		print("The cleansed data is stored in the file {}".format(output_filepath))
		
		#---------------------------------------------------------------------
		#--- ADDITIONAL CHECKS                                              
		#---------------------------------------------------------------------
		
		# Create an exception file to contain any lines with abberrant 
		# characters not caught with above
		exceptions_file = open(exceptions_filepath, 'w', 
								encoding='ascii', errors="backslashreplace")
		
		# Scan output file for any more charcater sequences that 
		# need to be adressed
		for line in open(output_filepath,"r", 
								encoding="ascii", errors="backslashreplace"):
			if re.search(r'\\x[a-z0-9]{2}', line):
				exceptions_file.write(line)
		
		# Close file
		exceptions_file.close()
		
		# Check if anything actually found
		if os.path.getsize(exceptions_filepath) == 0:
		
			# Silently remove working file
			os.remove(exceptions_filepath)
			
		else:
		
			# Let the user know more work required.
			print("WARNING: Exceptions still occur in the cleansed data")
			print("Open the file '{}' and review the lines containing unicode.".format(exception_filepath))
			
# Capture that dialog exited and returns no list
else:

	print("No file selected. Bye.")




