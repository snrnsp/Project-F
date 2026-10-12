import sys

try:
    from PIL import Image
    img = Image.open('F:/Project-F/Assets/Resources/Images/bg_lobby.png')
    img = img.convert('RGBA')
    width, height = img.size
    
    # Check rightmost 10 columns
    for x in range(width - 10, width):
        is_empty = True
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if a > 0 and (r > 5 or g > 5 or b > 5):
                is_empty = False
                break
        print(f"Col {x}: empty/black? {is_empty}")
except Exception as e:
    print(e)
