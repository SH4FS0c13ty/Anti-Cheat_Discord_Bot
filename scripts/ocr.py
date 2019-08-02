import pytesseract, os
from PIL import Image

def getid(file, userid):
    ocr_result = ocr_core(file)
    if ocr_result.find("&") != -1:
        pokeid = text_process(ocr_result, userid)
    else:
        pokeid = "ERROR"
    os.remove(file)
    return pokeid

def ocr_core(filename):
    print("[INFO] " + "Processing OCR ...")
    text = pytesseract.image_to_string(Image.open(filename), lang="ita", config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789&")
    return text

def text_process(text, userid):
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

    sep = "\n"
    rest = lastl.split(sep, 1)[0]

    file=open("user_ids\\" + userid + ".txt", "w")
    file.write(rest)
    file.close()

    print("[INFO] " + "OCR Result: " + rest)
    return rest
