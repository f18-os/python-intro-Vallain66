AUTHOR: Eric Lugo
COMPLETED: 9/3/18

* PROGRAM: wordCount.py,
* TEST: wordCountTest.py

* COMPILE: N/a

* TO RUN: python3 ./wordcount.py <input text file> <output file>

	where <input file text> is the text file with words to count
				<output file> is the file to save the word counts

* TO TEST: python3 ./wordCountTest.py <input text file> <output file> <key text file>

	where <input file text> is the text file with words to count
				<output file> is the file to save the word counts
				<key text file> is the file to test output against for correctness

* PRINCIPLE OF OPERATION:
	wordCount.py works:
	1. reading the input file into memory
	2. rempunc() handles removing punctuation by either inserting a space or empty space
	3. all lines are converted to lowercase and split into word tokens
	4. word tokens are passed to countwords() which returns a dictionary of words and their counts
	5. the wordcount is written to the specified output file line by line with a space between word and its counts
	end

* COLLABORATION: N/a	
