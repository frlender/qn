import os
import re


def getallfiles(pathx,pattern):
	# improvements: add ignorecase option for re
	matchedPath = []
	for directory, dirnames,filenames in os.walk(pathx):
		eachDirectoryFiles = [os.path.join(directory,perFile) for perFile 
			in filenames if re.search(pattern,perFile)]
		if eachDirectoryFiles:
			matchedPath = matchedPath + eachDirectoryFiles
	return matchedPath

def pinsplit(string,pattern,rangeValue):
	# split a string by pattern at designated point
	# e.g. pinsplit('a,b,ccd-5,6',',',3) outputs ['a,b,ccd-5','6']
	# e.g. pinaplit('a,b,ccd-5,6',',',[1,-1]) outputs ['a','b,ccd-5','6']

	patternIdx = [m.start() for m in re.finditer(pattern,string)]
	# if string doesn't contain any pattern
	if not patternIdx:
		return string
	if type(rangeValue) is int:
		if rangeValue>0:
			rangeValue = rangeValue - 1
		output = []
		output.append(string[:patternIdx[rangeValue]])
		output.append(string[patternIdx[rangeValue]+1:])
		return output
	else:
		patternCount = len(patternIdx)
		rangeValue = map(lambda x: x-1 if x>0 else patternCount+x,rangeValue)
		rangeValue = sorted(rangeValue)
		output = []
		startIdx = 0
		for val in rangeValue:
			endIdx = patternIdx[val]
			output.append(string[startIdx:endIdx])
			startIdx = endIdx+1
		output.append(string[startIdx:len(string)])
		return output

def getfilename(pathx):
	return os.path.splitext(os.path.basename(pathx))[0]
# test
# print getallfiles('.','.py')
# x = 'a,b,ccd-5,6'
# print pinsplit(x,',',-1)

def getNumber(s):
	# parse string to number without raising error
	try:
		return float(s)
	except ValueError:
		return False


def gmt2json(pathx,hasDescColumn=True,isFuzzy=False):
	wordsAll = []
	# secondColumn = []
	with open(pathx,'r') as gf:
		for line in gf:
			line = line.strip('\r\n\t')
#             if not a empty line
			if line:
				words = []
				i = 0
				for item in line.split('\t'):
					if i==0:
						words.append(item)
					else:
#               a gene symbol cannot be a string of numbers.
						if item!="" and not isNumStr(item):
							words.append(item)
				wordsAll.append(words)
				# secondColumn.append(words[1])
	gmtName = getfilename(pathx)
	print(gmtName)
	gmt = []
	if not isFuzzy and hasDescColumn:
		for words in wordsAll:
			gmt.append({'gmt':gmtName,'desc':words[1],
				'term':words[0],'items':words[2:]})
	return gmt