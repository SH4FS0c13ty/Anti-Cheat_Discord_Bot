import subprocess, sys, check

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]

NEW_CONSOLE = 0x00000010

pid = subprocess.Popen(args=["python", "oauth.py", arg1, arg2], creationflags=NEW_CONSOLE).pid

print("Discord OAauth2 module started with PID " + str(pid) + "\n")

check.start(arg3)