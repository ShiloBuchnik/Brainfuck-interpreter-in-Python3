import sys
import os
ARRAY_SIZE = 30000
BYTE_SIZE = 256


def handleFileErrors():
	if len(sys.argv) == 1:
		sys.stderr.write("Error: file not provided\n")
		sys.exit(-1)
	elif len(sys.argv) > 2:
		sys.stderr.write("Error: Too many arguments\n")
		sys.exit(-1)

	path = sys.argv[1]
	if not os.access(path, os.F_OK):
		sys.stderr.write("Error: file does not exist\n")
		sys.exit(-1)
	elif path[len(path) - 3:len(path)] != ".bf":
		sys.stderr.write("Error: incompatible type\n")
		sys.exit(-1)
	elif not os.access(path, os.R_OK):
		sys.stderr.write("Error: file is not readable\n")
		sys.exit(-1)

	return path


# Remember Dyck words from Combinatorics course?
# This function creates a dictionary that holds the location for every pair of braces
# Note that this is a bijective map, meaning, if 'start:end' is in the dict, then so as 'end:start'
# We also deal with errors regarding braces pairing here
def createBracesDict(code):
	braces_dict, temp_stack = {}, []

	for i in range(len(code)):
		if code[i] == '[':
			temp_stack.append(i)
		elif code[i] == ']':
			try:
				start = temp_stack.pop()
			except IndexError:  # In this case there's more ']' than '[' currently
				sys.stderr.write("Error: braces pairing is incorrect\n")
				sys.exit(-1)

			braces_dict[start] = i
			braces_dict[i] = start

	if temp_stack:  # We've reached the end with more '[' than ']'
		sys.stderr.write("Error: braces pairing is incorrect\n")
		sys.exit(-1)

	return braces_dict


def interpret(path):
	filename = os.path.split(path)[1]
	fp = open(filename, "r")
	code = "".join(filter(lambda i: i in ['>', '<', '+', '-', '.', ',', '[', ']'], list(fp.read())))
	fp.close()

	data_arr, data_ptr = [0] * ARRAY_SIZE, 0
	braces_dict = createBracesDict(code)

	i = 0
	while i != len(code):
		if code[i] == '>':
			data_ptr = (data_ptr + 1) % ARRAY_SIZE
		elif code[i] == '<':
			data_ptr = (data_ptr - 1) % ARRAY_SIZE
		elif code[i] == '+':
			data_arr[data_ptr] = (data_arr[data_ptr] + 1) % BYTE_SIZE
		elif code[i] == '-':
			data_arr[data_ptr] = (data_arr[data_ptr] - 1) % BYTE_SIZE
		elif code[i] == '.':
			sys.stdout.write(chr(data_arr[data_ptr]))
		elif code[i] == ',':
			data_arr[data_ptr] = ord(sys.stdin.read(1))
		elif code[i] == '[':
			if data_arr[data_ptr] == 0:
				i = braces_dict[i]
		elif code[i] == ']':
			if data_arr[data_ptr] != 0:
				i = braces_dict[i]

		i += 1


path = handleFileErrors()
interpret(path)
print()
