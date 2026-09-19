#!/usr/bin/env python3
"""Robust daemon launcher: double-fork + setsid so the child survives the
tool harness exiting. stdio -> logfile.

Usage: python3 daemon_run.py <logfile> <command> [args...]
Returns immediately. Child PID written to <logfile>.pid
"""
import os
import sys


def main():
    log = sys.argv[1]
    cmd = sys.argv[2:]

    if os.fork() > 0:
        os._exit(0)          # parent exits immediately
    os.setsid()              # new session, detached from controlling tty
    if os.fork() > 0:
        os._exit(0)          # middle process exits; grandchild is daemon

    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    devnull = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull, 0)

    with open(log + ".pid", "w") as f:
        f.write(str(os.getpid()) + "\n")

    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    main()
