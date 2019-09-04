import sys, os, json, subprocess, traceback
from excel2json import convert_from_file
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init()

if len(sys.argv) > 1:
    arg = sys.argv[1]

def log(event):
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    
    if os.path.isfile("logs\\Anti-Cheat.log") == True:
        file = open("logs\\Anti-Cheat.log", "a")
        if event == "NEW_SESSION":
            file.write("\n\n" + str(timestamp) + "  " + "NEW CHECKER MODULE SESSION STARTED\n")
        else:
            file.write(str(timestamp) + "  " + str(event) + "\n")
        file.close()
    else:
        file = open("logs\\Anti-Cheat.log", "w")
        if event == "NEW_SESSION":
            file.write(str(timestamp) + "  " + "NEW CHECKER MODULE SESSION STARTED\n")
        else:
            file.write(str(timestamp) + "  " + str(event) + "\n")
        file.close()

def log_traceback(event):
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    if os.path.isfile("logs\\Anti-Cheat_traceback.log") == True:
        file = open("logs\\Anti-Cheat_traceback.log", "a")
        file.write("=================================================================\n")
        file.write("Traceback at " + str(timestamp) + "\n" + event + "\n")
        file.write("=================================================================\n")
        file.close()
    else:
        file = open("logs\\Anti-Cheat_traceback.log", "w")
        file.write("Traceback at " + str(timestamp) + "\n" + event + "\n\n")
        file.close()

def excel2json():
    try:
        try:
            EXCEL_FILE = "lists\\cheaters.xlsx"
            convert_from_file(EXCEL_FILE)
            for filename in os.listdir("lists\\"):
                if filename.endswith(".json"):
                    os.rename("lists\\" + filename, "lists\\cheaters.json")
            print("[INFO] Cheaters Pokémon GO IDs list has been reset.")
            log("[INFO] Cheaters Pokémon GO IDs list has been reset.")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while resetting the cheaters Pokémon GO IDs list." + Style.RESET_ALL)
            log("[WARN] An error occured while resetting the cheaters Pokémon GO IDs list.")
            log("[ERRO] " + str(e))
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)

def show_config():
    try:
        json_file = open("scripts\\config.json")
        res = json.load(json_file)

        CLIENT_ID = res["CLIENT_ID"]
        CLIENT_SECRET = res["CLIENT_SECRET"]
        TOKEN = res["TOKEN"]
        HOST = res["HOST"]
        PORT = res["PORT"]
        REDIRECT_URL = res["REDIRECT_URL"]
        OAUTH_WINDOW = res["OAUTH_WINDOW"]
        CHECKER_WINDOW = res["CHECKER_WINDOW"]
        AUTOSTART = res["AUTOSTART"]

        print("=========================================================================================")
        print("                            Anti-Cheat current configuration                             ")
        print("=========================================================================================")
        print("                                   Functional settings                                   ")
        print("=========================================================================================")
        print(" CLIENT_ID:            " + CLIENT_ID)
        print(" CLIENT_SECRET:        " + CLIENT_SECRET)
        print(" TOKEN:                " + TOKEN)
        print(" HOST:                 " + HOST)
        print(" PORT:                 " + PORT)
        print(" REDIRECT_URL:         " + REDIRECT_URL)
        print(" AUTOSTART:            " + AUTOSTART)
        print("=========================================================================================")
        print("                                     Windows settings                                    ")
        print("=========================================================================================")
        print(" OAUTH_WINDOW:         " + OAUTH_WINDOW)
        print(" CHECKER_WINDOW:       " + CHECKER_WINDOW)
        print("=========================================================================================")
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)

def autostart_config(arg2):
    try:
        json_file = open("scripts\\config.json")
        res = json.load(json_file)

        CLIENT_ID = res["CLIENT_ID"]
        CLIENT_SECRET = res["CLIENT_SECRET"]
        TOKEN = res["TOKEN"]
        HOST = res["HOST"]
        PORT = res["PORT"]
        REDIRECT_URL = res["REDIRECT_URL"]
        OAUTH_WINDOW = res["OAUTH_WINDOW"]
        CHECKER_WINDOW = res["CHECKER_WINDOW"]
        AUTOSTART = res["AUTOSTART"]

        if arg2 == "start":
            if AUTOSTART == "0":
                log("[INFO] Autostart disabled. Resuming.")
                pass
            elif AUTOSTART == "1":
                print("[INFO] Autostart enabled. Starting Anti-Cheat.\n")
                log("[INFO] Autostart enabled. Starting Anti-Cheat.")
                startp = subprocess.Popen(args=["python", "scripts\\main.py", "scripts\\config.json"])
                startp.wait()
            else:
                print(Fore.RED + Style.BRIGHT + "[WARN] Incorrect autostart parameter." + Style.RESET_ALL)
                log("[WARN] Incorrect autostart parameter.")
        elif arg2 == "config":
            if AUTOSTART == "0":
                log("[INFO] Autostart disabled. Changing autostart parameter to 1.")
                print("[INFO] Autostart disabled. Changing autostart parameter to 1.")
                res = {
                      "CLIENT_ID" : CLIENT_ID,
                      "CLIENT_SECRET" : CLIENT_SECRET,
                      "TOKEN" : TOKEN,
                      "HOST" : HOST,
                      "PORT" : PORT,
                      "REDIRECT_URL" : REDIRECT_URL,
                      "OAUTH_WINDOW" : OAUTH_WINDOW,
                      "CHECKER_WINDOW": CHECKER_WINDOW,
                      "AUTOSTART": "1"
                      }
                json_file = open("scripts\\config.json", "w")
                json.dump(res, json_file, indent=4)
                json_file.close()
            elif AUTOSTART == "1":
                log("[INFO] Autostart enabled. Changing autostart parameter to 0.")
                print("[INFO] Autostart enabled. Changing autostart parameter to 0.")
                res = {
                      "CLIENT_ID" : CLIENT_ID,
                      "CLIENT_SECRET" : CLIENT_SECRET,
                      "TOKEN" : TOKEN,
                      "HOST" : HOST,
                      "PORT" : PORT,
                      "REDIRECT_URL" : REDIRECT_URL,
                      "OAUTH_WINDOW" : OAUTH_WINDOW,
                      "CHECKER_WINDOW": CHECKER_WINDOW,
                      "AUTOSTART": "0"
                      }
                json_file = open("scripts\\config.json", "w")
                json.dump(res, json_file, indent=4)
                json_file.close()
            else:
                print(Fore.RED + Style.BRIGHT + "[WARN] Incorrect autostart parameter." + Style.RESET_ALL)
                log("[WARN] Incorrect autostart parameter.")
        else:
            print(Fore.RED + Style.BRIGHT + "[WARN] Incorrect autostart parameter." + Style.RESET_ALL)
            log("[WARN] Incorrect autostart parameter.")
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)

def show_cheaters_pid():
    try:
        with open("lists\\cheaters.json") as json_file:
            data = json.load(json_file)
            for p in data:
                if p["Pseudo*"]:
                    print(p["Pseudo*"])
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)

def reset_json():
    try:
        res = {
              "CLIENT_ID" : "<CLIENT_ID>",
              "CLIENT_SECRET" : "<CLIENT_SECRET>",
              "TOKEN" : "<TOKEN>",
              "HOST" : "<HOST>",
              "PORT" : "<PORT>",
              "REDIRECT_URL" : "<REDIRECT_URL>",
              "OAUTH_WINDOW" : "SW_MINIMIZE",
              "CHECKER_WINDOW": "SW_MINIMIZE",
              "AUTOSTART": "0"
              }
        try:
            json_file = open("scripts\\config.json", "w")
            json.dump(res, json_file, indent=4)
            json_file.close()
            print("[INFO] Configuration file has been reset.")
            log("[INFO] Configuration file has been reset.")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "[WARN] An error occured while resetting the configuration file." + Style.RESET_ALL)
            log("[WARN] An error occured while resetting the configuration file.")
            log("[ERRO] " + str(e))
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)

def set(var):
    try:
        val = input("Value for " + var + ": ")
        
        json_file = open("scripts\\config.json", "r")
        res = json.load(json_file)
        res[var] = val
        json_file.close()
        
        json_file = open("scripts\\config.json", "w")
        json.dump(res, json_file, indent=4)
        json_file.close()
    except KeyboardInterrupt:
        return
    except Exception as e:
        log(e)
        log_traceback(traceback.format_exc())
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)

def contact():
    print("==============================================")
    print("|                SH4FS0c13ty                 |")
    print("==============================================")
    print("|                                            |")
    print("| Discord:    SH4FS0c13ty#1562               |")
    print("| Twitter:    @SH4FS0c13ty                   |")
    print("| Github:     https://github.com/SH4FS0c13ty |")
    print("| Website:    https://sh4fs0c13ty.tk/        |")
    print("|                                            |")
    print("| Other projects:                            |")
    print("|                                            |")
    print("|  - TigerXDragon (Toradora! Portable        |")
    print("|                  Translation Toolkit)      |")
    print("|                                            |")
    print("|  - Toradora! FR (Toradora! Portable        |")
    print("|                  Translation project       |")
    print("|                  https://toradora-fr.tk)   |")
    print("|                                            |")
    print("==============================================")

if arg == "show_config":
    show_config()

if arg == "show_cheaters_pid":
    show_cheaters_pid()

if arg == "reset_json":
    reset_json()

if arg == "set":
    arg2 = sys.argv[2]
    set(arg2)

if arg == "contact":
    contact()

if arg == "autostart":
    arg2 = sys.argv[2]
    autostart_config(arg2)
