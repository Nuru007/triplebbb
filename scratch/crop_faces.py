import os
import sys
from PIL import Image, ImageDraw, ImageOps

# Paths
IMAGE_DIR = "assets/images"
OUTPUT_DIR = "assets/images"

# Manual crop definitions as coordinates: (center_x, center_y, radius)
# Optimized for the specific stock photo dimensions and typical face placements
MANUAL_CROPS = {
    "story_founder.jpg": [
        {"center_x": 341, "center_y": 300, "radius": 150} # founder face
    ],
    "about_speaker.jpg": [
        {"center_x": 341, "center_y": 280, "radius": 130} # speaker face
    ],
    "hero_speaker.jpg": [
        {"center_x": 512, "center_y": 200, "radius": 120} # speaker face
    ],
    "hero_leadership.png": [
        {"center_x": 500, "center_y": 350, "radius": 160} # student leader face
    ],
    "hero_mentorship.png": [
        {"center_x": 512, "center_y": 320, "radius": 150} # mentor/student face
    ],
    "hero_sisterhood.png": [
        {"center_x": 480, "center_y": 300, "radius": 150} # sisterhood student face
    ],
    "about_gesture.jpg": [
        {"center_x": 341, "center_y": 260, "radius": 130} # student face
    ],
    "hero_workshop.jpg": [
        {"center_x": 512, "center_y": 240, "radius": 120} # speaker/student face
    ]
}

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

def crop_manual():
    print("Running in manual PIL-fallback mode...")
    face_count = 0
    for filename, crops in MANUAL_CROPS.items():
        img_path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            continue
            
        print(f"Manually cropping {filename}...")
        try:
            im = Image.open(img_path)
            width, height = im.size
            
            for idx, crop in enumerate(crops):
                cx = crop["center_x"]
                cy = crop["center_y"]
                r = crop["radius"]
                
                # Check bounds
                x1 = max(0, cx - r)
                y1 = max(0, cy - r)
                x2 = min(width, cx + r)
                y2 = min(height, cy + r)
                
                # Force square
                w_box = x2 - x1
                h_box = y2 - y1
                side = min(w_box, h_box)
                
                # Re-center box
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
                print(f"Saved manually cropped face {face_count} to {out_path}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Manual cropping complete. Generated {face_count} face images.")

def crop_opencv():
    import cv2
    import numpy as np
    
    print("Running in OpenCV-auto mode...")
    HAAR_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    if face_cascade.empty():
        print("Error: Could not load Haar cascade classifier. Falling back to manual mode.")
        crop_manual()
        return

    face_count = 0
    for filename in MANUAL_CROPS.keys():
        img_path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            continue
            
        print(f"Processing {filename}...")
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to read image: {img_path}")
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )
        
        print(f"Found {len(faces)} faces in {filename}")
        
        # If OpenCV failed to detect any face, fallback to manual crop for this image
        if len(faces) == 0:
            print(f"No faces detected in {filename}. Falling back to manual crop.")
            try:
                im = Image.open(img_path)
                width, height = im.size
                crop = MANUAL_CROPS[filename][0]
                cx, cy, r = crop["center_x"], crop["center_y"], crop["radius"]
                x1, y1 = max(0, cx - r), max(0, cy - r)
                x2, y2 = min(width, cx + r), min(height, cy + r)
                crop_pil = im.crop((x1, y1, x2, y2)).resize((200, 200), Image.Resampling.LANCZOS)
                circle_pil = crop_to_circle(crop_pil)
                face_count += 1
                out_path = os.path.join(OUTPUT_DIR, f"cropped_face_{face_count}.png")
                circle_pil.save(out_path, "PNG")
                print(f"Saved manually cropped face {face_count} to {out_path}")
            except Exception as e:
                print(f"Manual fallback error for {filename}: {e}")
            continue
            
        for i, (x, y, w, h) in enumerate(faces):
            padding_w = int(w * 0.4)
            padding_h = int(h * 0.4)
            
            y1 = max(0, y - padding_h)
            y2 = min(img.shape[0], y + h + padding_h)
            x1 = max(0, x - padding_w)
            x2 = min(img.shape[1], x + w + padding_w)
            
            crop_h = y2 - y1
            crop_w = x2 - x1
            side = min(crop_h, crop_w)
            
            cx, cy = x1 + crop_w // 2, y1 + crop_h // 2
            x1_sq = max(0, cx - side // 2)
            x2_sq = min(img.shape[1], x1_sq + side)
            y1_sq = max(0, cy - side // 2)
            y2_sq = min(img.shape[0], y1_sq + side)
            
            if (x2_sq - x1_sq) < side:
                side = x2_sq - x1_sq
                y2_sq = min(img.shape[0], y1_sq + side)
            if (y2_sq - y1_sq) < side:
                side = y2_sq - y1_sq
                x2_sq = min(img.shape[1], x1_sq + side)
                
            crop_cv = img[y1_sq:y2_sq, x1_sq:x2_sq]
            crop_rgb = cv2.cvtColor(crop_cv, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_rgb)
            crop_pil = crop_pil.resize((200, 200), Image.Resampling.LANCZOS)
            
            circle_pil = crop_to_circle(crop_pil)
            
            face_count += 1
            out_filename = f"cropped_face_{face_count}.png"
            out_path = os.path.join(OUTPUT_DIR, out_filename)
            circle_pil.save(out_path, "PNG")
            print(f"Saved auto-cropped face {face_count} to {out_path}")

if __name__ == "__main__":
    try:
        import cv2
        crop_opencv()
    except ImportError:
        crop_manual()
