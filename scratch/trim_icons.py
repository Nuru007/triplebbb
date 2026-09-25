from PIL import Image
import os

files = [
    "assets/images/icon_beauty.png",
    "assets/images/icon_brain.png",
    "assets/images/icon_balance.png"
]

for f in files:
    if os.path.exists(f):
        try:
            img = Image.open(f)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            datas = img.getdata()
            
            width, height = img.size
            min_x, min_y = width, height
            max_x, max_y = 0, 0
            
            found = False
            for y in range(height):
                for x in range(width):
                    alpha = datas[y * width + x][3]
                    if alpha > 0:
                        found = True
                        if x < min_x: min_x = x
                        if y < min_y: min_y = y
                        if x > max_x: max_x = x
                        if y > max_y: max_y = y
                        
            if found:
                # Add a small padding to prevent edge cutting
                padding = 8
                min_x = max(0, min_x - padding)
                min_y = max(0, min_y - padding)
                max_x = min(width, max_x + padding)
                max_y = min(height, max_y + padding)
                
                cropped_img = img.crop((min_x, min_y, max_x, max_y))
                cropped_img.save(f, "PNG")
                print(f"Trimmed transparent padding from {f} successfully.")
            else:
                print(f"{f} is fully transparent.")
        except Exception as e:
            print(f"Error trimming {f}: {e}")
    else:
        print(f"File {f} does not exist.")
