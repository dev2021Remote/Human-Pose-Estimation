def mergeFiles(path=''):
	data = data2 = ""

	# Reading data from file1
	filename = path + 'pose-output1.csv'
	with open(filename) as fp:
		data = fp.read()

	# Reading data from file2
	filename = path + 'pose-output2.csv'
	with open(filename) as fp:
		data2 = fp.read()

	# Merging 2 files
	# To add the data of file2
	# from next line
	data += "\n"
	data += data2

	filename = path + 'pose-output.csv'
	with open (filename, 'w') as fp:
		fp.write(data)
