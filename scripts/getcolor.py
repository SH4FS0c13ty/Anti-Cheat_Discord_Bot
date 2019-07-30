from PIL import Image

def main_color(image):
    im = Image.open(image)
    width, height = im.size
    x = 5
    y = height/2

    pix = im.load()
    color = pix[x,y]

    r = color[0]
    g = color[1]
    b = color[2]
    main_color = None

    if r >= g and r >= b:
        if g >= b:
            main_color = "Instinct"
        else:
            main_color = "Valor"
    else:
        main_color = "Mystic"
    
    return main_color