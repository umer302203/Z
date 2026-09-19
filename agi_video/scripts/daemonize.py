#!/usr/bin/env python3
"""daemonize.py — double-fork launcher. Survives the Bash tool's descendant cleanup.
Usage: python3 daemonize.py <logfile> <cmd> [args...]
"""
import os, sys

def daemonize():
    if os.fork() > 0:
        os._exit(0)          # parent exits
    os.setsid()              # new session, no controlling tty
    if os.fork() > 0:
        os._exit(0)          # intermediate exits -> PPID=1

def main():
    logfile, cmd = sys.argv[1], sys.argv[2:]
    daemonize()
    os.chdir("/")
    fd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 0)
    os.execvp(cmd[0], cmd)

main()
