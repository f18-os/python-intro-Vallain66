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


def execute(cmd):
	for dir in re.split(":", os.environ['PATH']): # try each directory in path
		program = "%s/%s" % (dir, cmd[0])
		try:
			os.execve(program, cmd, os.environ) # try to exec program
		except FileNotFoundError:             # ...expected
			pass                              # ...fail quietly

	os.write(2, ("Error: Could not exec %s\n" % cmd[0]).encode())
	sys.exit(1)								  # terminate with error


def ispipe(tasks):
	return len(tasks) > 1


def closepipe(r, w):
	os.close(r)
	os.close(w)


def gettasks(uinput):
	tasks = []
	for task in re.split("\|", uinput):
		tasks.append(task.split())
	return tasks
	

def handle(uinput):
	tasks = gettasks(uinput)

	pipe = ispipe(tasks)
	if pipe:
		pipein, pipeout = os.pipe()
		for fd in (pipein, pipeout):
			os.set_inheritable(fd, True)

	rc = os.fork()

	if rc < 0:
	    os.write(2, ("fork failed, returning %d\n" % rc).encode())
	    sys.exit(1)

	elif rc:        # parent (forked ok)
		if pipe:
			os.close(pipeout)
			os.dup2(pipein, STDIN)
			execute(tasks[1])

		os.wait()

	else: # child
		if pipe:
			os.close(pipein)
			os.dup2(pipeout, STDOUT)

		# handles redirections
		if isredirect(tasks[0]):
			tasks[0] = redirect(tasks[0])

		execute(tasks[0])

	if pipe:
		closepipe(r, w)

if __name__ == '__main__':
	main()
