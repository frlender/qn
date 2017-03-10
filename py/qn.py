import os
import re
import csv
from scipy.misc import comb
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

from clustergram import clustergram



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

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

copydict = lambda dct, *keys: {key: dct[key] for key in keys}

def flatList(listOfLists):
	return [item for sublist in listOfLists for item in sublist]

def printEvery(unit,n):
	if n%unit==0:
		print(n)

def csv2list(pathx,delim='\t'):
    res = []
    with open(pathx,'r') as pf:
        for line in pf:
            line = line.strip('\r\n\t')
            res.append(line.split(delim))
    return res


def plotPCA(mat,labels):
    # columns are samples and rows are genes
    pca = PCA(n_components=3)
    pca.fit(mat)
    ax = scatter3(pca.components_.T,labels)
    ax.set_xlabel('PC1 ('+format(pca.explained_variance_ratio_[0],'.2')+')')
    ax.set_ylabel('PC2 ('+format(pca.explained_variance_ratio_[1],'.2')+')')
    ax.set_zlabel('PC3 ('+format(pca.explained_variance_ratio_[2],'.2')+')')

def plotMDS(distMat,groups=None,labels=None):
	# input should be distance matrix
	mds = MDS(dissimilarity="precomputed",
	max_iter=10000,eps=1e-6)
	print('new')
	mds.fit(distMat)
	coordinates = mds.embedding_
	fig = plt.figure()
	ax = fig.add_subplot(111)
	if groups:
		colors = ['r','y','b','c']
		uniqGroups = list(set(groups))
		groupColors = []
		for group in groups:
			idx = uniqGroups.index(group)
			groupColors.append(colors[idx])
		ax.scatter(coordinates[:,0],coordinates[:,1],c=groupColors)
	else:
		ax.scatter(coordinates[:,0],coordinates[:,1])
	if labels:
		for i,label in enumerate(labels):
			ax.annotate(label,xy=(coordinates[i,0],coordinates[i,1]),
			xytext=(coordinates[i,0],coordinates[i,1]+0.05))
	return ax


def scatter3(mat,labels):
    # colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    colors = ['r','y','b','c']
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plottedLabels = []
    for i, label in enumerate(set(labels)):
        plottedLabels.append(label)
        idx = np.array([True if item==label else False for item in labels])
        print(label,colors[i])
        subMat = mat[idx,:]
        xs = subMat[:,0]
        ys = subMat[:,1]
        zs = subMat[:,2]
        ax.scatter(xs, ys, zs, c=colors[i], marker='o')
    plt.show()
    plt.legend(plottedLabels)
    return ax

def tidy_split(df, column, sep='|', keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.

	Author
	--------
	Daniel Himmelstein @ stackflow
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df

def groupby(iterable,keyFunc):
	res = OrderedDict()
	for item in iterable:
		key = keyFunc(item)
		if key not in res:
			res[key] = []
		res[key].append(item)
	return res

def inferSchema(coll,exclude=['_id']):
	projection = {}
	if exclude:
		for key in exclude:
			projection[key] = False

	summary = {}
	total = 0
	for doc in coll.find(projection=projection):
		total+=1
		for key in doc:
			if key not in summary:
				summary[key] = {'count':0,'type':set()}
			summary[key]['count'] += 1
			summary[key]['type'].add(type(doc[key]))

	for key in summary:
		summary[key]['ratio'] = summary[key]['count']/total
		summary[key]['count'] = str(summary[key]['count'])+'/'+str(total)
		summary[key]['type'] = list(summary[key]['type'])

	return summary

def averageByIndex(series):
	return series.groupby(level=0).mean()

def getParDir(path):
	return os.path.dirname(path)

def getBaseDir():
	currentPath = os.getcwd()
	while currentPath != '/':
		if os.path.isdir(currentPath+'/.git'):
			break
		currentPath = getParDir(currentPath)
	if currentPath == '/':
		raise Exception('Base dir not found because .git directory is not present')
	return currentPath

def addToDict(target,source,keys):
	for key in keys:
		if isinstance(key,str):
			target[key] = source[key]
		else:
			target[key[0]] = source[key[1]]
	return target
