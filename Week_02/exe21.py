#!/usr/bin/python

import sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	A = []

	def import_matrix_to_array(filename):
		inputfile = open(filename, 'r')
		return [[x.strip() for x in line.split()] for line in inputfile]

	def export_array_to_matrix(array, outputname):
		outputfile = open(outputname, 'w')
		for row in array:
			outputfile.write(' '.join(row) + '\n')

	try:
		opts, args = getopt.getopt(argv, 'hi:o:', ['inputfile=', 'outputfile='])
	except getopt.GetoptError:
		print 'exe21.py -i <inputfile> -o <outputfile>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'exe21.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ['-i', '--inputfile']:
			A = import_matrix_to_array(arg)
			print A
		elif opt in ['-o', '--Outputfile']:
			export_array_to_matrix(A, arg)

if __name__ == '__main__':
	main(sys.argv[1:])

