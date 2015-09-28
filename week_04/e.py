import cPickle as pickle
import numpy as np
from scipy.sparse import *
from scipy import *
import time
from sklearn.metrics import jaccard_similarity_score

def DBSCAN(d,eps,min_points):
	matrix = csr_matrix(d)
	s = time.time()
	n_points = matrix.shape[0]
	clusters = [-1] * n_points
	cluster_id = 1
	print "Start"
	for i in xrange(n_points):
		if clusters[i] == -1:
			if expandCluster(matrix, i, clusters,cluster_id,eps,min_points):
				cluster_id += 1
				print cluster_id

	e = time.time()
	print "Done " + str(e-s)
	#print clusters
	stat = [0] * (cluster_id)
	for j in xrange(n_points):
		if -2 == clusters[j]:
			stat[0] += 1

	for j in xrange(n_points):
		stat[clusters[j]] += 1

	print range(cluster_id)

	return stat
			
def expandCluster(matrix, p_index, clusters, cluster_id, eps, min_points):
	unclassifiedPoints = extractUnclassifiedPoints(clusters)

	neighbours = findNeighbours(p_index, matrix, eps, unclassifiedPoints)
	if len(neighbours) < min_points:
		clusters[p_index] = -2
		return False
	clusters[p_index] = cluster_id
	for neighbour_id in neighbours:
		clusters[neighbour_id] = cluster_id

	while len(neighbours) > 0:
		current_neighbour_id = neighbours[0]
		new_neighbours = findNeighbours(current_neighbour_id, matrix, eps, unclassifiedPoints)
		
		if len(new_neighbours) >= min_points:
			for id in new_neighbours:
				if clusters[id] == -1 or clusters[id] == -2:
					if clusters[id] == -1:
						neighbours.append(id)
					clusters[id] = cluster_id
		unclassifiedPoints.remove(current_neighbour_id)
		neighbours = neighbours[1:]
	
	return True

def extractUnclassifiedPoints(clusters):
	unclassifiedPoints = set()
	for i in xrange(len(clusters)):
		if clusters[i] < 0:
			unclassifiedPoints.add(i)
	return unclassifiedPoints

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

def jaccardDistance(v1,v2):
	v1Index = 0
	v2Index = 0
	union = 0.0
	intersect = 0.0
	while (v1Index < len(v1) and v2Index < len(v2)):
		if v1[v1Index] == v2[v2Index]:
			union += 1
			intersect += 1
			v1Index += 1
			v2Index += 1
		elif v1[v1Index] > v2[v2Index]:
			union += 1
			v2Index += 1
		elif v1[v1Index] < v2[v2Index]:
			union += 1
			v1Index += 1		

	union += len(v1) - v1Index
	union += len(v2) - v2Index

	if union == 0: return 0
	return 1.0 - intersect / union