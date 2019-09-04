import pytesseract, os, sys, traceback
import tools
from PIL import Image
import colorama
from colorama import Fore, Style

colorama.init()

def getid(file, userid):
    try:
        global filename
        filename = file
        ocr_result = ocr_core(file)
        if ocr_result.find("&") != -1:
            pokeid = text_process(ocr_result, userid)
        elif ocr_result.find("PROGRESDELASEMAINE") != -1:
            pokeid = text_processfr(ocr_result, userid, 1)
        elif ocr_result.find("PROGRSDELASEMAINE") != -1:
            pokeid = text_processfr(ocr_result, userid, 2)
        else:
            pokeid = "ERROR"
        os.remove(file)
        return pokeid
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def ocr_core(filename):
    try:
        print("[INFO] " + "Processing OCR ...")
        tools.log("[INFO] " + "Processing OCR ...")
        text = pytesseract.image_to_string(Image.open(filename), lang="ita", config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789&")
        return text
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())

def text_process(text, userid):
    try:
        sep = "&"
        rest = text.split(sep, 1)[0]

        file=open("user_ids\\" + userid + ".txt", "w")
        file.write(rest)
        file.close()

        file = open("user_ids\\" + userid + ".txt", "r")
        lastl = list(file)[-1]
        file.close()

        file = open("user_ids\\" + userid + ".txt", "w")
        file.write(lastl)
        file.close()
        
        file = open("user_ids\\" + userid + ".txt", "r")
        lines = file.read().splitlines()
        file.close()
        
        last_line = lastl

        if "\n" in last_line:
            sep = "\n"
            last_line = last_line.split(sep, 1)[0]
        else:
            pass

        if " " in last_line:
            tools.log("[INFO] " + "OCR Result: " + last_line)
            print(Fore.RED + Style.BRIGHT + "[WARN] Found space in detected username. The following procedures could lead to errors." + Style.RESET_ALL)
            tools.log("[WARN] Found space in detected username. The following procedures could lead to errors.")
            last_line = fallback(userid, 2)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(last_line)
            file.close()
        else:
            print("[INFO] " + "OCR Result: " + last_line)
            tools.log("[INFO] " + "OCR Result: " + last_line)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(last_line)
            file.close()
        return last_line
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        return "ERROR"

def text_processfr(text, userid, idsep):
    try:
        if idsep == 1:
            sep = "PROGRESDELASEMAINE"
        if idsep == 2:
            sep = "PROGRSDELASEMAINE"
        
        rest = text.split(sep, 1)[0]
        
        file=open("user_ids\\" + userid + ".txt", "w")
        file.write(rest)
        file.close()
        
        file = open("user_ids\\" + userid + ".txt", "r")
        lines = file.read().splitlines()
        last_line = lines[-1]
        file.close()
        
        while last_line.find("et") == -1:
            lines = lines[:-1]
            last_line = lines[-1]
        
        lines = lines[:-1]
        last_line = lines[-1]

        if last_line != "":
            pass
        else:
            lines = lines[:-1]
            last_line = lines[-1]
        
        if " " in last_line:
            tools.log("[INFO] " + "OCR Result: " + last_line)
            print(Fore.RED + Style.BRIGHT + "[WARN] Found space in detected username. The following procedures could lead to errors." + Style.RESET_ALL)
            tools.log("[WARN] Found space in detected username. The following procedures could lead to errors.")
            last_line = fallback(userid, 1)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(last_line)
            file.close()
        else:
            print("[INFO] " + "OCR Result: " + last_line)
            tools.log("[INFO] " + "OCR Result: " + last_line)
            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()
        return last_line
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        return "ERROR"

def fallback(userid, method):
    try:
        global filename
        print("[INFO] Using fallback function to detect username.")
        tools.log("[INFO] Using fallback function to detect username.")

        text = os.popen("tesseract -l ita " + filename + " stdout quiet").read()
        
        if method == 1:
            sep = "PROGRÃˆS DE LA SEMAINE"
            rest = text.split(sep, 1)[0]

            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()

            file = open("user_ids\\" + userid + ".txt", "r")
            lines = file.read().splitlines()
            last_line = lines[-1]

            while last_line.find("et") == -1:
                lines = lines[:-1]
                last_line = lines[-1]

            lines = lines[:-1]
            last_line = lines[-1]

            if last_line != "":
                pass
            else:
                lines = lines[:-1]
                last_line = lines[-1]

            if " " in last_line:
                sep = " "
                rest = last_line.split(sep, 1)[0]

            print("[INFO] " + "Fallback OCR Result: " + rest)
            tools.log("[INFO] " + "Fallback OCR Result: " + rest)
            return rest
        elif method == 2:
            sep = "&"
            rest = text.split(sep, 1)[0]

            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()

            file = open("user_ids\\" + userid + ".txt", "r")
            lastl = list(file)[-1]
            file.close()

            file = open("user_ids\\" + userid + ".txt", "w")
            file.write(lastl)
            file.close()
            
            file = open("user_ids\\" + userid + ".txt", "r")
            lines = file.read().splitlines()
            file.close()

            last_line = lastl

            if "\n" in last_line:
                sep = "\n"
                last_line = last_line.split(sep, 1)[0]
            else:
                pass

            if " " in last_line:
                sep = " "
                rest = last_line.split(sep, 1)[0]

            file=open("user_ids\\" + userid + ".txt", "w")
            file.write(rest)
            file.close()

            print("[INFO] " + "Fallback OCR Result: " + rest)
            tools.log("[INFO] " + "Fallback OCR Result: " + rest)
            return rest
        else:
            print(Fore.RED + Style.BRIGHT + "[WARN] Wrong fallback method. Aborting." + Style.RESET_ALL)
            tools.log("[WARN] Wrong fallback method. Aborting.")
            return "ERROR"
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[WARN] An unknown error occured. Please check the Anti-Cheat.log and Anti-Cheat_traceback.log files to know more." + Style.RESET_ALL)
        tools.log("[ERRO] " + str(e))
        tools.log_traceback(traceback.format_exc())
        return "ERROR"
