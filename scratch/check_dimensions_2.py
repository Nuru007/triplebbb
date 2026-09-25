from PIL import Image
import os

files = [
    "media__1783271711508.png",
    "media__1783271844050.png"
]

for f in files:
    path = os.path.join("/Users/admin/.gemini/antigravity-ide/brain/1c8288cf-b19c-4615-9cdf-99047682d019", f)
    if os.path.exists(path):
        try:
            im = Image.open(path)
            print(f"{f}: format={im.format}, size={im.size}, mode={im.mode}")
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"{f} does not exist")
