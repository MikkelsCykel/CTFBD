#!/usr/bin/python

import sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	bitstrings = []

	def _get_binary_rec(n):
		if not n:
			return ''
		else:
			return _get_binary(n / 2) + str(n % 2)

	def _apply_padding(n, w):
		return '0' * (n - len(w)) + w

	def get_n_binary_repesentations(N):
		return [_apply_padding(N, _get_binary(n)) for n in xrange(2 ** N)]

	try:
		opts, args = getopt.getopt(argv, 'hi:', ['inputinteger='])
	except getopt.GetoptError:
		print 'exe22.py -i <inputinteger>'
		sys.exit(2)
		

	for opt, arg in opts:
		if opt == '-h':
			print 'exe22.py -i <inputinteger>'
			sys.exit()
		elif opt in ['-i', '--inputinteger']:
			try:
				argint = int(arg)
				posiblecombinations = 2 ** argint
				bitstrings = get_n_binary_repesentations(argint)
				totalfound = len(bitstrings)
				if(posiblecombinations is not totalfound):
					print 'Something went wrong missed %d possible combinations'%(posiblecombinations - totalfound)
					print bitstrings 
				else:
					print bitstrings
					print 'total: %d'%(posiblecombinations)

			except ValueError:
				print 'exe22.py -i <inputinteger>'
				sys.exit(2)

if __name__ == '__main__':
	main(sys.argv[1:])
