from PIL import Image
import os
import glob

brain_dir = "/Users/admin/.gemini/antigravity-ide/brain/1c8288cf-b19c-4615-9cdf-99047682d019"
png_files = glob.glob(os.path.join(brain_dir, "*.png"))

for path in png_files:
    f = os.path.basename(path)
    try:
        im = Image.open(path)
        print(f"{f}: format={im.format}, size={im.size}, mode={im.mode}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
