from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a new image with RGBA (for transparency)
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Create circular background with gradient
    for i in range(size):
        for j in range(size):
            # Calculate distance from center
            dx = i - size/2
            dy = j - size/2
            distance = (dx**2 + dy**2)**0.5
            
            if distance <= size/2:
                # Create gradient effect
                gradient = 1 - (distance/(size/2))
                # Mix between blue and purple
                r = int(41 * (1-gradient) + 142 * gradient)  # From blue to purple
                g = int(128 * (1-gradient) + 68 * gradient)
                b = int(185 * (1-gradient) + 173 * gradient)
                a = 255  # Full opacity
                
                image.putpixel((i, j), (r, g, b, a))
    
    # Add 'J' letter in the center
    try:
        # Try to use a nice font if available
        font = ImageFont.truetype("arial.ttf", size=160)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw white 'J' with slight offset for shadow effect
    draw.text((size/2-45, size/2-80), 'J', fill=(0, 0, 0, 100), font=font)  # shadow
    draw.text((size/2-48, size/2-83), 'J', fill=(255, 255, 255, 255), font=font)  # main text
    
    # Save in different sizes
    sizes = [(256, 256), (128, 128), (64, 64), (32, 32)]
    for s in sizes:
        resized = image.resize(s, Image.Resampling.LANCZOS)
        resized.save(f'icon_{s[0]}.png')
    
    # Save as ICO file
    image.save('jeremiah.ico', format='ICO', sizes=sizes)

if __name__ == '__main__':
    create_icon()
