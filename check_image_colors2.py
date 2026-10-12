from PIL import Image

path = 'F:/Project-F/Assets/Resources/Images/Logos/LOST_STUDIO_Logo.png'
with Image.open(path) as img:
    img = img.convert('RGBA')
    width, height = img.size
    
    # Check pixels in the bottom half where text usually is
    bottom_half = img.crop((0, height//2, width, height))
    
    colors = sorted([c for c in bottom_half.getcolors(maxcolors=1000000) if c[1][3] > 10], key=lambda x: x[0], reverse=True)
    for i in range(min(5, len(colors))):
        print(f"Count: {colors[i][0]}, Color: {colors[i][1]}")
