import subprocess, sys, check

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]

DETACHED_PROCESS = 0x00000008

pid = subprocess.Popen(['python', "oauth.py", arg1, arg2],
                       creationflags=DETACHED_PROCESS).pid

check.start(arg3)