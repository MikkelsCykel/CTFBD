#!/usr/bin/python

from __future__ import division
from sklearn.metrics import jaccard_similarity_score
import pickle

data_file = open('test_files/data_10points_10dims.dat', 'r')
csr_matrix = pickle.load(data_file)
visited = []
noise = []
clusters = []
in_cluster = []

id = lambda p: '%d%d'%(p[0],p[1])

def mark_point(p, table):
	table.append(p)

def is_marked(p, table):
	return (p in table)

def distance(a, b):
	v1Index = 0
	v2Index = 0
	union = 0.0
	intersect = 0.0
	while (v1Index < len(a) and v2Index < len(b)):
		if a[v1Index] == b[v2Index]:
			union += 1
			intersect += 1
			v1Index += 1
			v2Index += 1
		elif a[v1Index] > b[v2Index]:
			union += 1
			v2Index += 1
		elif a[v1Index] < b[v2Index]:
			union += 1
			v1Index += 1		

	union += len(a) - v1Index
	union += len(b) - v2Index

	if union == 0: return 0
	return 1.0 - intersect / union
#	x = [0, 0]
#	for i in xrange(0, len(a)):
#		x[0] += min(a[i], b[i])
#		x[1] += max(a[i], b[i])
#	return 1 - x[0]/x[1]

def region_query(x, eps):
	def findNeighbours(p,matrix,eps, unclassifiedPoints):
	#s1 = time.time()
	n_points = matrix.shape[0]
	neighbours  = []
	v = matrix[p].indices
	for i in unclassifiedPoints:
		jd = jaccardDistance(v, matrix[i].indices)
		if eps >= jd:
			neighbours.append(i)

	#s2 = time.time()	
	#print s2 - s1
	return neighbours	
	#X = []
	#for row_number, row in enumerate(csr_matrix):
	#	for indice in row.indices:
	#		p = (row_number, indice)
	#		if distance(x, p) <= eps:
	#			X.append(p)
	#print X
	#return X

def expand_cluster(p, neightbor_pts, eps, min_pts):
	c = [p]
	mark_point(id(p), in_cluster)

	for pn in neightbor_pts:
		if not is_marked(id(pn), visited):
			
			mark_point(id(pn), visited)
			neightbor_pnts = region_query(pn, eps)
			
			if len(neightbor_pnts) >= min_pts:
				print len(neightbor_pnts)
				neightbor_pts += neightbor_pnts

			if not is_marked(id(pn), in_cluster):
				c.append(pn)
				print c
				mark_point(id(p), in_cluster)
	return c

def DBSCAN(eps, min_pts):
	for row_number, row in enumerate(csr_matrix):
		for indice in row.indices:
			p = (row_number, indice)
			if is_marked(id(p), visited):
				continue

			mark_point(id(p), visited)
			neightbor_pts = region_query(p, eps)
			
			if len(neightbor_pts) < min_pts:
				mark_point(id(p), noise)
				continue

			clusters.append(expand_cluster(p, neightbor_pts, eps, min_pts))

DBSCAN(0.4, 2)

print csr_matrix
print clusters
print len(clusters)



