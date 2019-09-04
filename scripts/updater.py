import itertools, threading, time, sys, subprocess, json, os, traceback
import tools, colorama, hashlib
from colorama import Fore, Style
import shutil
from shutil import copyfile

colorama.init()
arg = sys.argv[1]

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def updating():
    global done
    for c in itertools.cycle(['.  ', '.. ', '...']):
        if done:
            break
        sys.stdout.write('\rUpdating Anti-Cheat ' + c)
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\rUpdating Anti-Cheat ...\n')

def update(url):
    try:
        global done
        global new_checksum
        done = False

        t = threading.Thread(target=updating)
        t.start()

        tools.log("[INFO] Downloading new Anti-Cheat version at " + url)
        dl = subprocess.Popen(args=["setup\\curl.exe", "-s", "-f", "-k", "--output", "Anti-Cheat_EN.zip", url])
        dl.wait()
        
        if sha256sum("Anti-Cheat_EN.zip").lower() == new_checksum.lower():
            tools.log("[INFO] Checksum verified for Anti-Cheat_EN.zip: " + new_checksum)
            tools.log("[INFO] Extracting Anti-Cheat_EN.zip archive ...")
            extract = subprocess.Popen(args=["setup\\7z.exe", "x", "Anti-Cheat_EN.zip", "-bb3", "-r"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            extract.wait()
            dir = os.getcwd()
            tools.log("[INFO] Removing new default config.json file.")
            os.remove(dir + "\\Anti-Cheat_Discord_Bot-master\\scripts\\config.json")
            tools.log("[INFO] Copying new folder: Anti-Cheat_Discord_Bot-master/licenses.")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master\\licenses"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir + "\\licenses")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\licenses")
            tools.log("[INFO] Removed new folder: Anti-Cheat_Discord_Bot-master/licenses.")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\lists")
            tools.log("[INFO] Removed new folder: Anti-Cheat_Discord_Bot-master/lists.")
            tools.log("[INFO] Copying new folder: Anti-Cheat_Discord_Bot-master/scripts.")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master\\scripts"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir + "\\scripts")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\scripts")
            tools.log("[INFO] Removed new folder: Anti-Cheat_Discord_Bot-master/scripts.")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\servers_lists")
            tools.log("[INFO] Removed new folder: Anti-Cheat_Discord_Bot-master/servers_lists.")
            tools.log("[INFO] Copying new folder: Anti-Cheat_Discord_Bot-master/setup.")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master\\setup"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir + "\\setup")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\setup")
            tools.log("[INFO] Removed new folder: Anti-Cheat_Discord_Bot-master/setup.")
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master\\user_ids")
            tools.log("[INFO] Removed new folder: Anti-Cheat_Discord_Bot-master/user_ids.")
            tools.log("[INFO] Copying new folder: Anti-Cheat_Discord_Bot-master/")
            for root, dirs, files in os.walk(dir + "\\Anti-Cheat_Discord_Bot-master"):
                for file in files:
                    path_file = os.path.join(root,file)
                    shutil.copy2(path_file, dir)
            shutil.rmtree(dir + "\\Anti-Cheat_Discord_Bot-master")
            tools.log("[INFO] Removed new folder: Anti-Cheat_Discord_Bot-master/")
            tools.log("[INFO] Installing new Python requirements ...")
            pysetup = subprocess.Popen(args=["python", "-m", "pip", "-r", "setup\\requirements.txt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            pysetup.wait()
            tools.log("[INFO] Anti-Cheat has been updated.")
            print("[INFO] Anti-Cheat has been updated.\n\nPlease close this window without using the exit command and restart the Anti-Cheat main console.")
            while True:
                time.sleep(1)
        else:
            done = True
            time.sleep(0.5)
            print(Fore.RED + Style.BRIGHT + "[WARN] Incorrect checksum. File may me corrupted or altered." + Style.RESET_ALL)
            print("[INFO] Aborting update.")
            tools.log("[WARN] Incorrect checksum. File may me corrupted or altered.")
            tools.log("[INFO] Aborting update.")
        os.remove("Anti-Cheat_EN.zip")
        time.sleep(1)
        done = True
    except KeyboardInterrupt:
        done = True
        os.remove("updates.json")
        return
    except Exception as e:
        done = True
        time.sleep(0.5)
        print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while updating. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[WARN] An error occured while updating.")
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())


def check_updates(command):
    try:
        name = "Anti-Cheat EN"
        version = "v1.4.0"
        date = "04/09/19"

        print("Checking for updates ...")
        tools.log("[INFO] Checking for updates ...")
        check = subprocess.Popen(args=["setup\\curl.exe", "-s", "-f", "-k", "--output", "updates.json", "https://sh4fs0c13ty.tk/updates/updates.json"])
        check.wait()
        with open("updates.json") as json_file:
            data = json.load(json_file)
            for p in data:
                if "Anti-Cheat EN" == p['App']:
                    new_version = p['Version']
                    new_codename = p['Codename']
                    new_url = p['Link']
                    new_date = p['Release date']
                    global new_checksum
                    new_checksum = p['Checksum']
            if version < new_version:
                if date < new_date:
                    if command == "update":
                        update(new_url)
                    elif command == "check":
                        print("A new update is available: Anti-Cheat " + new_version + " (" + new_codename + ") released on " + new_date + ".")
                        print("Please use the \"update\" command to update to the new version.")
                        tools.log("[INFO] A new update is available: Anti-Cheat " + new_version + " (" + new_codename + ") released on " + new_date + ".")
                else:
                    print("You already have the latest version of Anti-Cheat!")
                    tools.log("[INFO] No new version available.")
            else:
                print("You already have the latest version of Anti-Cheat!")
                tools.log("[INFO] No new version available.")
    except KeyboardInterrupt:
        os.remove("updates.json")
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while checking for updates. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[WARN] An error occured while checking for updates.")
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        os.remove("updates.json")

if arg == "update":
    check_updates(arg)
elif arg == "check":
    check_updates(arg)
else:
    print("Invalid argument.")
    
os.remove("updates.json")