#! /usr/bin/python
##############################################################################################################
# By: David Workman
# Created: 10/26/2017
# Last Modify: 10/26/2017
#
# This code reads in a csv and parses the second column adding any numbers in that column together with the below exceptions
#
# 1) If the column contains any special characters outside of / or , or \ or " " it will be ignored
# 2) If the column is a date string that parses in the dateutil library it will be ignored
# 3) If the word "to" or "or" appear in the string it is ignored. A word is defined in this case by any string of characters surrounded by spaces.
# 4) There is no sanity done on the number. So if someone mistakenly put a TN or other numerical value in the field it will have that numerical value in there.
# 5) A number must be a composed of character 0-9. I am not accounting for people who spelled out numbers in words since that would require spell check.
# 6) Also as clarification on special characters + or - where excluded as they indicate ranges and/or inexact values. As such they where excluded.
#	The characters chosen where chosen since they have specific value in english vocabulary pertaning to value as follows
#	/ and \ : These where chosen since they are often used when writing out w/ or w\. Though that second one is nonsense, but people do mispel
#	" " : The space character was chosen because I'm lazy and am using the isalnum method of python string to filter all the bad char and we like space.
#	, : This is used as the traditional separater for orders of magnitude in the US. I have to assume that everyone was using that mindset or all is lost
# 7) I finished this late and on an empty stomach so I probably screwed something up. If I did let me know or unscrew it please:)
##############################################################################################################

import csv
import re
from datetime import datetime

def isDate(isDateString):
	"""
	Input: String
	Output: True if Date:False if not
	Checks if string is a date
	"""
	try:
		datetime.strptime(isDateString, "%m/%d/%Y")
		return True
	except ValueError:
		return False

def sanitizeString(MurkyString):
	"""
	Input: String
	Output: String sanitized by rules in this function
	"""

	MurkyString = MurkyString.split()
	if 'to' in MurkyString:
#		print MurkyString
		return ""
	if 'or' in MurkyString:
#		print MurkyString
		return ""

        MurkyString = "".join( [ letter for letter in "".join(MurkyString) if letter not in ["/",",","\\"," "]] )

	return MurkyString

def convertToNumExt(DirtyString):
	"""
	Input: String
	Output: Sum of all numbers in a string (treating clumps of numbers as a single number)
	"""
        if DirtyString.isdigit():
#                print "It's a Number"
#                print DirtyString
                return int(DirtyString)
        elif isDate(DirtyString):
#		print "It's a Date"
#		print DirtyString
                return None

        DirtyString = sanitizeString(DirtyString)

        if DirtyString.isalpha():
#		print "It's a word"
#		print DirtyString
                return None
	elif DirtyString.isalnum():
#		print "It's a alphanumero"
#		print DirtyString
		Nums = re.split("\D*",DirtyString)
		Nums = [ int(Num) for Num in Nums if Num.isdigit() ]
#		print Nums
		return sum(Nums)
	else:
#		print "It's a Nothing"
#		print DirtyString
		try:
			return int(float(DirtyString))
		except:
			return ""	

N = 100000
InputFile = 'Opp.NumberExt.QA5.String.csv'
OutputFile = 'Opp.NumberExt.QA5.Number.csv'
CsvInput = open(InputFile,'rb')
CsvOutput = open(OutputFile,'w+b')
AccountList = csv.reader(CsvInput)
Translation = csv.writer(CsvOutput)
#for x in range(N):
#	Account=AccountList.next()
for Account in AccountList:
	Account[1] = convertToNumExt(Account[1])
#	if not isinstance( Account[1], int):
	Translation.writerow(Account)
CsvInput.close()
CsvOutput.close()
