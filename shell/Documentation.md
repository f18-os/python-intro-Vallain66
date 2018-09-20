
UPDATED: 9/19/18

## shell.py
* TEST: N/a

* COMPILE: N/a

* TO RUN: python3 shell.py
		OR
	  ./shell.py

## PRINCIPLE OF OPERATION:
shell.py works by:
	1. printing a prompt that sanitizes empty input, watches for keyword exit to quit program or keyworkd export to change PS1 var
	* if exit is typed the program will break main loop and terminate
	usage `$ exit`
	* if export is typed the program will attempt to parse the new prompt to display
	usage `$ export PS1=<new prompt>`
	2. user input is passed to handle() which interprets command line commands by:
	* input is split into tasks which are then executed in turn
	4. the program forks to run commands separate from shell program
	5. if fork is successful task comprehension begins, if output or input keywords("<", ">") are detected and the proper i/o are 		opened for use
	6. the proper path to the program is found by iterating over all possible paths and attempting to run program using each until 		successful
	7. logic for pipes is handled if more than one task (i.e. multiple programs) are to be run
	8. currently the parent handles input then outputs into the pipe and the child accepts input from the pipe and outputs to STDOUT
	end
	
## NOTE
This shell will handle redirection and pipeing once separatly just fine. Redirection works as expected.
Pipeing works as expected, however as both the parent and child handle a task each when the parent completes its task the shell will exit. After a command is executed the shell will exit normally which is good behavior for a child but is unwanted for the parent. To solve this problem I have started on a version 2 which forks twice and each child then handles a separate task. Which should solve this problem as each child will handle a task and communicate with eachother, then die in turn leaving the parent shell to continue running.
It still has a bug that is very strange; The output of the second task is interpreted as a new command to exec.

* COLLABORATION: N/a
