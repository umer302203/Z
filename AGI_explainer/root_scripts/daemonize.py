#!/usr/bin/env python3
"""daemonize.py — double-fork daemon launcher (survives tool-call-end cleanup).
Usage: python3 daemonize.py <logfile> <cmd> [args...]
Child reparents to PID 1 (PPID=1 proves survival across Bash tool calls)."""
import os, sys

def daemonize():
    if os.fork() > 0:
        os._exit(0)          # parent exits -> child reparents to init
    os.setsid()              # new session, detach tty
    if os.fork() > 0:
        os._exit(0)          # daemon = grandchild, child of PID 1
    os.chdir("/")
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 0)      # stdin <- /dev/null

def main():
    if len(sys.argv) < 3:
        print("usage: daemonize.py <logfile> <cmd> [args...]"); sys.exit(1)
    logfile, cmd = sys.argv[1], sys.argv[2:]
    daemonize()
    fd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    os.execvp(cmd[0], cmd)

if __name__ == "__main__":
    main()
