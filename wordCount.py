import sys, os, re

def rempunc(str):
	# replace - and ' with space
	str = str.replace("-", " ")
	str = str.replace("\'", " ")
	#remove all other punctuation
	pattern = re.compile('[!?.,:;"]')
	return pattern.sub("", str)


def countwords(words):
	wordmap = {}
	for word in words:
		if word not in wordmap.keys():
			wordmap[word] = 1
		else:
			count = wordmap[word]
			wordmap[word] = count + 1
	return wordmap

def main():
	if len(sys.argv) is not 3:
		print("Correct usage: wordcount.py <input text file> <output file>")
		exit()

	inputFname = sys.argv[1]
	outFname = sys.argv[2]

	#first input file exists
	if not os.path.exists(inputFname):
	    print ("text file input %s doesn't exist! Exiting" % inputFname)
	    exit()
	#make check outfile exists
	elif not os.path.exists(outFname):
	    print ("text file output %s doesn't exist! Exiting" % outFname)
	    exit()

	# get input file as string
	with open(inputFname, 'r') as file:
		words = file.read()

	lines = []
	wordcount = {}

	# remove punctuation and place into dict
	words = rempunc(words)
	lines = words.lower().split()

	wordcount = countwords(lines)

	# write dict to output file
	with open(outFname, 'w') as ofile:
		for key, val  in sorted(wordcount.items()): # sorted alphabeta
			ofile.write("%s %s\n" % (key,val))

if __name__ == "__main__":
	main()
