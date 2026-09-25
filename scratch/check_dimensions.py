from PIL import Image
import os

files = [
    "temp_1188.png",
    "temp_1345.png",
    "temp_1524.png",
    "temp_2395.png"
]

for f in files:
    path = os.path.join("assets/images", f)
    if os.path.exists(path):
        try:
            im = Image.open(path)
            print(f"{f}: format={im.format}, size={im.size}, mode={im.mode}")
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"{f} does not exist")
