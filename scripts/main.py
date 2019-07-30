import subprocess, sys, json

arg = sys.argv[1]

NEW_CONSOLE = 0x00000010

json_file = open(arg)
res = json.load(json_file)

CLIENT_ID = res["CLIENT_ID"]
CLIENT_SECRET = res["CLIENT_SECRET"]
TOKEN = res["TOKEN"]
HOST = res["HOST"]
PORT = res["PORT"]
REDIRECT_URL = res["REDIRECT_URL"]

print("Starting Anti-Cheat with the following settings ...")
print("=========================================================================================")
print("CLIENT_ID:            " + CLIENT_ID)
print("CLIENT_SECRET:        " + CLIENT_SECRET)
print("TOKEN:                " + TOKEN)
print("HOST:                 " + HOST)
print("PORT:                 " + PORT)
print("REDIRECT_URL:         " + REDIRECT_URL)
print("=========================================================================================\n")

SW_MINIMIZE = 6
info = subprocess.STARTUPINFO()
info.dwFlags = subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = SW_MINIMIZE

pid = subprocess.Popen(args=["python", "scripts\\oauth.py", CLIENT_ID, CLIENT_SECRET, HOST, PORT, REDIRECT_URL], creationflags=NEW_CONSOLE, startupinfo=info).pid
print("Anti-Cheat OAauth2 module started with PID " + str(pid) + " with minimized console.")

f = open("scripts\\oauth_pid.txt", "w")
f.write(str(pid))
f.close()

pid2 = subprocess.Popen(args=["python", "scripts\\check.py", TOKEN], creationflags=NEW_CONSOLE, startupinfo=info).pid
print("Anti-Cheat Checker module started with PID " + str(pid2) + " with minimized console.")

f = open("scripts\\check_pid.txt", "w")
f.write(str(pid2))
f.close()
