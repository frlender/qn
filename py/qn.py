import os
import re
from itertools import combinations
from difflib import SequenceMatcher

def pinsplit(string,pattern,rangeValue):
	# split a string by pattern at designated point
	# e.g. pinsplit('a,b,ccd-5,6',',',3) outputs ['a,b,ccd-5','6']
	# e.g. pinaplit('a,b,ccd-5,6',',',[1,-1]) outputs ['a','b,ccd-5','6']
	
	patternIdx = [m.start() for m in re.finditer(pattern,string)]
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