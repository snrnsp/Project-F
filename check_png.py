import struct

def get_image_info(filepath):
    with open(filepath, 'rb') as f:
        head = f.read(24)
        if len(head) != 24: return None
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            check = struct.unpack('>i', head[8:12])[0]
            if head[12:16] == b'IHDR':
                width, height = struct.unpack('>ii', head[16:24])
                return width, height
    return None

print(get_image_info('F:/Project-F/Assets/Resources/Images/bg_lobby.png'))
