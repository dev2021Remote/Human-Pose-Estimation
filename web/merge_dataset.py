
def mergeFiles():
	# Python program to
	# demonstrate merging
	# of two files

	data = data2 = ""

	# Reading data from file1
	with open('../pose-output1.csv') as fp:
		data = fp.read()

	# Reading data from file2
	with open('../pose-output1.csv') as fp:
		data2 = fp.read()

	# Merging 2 files
	# To add the data of file2
	# from next line
	data += "\n"
	data += data2

	with open ('../pose-output.csv', 'w') as fp:
		fp.write(data)
