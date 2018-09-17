#! /usr/bin/env python3

import os, sys, re

PS1 = "$ "
def main():
	os.write(1, ("Type exit to quit\n").encode())
	while(True):
		# prompt user input
		uinput = input(PS1)
		if not uinput:
			continue
		if prompt(uinput):
			continue
		isexit(uinput)
		handle(uinput)

def isexit(str):
	if str == "exit":
		os.write(1, ("Goodbye...\n").encode())
		sys.exit(0)

def prompt(uinput):
	if uinput.startswith("export PS1"):
		uinput = re.split("=", uinput)
		print(uinput)
		global PS1
		PS1 = uinput[1]
		return True
	if uinput == "$PS1":
		print(PS1)
		return True

def isredirect(cmds):
	return ">" in cmds or "<" in cmds

def redirect(cmds):
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
	return cmds

def execute(cmds):
	for dir in re.split(":", os.environ['PATH']): # try each directory in path
		program = "%s/%s" % (dir, cmds[0])
		try:
			os.execve(program, cmds, os.environ) # try to exec program
		except FileNotFoundError:             # ...expected
			pass                              # ...fail quietly

	os.write(2, ("Error: Could not exec %s\n" % cmds[0]).encode())
	sys.exit(1)								  # terminate with error

def ispipe(cmds):
	return "|" in cmds

def closepipe(r, w):
	os.close(r)
	os.close(w)

#def creatpipe(cmds):

def handle(uinput):
	cmds = uinput.split()
	pipe = ispipe(cmds)
	if pipe:
		r, w = os.pipe()
		# remove pipe section
		secondcmd = []
		pipeind = cmds.index("|")
		del cmds[pipeind]
		secondcmd.append(cmds.pop(pipeind))

		print("sec cmd: ")
		print(secondcmd)

	rc = os.fork()

	if rc < 0:
	    os.write(2, ("fork failed, returning %d\n" % rc).encode())
	    sys.exit(1)

	elif rc:        # parent (forked ok)
		print("Parent code run")
		if pipe:
			os.close(r)
			os.close(0)
			os.dup(w)

			execute(secondcmd)

		os.wait()
		os.write(2, ("Child is dead\n").encode())

	else: # child
		if pipe:
			os.close(w)
			os.close(1)
			os.dup(r)

		# handles redirections
		if isredirect(cmds):
			cmds = redirect(cmds)

		execute(cmds)

	if pipe:
		closepipe(r, w)

if __name__ == '__main__':
	main()
