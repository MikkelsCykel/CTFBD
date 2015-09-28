#!/usr/bin/python

import sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	jsondata = ''
	delimeters = ['{', '}', '[', ']']
	symbols = ['.', ',', '\n', '\\', '"', '/', ')', '(', '?', '!', '', ':']
	dictionary = {}

	def _string_contains_delimiter(inputstring):
		return 1 in [d in inputstring for d in delimeters]

	def _extract_words_from_string(inputstring):
		trimmed = ''.join([ch if ch not in symbols else ' ' for ch in inputstring])
		return [word for word in trimmed.lstrip(' ').split(' ') if word]

	def _add_words_to_dictionary(words):
		key = words[0]
		if key in dictionary:
			dictionary[key].append(words[1:])
		else:
			dictionary[key] = words[1:]


	def import_json_file_to_dictionary(filename):
		output = ''
		with open(filename) as data:
			for row in data:
				if _string_contains_delimiter(row):
					continue
				words = _extract_words_from_string(row)
				_add_words_to_dictionary(words)

	def get_bag_of_words_for_json_field(fieldname):
		collection = dictionary[fieldname]
		bag = []
		words = []

		for text in collection:
			for w in text:
				if w.lower() in words:
					continue
				else:
					words.append(w.lower())

		m = len(words)

		for text in collection:
			temp = [0] * m
			for w in text:
				temp[words.index(w.lower())] += 1
			bag.append(temp)
		
		return bag


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
			bagofwords = get_bag_of_words_for_json_field('request_text')
			print bagofwords

if __name__ == '__main__':
	main(sys.argv[1:])
