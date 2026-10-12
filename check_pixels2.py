import sys

try:
    from PIL import Image
    img = Image.open('F:/Project-F/Assets/Resources/Images/bg_lobby.png')
    img = img.convert('RGBA')
    width, height = img.size
    
    # Check rightmost column (1919)
    black_pixels = 0
    transparent_pixels = 0
    for y in range(height):
        r, g, b, a = img.getpixel((width - 1, y))
        if a == 0:
            transparent_pixels += 1
        elif r < 10 and g < 10 and b < 10:
            black_pixels += 1
            
    print(f"Rightmost column: {transparent_pixels} transparent, {black_pixels} black out of {height}")
except Exception as e:
    print(e)
