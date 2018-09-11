AUTHOR: Eric Lugo (enlugo)
COMPLETED: 9/9/18

## shell.py
* TEST: N/a

* COMPILE: N/a

* TO RUN: python3 shell.py

## PRINCIPLE OF OPERATION:
shell.py works by:
	1. printing a prompt that sanitizes empty input, watches for keyword exit to quit program
	* if exit is typed the program will break main loop and terminate
	2. user input is passed to handle() which interprets command line commands by:
	3. input is split into word tokens
	4. the program forks to run commands separate from shell program
	5. if fork is successful word comprehension begins, if output or input keywords("<", ">") are detected and the proper i/o are opened for use
	6. the proper path to the program is found by iterating over all possible paths and attempting to run program using each until successful
	end

* COLLABORATION: N/a
