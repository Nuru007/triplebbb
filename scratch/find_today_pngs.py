import os
import glob
import datetime

root_dir = "/Users/admin/.gemini/antigravity-ide/"
all_pngs = glob.glob(os.path.join(root_dir, "**/*.png"), recursive=True)

print(f"Found {len(all_pngs)} PNG files in total.")
today = datetime.date.today()

for path in all_pngs:
    mtime = os.path.getmtime(path)
    dt = datetime.datetime.fromtimestamp(mtime)
    if dt.date() == today:
        print(f"{path}: size={os.path.getsize(path)}, mtime={dt}")
