import sys
import os

def handle_errors():
	if len(sys.argv) != 2:
		sys.stderr.write("Error: Too many arguments")
		sys.exit(-1)

	path = sys.argv[1]
	if not os.access(path, os.R_OK):
		sys.stderr.write("Error: file does not exist")
		sys.exit(-1)
	elif not os.access(path, os.R_OK):
		sys.stderr.write("Error: file is not readable")
		sys.exit(-1)

	return path

def interpret(path):
	filename = os.path.split(path)[1]
	fp = open(filename, "r")
	code = "".join(filter(lambda i: i in ['>', '<', '+', '-', '.', ',', '[', ']'], list(fp.read())))
	fp.close()

	dataArr, dataPtr = [0] * 30000, 0

	for i in code:
		print("hey")




def main():
	path = handle_errors()
	interpret(path)