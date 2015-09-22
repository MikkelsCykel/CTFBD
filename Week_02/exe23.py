#!/usr/bin/python

import sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	jsondata = ''
	delimeters = ['{', '}', '[', ']']
	symbols = ['.', ',', '\n', '\\', '"', '/', ')', '(', '?', '!', '', ':']

	def _string_contains_delimiter(inputstring):
		return 1 in [d in inputstring for d in delimeters]

	def _extract_words_from_string(inputstring):
		trimmed = ''.join([ch if ch not in symbols else ' ' for ch in inputstring])
		return [word for word in trimmed.lstrip(' ').split(' ') if word]

	def _add_words_to_dictionary(words):
		key = 

	def import_json_file_to_dictionary(filename):
		output = ''
		with open(filename) as data:
			for row in data:
				if _string_contains_delimiter(row):
					continue
				print _extract_words_from_string(row)

	def extract_all_values_from_json_field():
		return 'not implemented yet'

	try:
		opts, args = getopt.getopt(argv, 'hi:f:', ['jsonfile=', 'jsonfield'])
	except getopt.GetoptError:
		print 'exe23.py -i <jsonfile> -f <jsonfield>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'exe23.py -i <jsonfile> -f <jsonfield>'
			sys.exit()
		elif opt in ['-i', '--jsonfile']:
			jsondata = import_json_file_to_dictionary(arg)
		elif opt in ['-f', '--jsonfield']:
			extract_all_values_from_json_field(arg)

if __name__ == '__main__':
	main(sys.argv[1:])
