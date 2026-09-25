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
            img = Image.open(f).convert("RGBA")
            datas = img.getdata()
            
            newData = []
            for item in datas:
                r, g, b, a = item[0], item[1], item[2], item[3]
                
                # Calculate lightness (0 to 255)
                lightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # Opacity is inverted lightness (black = 255 alpha, white = 0 alpha)
                alpha = 255 - lightness
                
                # Factor in any existing alpha
                alpha = min(alpha, a)
                
                # Make the shape solid black (0,0,0) with calculated transparency
                newData.append((0, 0, 0, alpha))
                
            img.putdata(newData)
            img.save(f, "PNG")
            print(f"Successfully processed {f} into a transparent stencil icon.")
        except Exception as e:
            print(f"Error processing {f}: {e}")
    else:
        print(f"File {f} does not exist.")
