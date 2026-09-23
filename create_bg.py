import os
import struct
import zlib

def create_png(width, height, r, g, b, filename):
    # 1 pixel png
    # IHDR
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_chunk = b'IHDR' + ihdr
    ihdr_crc = zlib.crc32(ihdr_chunk) & 0xffffffff
    
    # IDAT
    # Uncompressed data: filter byte (0) + RGB
    raw_data = b'\x00' + struct.pack('BBB', r, g, b)
    compressed = zlib.compress(raw_data)
    idat_chunk = b'IDAT' + compressed
    idat_crc = zlib.crc32(idat_chunk) & 0xffffffff
    
    # IEND
    iend_chunk = b'IEND'
    iend_crc = zlib.crc32(iend_chunk) & 0xffffffff
    
    with open(filename, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        
        f.write(struct.pack('>I', len(ihdr)))
        f.write(ihdr_chunk)
        f.write(struct.pack('>I', ihdr_crc))
        
        f.write(struct.pack('>I', len(compressed)))
        f.write(idat_chunk)
        f.write(struct.pack('>I', idat_crc))
        
        f.write(struct.pack('>I', 0))
        f.write(iend_chunk)
        f.write(struct.pack('>I', iend_crc))

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Images/bg_flashback.png'
create_png(1, 1, 25, 12, 40, path)
print('Created bg_flashback.png')
