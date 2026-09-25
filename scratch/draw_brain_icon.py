from PIL import Image, ImageDraw

def draw_book_icon():
    # Create a 512x512 transparent image
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Coordinates for a clean, thick flat-design open book icon
    # Left Page
    left_page = [
        (240, 150), (200, 130), (140, 130), (70, 160),
        (70, 370), (140, 340), (200, 340), (240, 360)
    ]
    # Right Page
    right_page = [
        (272, 160), (312, 340), (372, 340), (442, 370),
        (442, 160), (372, 130), (312, 130), (272, 150)
    ]
    
    # Draw book pages using smooth polygon drawing
    # For a high-quality icon, we'll draw filled polygons with clean curves
    # We can draw the main pages and a book spine
    
    # Left page outline (thick)
    draw.polygon(
        [(240, 160), (190, 140), (130, 140), (80, 170), 
         (80, 360), (130, 330), (190, 330), (240, 350)],
        fill=(18, 10, 29, 255) # Match brand dark color
    )
    
    # Right page outline (thick)
    draw.polygon(
        [(272, 160), (322, 140), (382, 140), (432, 170), 
         (432, 360), (382, 330), (322, 330), (272, 350)],
        fill=(18, 10, 29, 255)
    )
    
    # Center spine
    draw.rectangle([(246, 170), (266, 360)], fill=(18, 10, 29, 255))
    
    # Bottom page edges (pages stack effect)
    draw.polygon([(80, 360), (130, 330), (190, 330), (240, 350), (240, 365), (190, 345), (130, 345), (80, 375)], fill=(18, 10, 29, 200))
    draw.polygon([(432, 360), (382, 330), (322, 330), (272, 350), (272, 365), (322, 345), (382, 345), (432, 375)], fill=(18, 10, 29, 200))

    img.save("/Users/admin/Desktop/triplebwebsite/assets/images/icon_brain.png", "PNG")
    print("Brain icon generated successfully!")

if __name__ == "__main__":
    draw_book_icon()
