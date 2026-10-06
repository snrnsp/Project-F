import os
import struct

def get_png_size(file_path):
    with open(file_path, 'rb') as f:
        data = f.read(24)
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            w, h = struct.unpack('>II', data[16:24])
            return w, h
    return 0, 0

chars_dir = 'Assets/Resources/Characters'
for char in os.listdir(chars_dir):
    char_path = os.path.join(chars_dir, char)
    if os.path.isdir(char_path):
        for img in os.listdir(char_path):
            if img.endswith('.png'):
                w, h = get_png_size(os.path.join(char_path, img))
                print(f"{char}: {w}x{h}")
                break
