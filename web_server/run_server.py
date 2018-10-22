#!/usr/bin/env python

from subprocess import call

def run_server():

	call(["php","-S","0:8000"])


if __name__ == "__main__":
	run_server()
