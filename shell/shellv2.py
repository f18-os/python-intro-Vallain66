#! /usr/bin/env python3

import os, sys, re

PS1 = "$ "
STDIN = 0
STDOUT = 1

def main():
	os.write(1, ("Type exit to quit\n").encode())
	while(True):
		# prompt user input
		uinput = input(PS1)
		if not uinput:       # empty input
			continue
		if prompt(uinput):   # changing prompt
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
	os.write(2, ("Executing %s\n" % cmds).encode())
	for dir in re.split(":", os.environ['PATH']): # try each directory in path
		program = "%s/%s" % (dir, cmds[0])
		try:
			os.execve(program, cmds, os.environ) # try to exec program
		except FileNotFoundError:             # ...expected
			pass                              # ...fail quietly

	os.write(2, ("Error: Could not exec %s\n" % cmds[0]).encode())
	sys.exit(1)								  # terminate with error

def ispipe(tasks):
	return len(tasks) > 1

def closepipe(r, w):
	for fd in (r, w):
		os.close(fd)

def gettasks(uinput):
	tasks = []
	for task in re.split("\|", uinput):
		tasks.append(task.split())
	return tasks

def handle(uinput):
	# process input into separate tasks
	tasks = gettasks(uinput)
	# is a pipe required
	pipe = ispipe(tasks)

	children = int(len(tasks))

	for i in range(children):
		if len(tasks) > 0:
			task = tasks.pop(0)
		print("task: ", i+1, task)
		if pipe:
			pipein, pipeout = os.pipe()
			for fd in (pipein, pipeout):
				os.set_inheritable(fd, True)
		rc = os.fork()

		if rc < 0:
		    os.write(2, ("fork failed, returning %d\n" % rc).encode())
		    sys.exit(1)

		elif rc == 0: # CHILD
			# determine is a pipe is necessary
			if pipe:
				os.close(pipein)
				os.dup2(pipeout, STDOUT)

			if isredirect(task):
				task = redirect(task)

			execute(task)
		else:		# PARENT
			if pipe:
				os.close(pipeout)
				os.dup2(pipein, STDIN)
			os.wait()
	#if pipe:
	#	closepipe(pipein, pipeout)

if __name__ == '__main__':
	main()
