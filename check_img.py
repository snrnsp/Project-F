from PIL import Image
import os

files = [
    'F:/Project-F/Assets/Resources/Characters/카스미/찡그림.png',
    'F:/Project-F/Assets/Resources/Characters/하루카/웃음.png'
]

for f in files:
    try:
        with Image.open(f) as img:
            bbox = img.getbbox()
            print(f"{os.path.basename(f)}: size={img.size}, bbox={bbox}")
            # Center of the image is size[0]/2
            # Center of the bounding box is (bbox[0] + bbox[2])/2
            img_center = img.size[0] / 2
            bbox_center = (bbox[0] + bbox[2]) / 2
            print(f"  Image Center X: {img_center}")
            print(f"  Visible BBox Center X: {bbox_center}")
            print(f"  Shift: {bbox_center - img_center} pixels")
    except Exception as e:
        print(f"Error reading {f}: {e}")
