#!/usr/bin/python

from __future__ import division
from sklearn.metrics import jaccard_similarity_score
import pickle

data_file = open('test_files/data_10points_10dims.dat', 'r')
csr_matrix = pickle.load(data_file)

visited = []
in_cluster = []

def mark_point(p, table):
	table.append(p)

def is_marked(p, table):
	return (p in table)

def distance(a, b):
	i1 = 0; i2 = 0; union = 0.0; intersect = 0.0
	while (i1 < len(a) and i2 < len(b)):
		if a[i1] == b[i2]:
			union += 1; intersect += 1 ;i1 += 1; i2 += 1
		elif a[i1] > b[i2]:
			union += 1; i2 += 1
		elif a[i1] < b[i2]:
			union += 1; i1 += 1		
	union += len(a) - i1; union += len(b) - i2
	if union == 0: return 0
	return 1.0 - intersect / union

def region_query(p, eps):
	dim = csr_matrix.shape[0]
	X = []
	vector = csr_matrix[p].indices
	for pp in xrange(0, dim):
		if distance(vector, csr_matrix[pp].indices) <= eps:
			X.append(pp)
	return X

def expand_cluster(p, neightbor_pts, eps, min_pts):
	c = [p]
	mark_point(p, in_cluster)
	for pn in neightbor_pts:
		if not is_marked(pn, visited):
			mark_point(pn, visited)
			neightbor_pnts = region_query(pn, eps)		
			if len(neightbor_pnts) >= min_pts:
				neightbor_pts += neightbor_pnts
			if not is_marked(pn, in_cluster):
				c.append(pn)
				mark_point(p, in_cluster)
	return c

def DBSCAN(eps, min_pts):
	noise = []
	clusters = []
	dim = csr_matrix.shape[0]
	for p in xrange(0, dim):
		if is_marked(p, visited):
				continue
		mark_point(p, visited)
		neightbor_pts = region_query(p, eps)
		if len(neightbor_pts) < min_pts:
			mark_point(p, noise)
			continue
		clusters.append(expand_cluster(p, neightbor_pts, eps, min_pts))
	return clusters, noise
		
C,N = DBSCAN(0.4, 2)

print
print 'Clasified as clusters:'
print C
print
print 'Clasified as Noise:'
print N
print