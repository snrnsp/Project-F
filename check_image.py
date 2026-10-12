from PIL import Image

path = 'F:/Project-F/Assets/Resources/Images/Logos/LOST_STUDIO_Logo.png'
try:
    with Image.open(path) as img:
        print(f"Format: {img.format}")
        print(f"Size: {img.size}")
        print(f"Mode: {img.mode}")
except Exception as e:
    print(f"Error: {e}")
