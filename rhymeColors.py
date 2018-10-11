#!/usr/bin/env python

### rhymeColors.py
### Fabian Gaspero-Beckstrom -

'''
###### IMPORTANT ######

	In order to work you must have both sylvia and termcolor installed.
	Both can be installed via pip but the files can be found below.

	sylvia: 	https://github.com/bgutter/sylvia
	termcolor:	https://pypi.org/project/termcolor/#files

#######################

	This is a program that takes a text file as input and prints it back out
	to the command line with the rhymes color coded. It utilizes a method from a
	seperate program called sylvia in order to retreive a  list of rhymes for each
	word in the input file. It then cycles through each word in the input and
	checks to see if a rhyme for that word exists elsewhere in the text. The
	rhyming words are then grouped and assigned a color in the final output process.

Note 1: Better results may be acheived by switching the 'near' flag on line 62
        to False, depending on the type of content in the input text.

Note 2: Since this program does not take into account the length of the input
        text, the result may appear to make less sense the more lines that are
        fed into it. In other words, rhyming words will be grouped together by
        color regardless fo how distant they are from eachother in the text.
'''

import string
import os
import sys
from termcolor import colored
from sylvia import *
import pkg_resources


_debug = False

# instantiate phonetic dictionary class from sylvia
pd = PhoneticDictionary(binFile=pkg_resources.resource_stream( "sylvia", "cmudict.sylviabin" ))

# get arguments
inFile = sys.argv[1]

colors = ['red','green','yellow','blue','cyan','white','grey']	# define list of colors
omit = ["the", "and", "as", "of"] 								# filler words to omit
output = ""														# initialized output text
word_list = []													# list of words from input w/o filler words
inp = []														# list of words from input w/ filler words
r_matrix = []													# list of lists of rhymes

# the function that does it all
def get_dem_rhymes( word_list, file ):

	# get rhymes for each word
	for word in word_list:
		# get list of rhymes
		rhymes = pd.getRhymes(word, near = True)
		# split into list and append to matrix
		r_matrix.append(rhymes)

	# sanitize rhyme lists in matrix
	for rhymes in r_matrix:
		for i in range(len(rhymes)):
			temp = rhymes[i]
			rhymes[i] = temp.translate(None, string.punctuation).lower()


	wset = set(word_list)
	# new matrix for words grouped by rhyme
	r_list = [[] for x in range(len(word_list))]
	# use set operations to identify matches
	for i in range(len(r_matrix)):
		# insert word itself in front
		r_list[i].insert(0,word_list[i])
		# intersection of sets
		rset = set(r_matrix[i])
		matches = (rset & wset)
		# if result of intersection not empty, add matches to r_list
		if len(matches) > 0:
			for w in matches:
				r_list[i].append(w)

	# set length of r_list
	l = len(r_list)

	# sort r_list from longest to shortest
	r_list.sort(key=len)
	r_list.reverse()

	# sort r_list elements by alphabet
	for i in range(l):
		r_list[i] = sorted(r_list[i])

	if _debug:
		for r in r_list:
			print r
			print '\n'

	# remove repeated lists
	new_l = []
	for elem in r_list:
	    if elem not in new_l:
	        new_l.append(elem)

	# remove lists with shared elements
	new_m = [new_l[x] for x in range(len(new_l)) if x == 0 or new_l[x][0] != new_l[x-1][0]]

	# remove lists with only one element
	rhyme_table = [new_m[x] for x in range(len(new_m)) if len(new_m[x]) > 1]


	if _debug:
		for z in rhyme_table:
			print z



	# read text file by line
	text = ""
	with open(file) as f:
		for line in f.readlines():
			for w in line.split():
				# sanitize
				w = w.translate(None, string.punctuation).lower()
				flag = 0
				for j in range(len(rhyme_table)):
					# if the word is in a rhyme group then color code it
					if w in rhyme_table[j]:
						text = text + " " + colored(w,colors[j%7])
						flag = 1
						break
				if flag == 0:
					text = text + " " + w
			text = text + '\n'

	return text


### Main ###

# open text file
f = open(inFile)
for line in f.readlines():
	words = line.split()
	for w in words:
		# strip punctuation and convert to lowercase
		w = w.translate(None, string.punctuation).lower()
		if w not in omit and len(w) > 2:
			word_list.append(w)
			inp.append(w)
		else:
			inp.append(w)

		# concat output with existing output
output = get_dem_rhymes(word_list, inFile)
# close file
f.close()
# print colorized output
print output



