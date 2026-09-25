import os
from PIL import Image, ImageDraw, ImageOps

IMAGE_DIR = "assets/images"
OUTPUT_DIR = "assets/images"

# Exact coordinates detected by macOS CoreImage CIDetector
# Center coordinates (x, y) and custom crop radius (adjusted to get head & shoulders)
CROPS = [
    # 1. Founder face from story_founder.jpg
    {"file": "story_founder.jpg", "cx": 320, "cy": 310, "r": 90},
    
    # 2. Speaker face from about_speaker.jpg (Face 1)
    {"file": "about_speaker.jpg", "cx": 267, "cy": 766, "r": 130},
    
    # 3. Main speaker face from hero_speaker.jpg
    {"file": "hero_speaker.jpg", "cx": 214, "cy": 237, "r": 125},
    
    # 4. Student face from hero_leadership.png (Face 2)
    {"file": "hero_leadership.png", "cx": 336, "cy": 364, "r": 130},
    
    # 5. Mentee/Student face from hero_mentorship.png (Face 1)
    {"file": "hero_mentorship.png", "cx": 355, "cy": 493, "r": 150},
    
    # 6. Mentor face from hero_mentorship.png (Face 2)
    {"file": "hero_mentorship.png", "cx": 733, "cy": 489, "r": 140},
    
    # 7. Student face from about_gesture.jpg
    {"file": "about_gesture.jpg", "cx": 444, "cy": 482, "r": 160},
    
    # 8. Another leader face from hero_leadership.png (Face 1)
    {"file": "hero_leadership.png", "cx": 678, "cy": 545, "r": 135}
]

def crop_to_circle(img_pil):
    """Crops a PIL image into a circle with a transparent background."""
    img_pil = img_pil.convert("RGBA")
    size = img_pil.size
    
    # Create circular mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    
    output = ImageOps.fit(img_pil, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

def run_precise_crops():
    print("Generating high-accuracy face crops using Pillow...")
    face_count = 0
    
    for idx, crop in enumerate(CROPS):
        filename = crop["file"]
        img_path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            continue
            
        try:
            im = Image.open(img_path)
            width, height = im.size
            
            cx = crop["cx"]
            cy = crop["cy"]
            r = crop["r"]
            
            # Check crop bounds and constrain to image boundaries
            x1 = max(0, cx - r)
            y1 = max(0, cy - r)
            x2 = min(width, cx + r)
            y2 = min(height, cy + r)
            
            # Ensure crop is perfectly square
            w_box = x2 - x1
            h_box = y2 - y1
            side = min(w_box, h_box)
            
            # Re-center square crop
            cx_new = x1 + w_box // 2
            cy_new = y1 + h_box // 2
            x1 = max(0, cx_new - side // 2)
            x2 = min(width, x1 + side)
            y1 = max(0, cy_new - side // 2)
            y2 = min(height, y1 + side)
            
            crop_pil = im.crop((x1, y1, x2, y2))
            crop_pil = crop_pil.resize((200, 200), Image.Resampling.LANCZOS)
            
            circle_pil = crop_to_circle(crop_pil)
            
            face_count += 1
            out_filename = f"cropped_face_{face_count}.png"
            out_path = os.path.join(OUTPUT_DIR, out_filename)
            circle_pil.save(out_path, "PNG")
            print(f"Saved precise crop {face_count} (from {filename}) to {out_path}")
            
        except Exception as e:
            print(f"Error cropping {filename}: {e}")
            
    print(f"Finished. Generated {face_count} face crops.")

if __name__ == "__main__":
    run_precise_crops()
