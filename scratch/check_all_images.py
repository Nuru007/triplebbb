import os
from PIL import Image

image_dir = "assets/images"
for f in sorted(os.listdir(image_dir)):
    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(image_dir, f)
        try:
            im = Image.open(path)
            print(f"{f}: format={im.format}, size={im.size}, mode={im.mode}")
        except Exception as e:
            print(f"Error reading {f}: {e}")
