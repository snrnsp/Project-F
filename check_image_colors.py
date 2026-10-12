from PIL import Image

path = 'F:/Project-F/Assets/Resources/Images/Logos/LOST_STUDIO_Logo.png'
with Image.open(path) as img:
    img = img.convert('RGBA')
    width, height = img.size
    
    # Check pixels in the bottom half where text usually is
    bottom_half = img.crop((0, height//2, width, height))
    
    has_black = False
    has_white = False
    has_color = False
    
    for count, (r, g, b, a) in bottom_half.getcolors(maxcolors=100000) or []:
        if a > 10: # Only look at visible pixels
            if r < 50 and g < 50 and b < 50:
                has_black = True
            elif r > 200 and g > 200 and b > 200:
                has_white = True
            else:
                has_color = True

    print(f"Bottom half analysis - Black: {has_black}, White: {has_white}, Color: {has_color}")
