#! /usr/bin/env python3

import os, sys, re

def main():
	os.write(1, ("Type exit to quit\n").encode())
	while(True):
		# prompt user input
		uinput = input("$ ")
		if not uinput:
			continue

		if uinput == "exit":
			os.write(1, ("Goodbye...\n").encode())
			break

		handle(uinput)

def handle(uinput):
	cmds = uinput.split()
	rc = os.fork()

	if rc < 0:
	    os.write(2, ("fork failed, returning %d\n" % rc).encode())
	    sys.exit(1)

	elif rc == 0:                   # child
		# check if output set correctly
		if ">" in cmds:
			outputF = None
			try:
				outputF = cmds[cmds.index(">") + 1]
			except IndexError:
				os.write(2, ("syntax error\n").encode())
				pass

			if outputF is not None:
				os.close(1)                 # redirect child's stdout
				sys.stdout = open(outputF, "w")
				fd = sys.stdout.fileno()
				os.set_inheritable(fd, True)
				# remove output section
				outind = cmds.index(">")
				del cmds[outind:outind+2]
		# check if input is set correctly
		if "<" in cmds:
			inputF = None
			try:
				inputF = cmds[cmds.index("<") + 1]
			except IndexError:
				os.write(2, ("syntax error\n").encode())
				pass

			if inputF is not None:
				if not os.path.exists(inputF):
				    os.write(2, ("Input file %s doesn't exist! Exiting" % inputF).encode())
				    sys.exit(1)

				os.close(0)                 # redirect child's stdin
				sys.stdin = open(inputF, "r")
				fd = sys.stdin.fileno()
				os.set_inheritable(fd, True)
				# remove input section
				inind = cmds.index("<")
				del cmds[inind:inind+2]

		for dir in re.split(":", os.environ['PATH']): # try each directory in path
			program = "%s/%s" % (dir, cmds[0])
			try:
				os.execve(program, cmds, os.environ) # try to exec program
			except FileNotFoundError:             # ...expected
				pass                              # ...fail quietly

		os.write(2, ("Error: Could not exec %s\n" % cmds[0]).encode())
		sys.exit(1)                 # terminate with error

	else:        # parent (forked ok)
	    childPidCode = os.wait()

if __name__ == '__main__':
	main()
