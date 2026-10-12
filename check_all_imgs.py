from PIL import Image
import os
import glob

chars_dir = 'F:/Project-F/Assets/Resources/Characters'
for char_name in os.listdir(chars_dir):
    char_path = os.path.join(chars_dir, char_name)
    if os.path.isdir(char_path):
        # find the first png
        pngs = glob.glob(os.path.join(char_path, '*.png'))
        if pngs:
            try:
                with Image.open(pngs[0]) as img:
                    bbox = img.getbbox()
                    w, h = img.size
                    center_x = w / 2
                    bbox_center_x = (bbox[0] + bbox[2]) / 2 if bbox else center_x
                    shift_percent = (bbox_center_x - center_x) / w
                    print(f"{char_name}: shift = {shift_percent*100:.1f}%")
            except Exception as e:
                pass
