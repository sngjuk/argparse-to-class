#!/usr/bin/env python

from subprocess import call

def run_server():
        call(["chmod", "777", "../arg2cls_v0.8.py"])
        call(["chmod", "777", "action_page.php"])
	call(["php","-S","0:8000"])


if __name__ == "__main__":
	run_server()
