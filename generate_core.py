import os
import random
from PIL import Image, ImageDraw

# Color palette from your README
COLOR_BG = (10, 10, 10, 255) # Matte black
COLOR_GLOW = (242, 86, 35, 255) # F25623
COLOR_ALT = (255, 69, 0, 255) # FF4500
COLOR_TEXT = (255, 255, 255, 255) # White

def generate_core_pattern(width=1600, height=800):
    """
    Generates a unique, procedural isometric design
    to represent a conceptual 'Digital Core'.
    """
    img = Image.new('RGBA', (width, height), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Simple grid base for complex, multi-layered feel
    grid_size = 40
    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            # Draw a subtle base grid pattern
            draw.point((x, y), fill=(20, 20, 20, 255))

    # Add complex, procedural structures
    # (Here we just draw some random connected paths and blocks)
    for _ in range(30):
        # Pick a starting point
        x1 = random.randrange(width // 4, 3 * width // 4, grid_size)
        y1 = random.randrange(height // 4, 3 * height // 4, grid_size)

        # Draw a complex, branching path
        length = random.randint(5, 15)
        for _ in range(length):
            direction = random.choice(['x', 'y'])
            change = random.choice([-grid_size, grid_size])
            if direction == 'x':
                x2, y2 = x1 + change, y1
            else:
                x2, y2 = x1, y1 + change
            
            # Constrain to reasonable canvas space
            x2 = max(0, min(width, x2))
            y2 = max(0, min(height, y2))

            # Draw glowing line and 'nodes' (blocks)
            line_color = random.choice([COLOR_GLOW, COLOR_ALT])
            
            # Simulate multi-layered structure
            line_width = random.randint(3, 8)
            draw.line((x1, y1, x2, y2), fill=line_color, width=line_width)
            
            # Procedural node structure
            if random.random() < 0.2:
                # Add white node accent
                draw.rectangle((x2-10, y2-10, x2+10, y2+10), outline=COLOR_TEXT, width=2)
            
            # Continue the path
            x1, y1 = x2, y2

    # Add 'data particle' cluster
    for _ in range(50):
        px = random.randrange(0, width)
        py = random.randrange(0, height)
        size = random.randint(1, 3)
        draw.ellipse((px, py, px+size, py+size), fill=COLOR_GLOW)

    # Apply some depth effects
    # (A full engine would render reflections and depth-of-field)
    
    # Save the generated image
    # Note: For animation, your script would generate and save frames, 
    # then combine them into a final .gif or .mp4 file.
    img.save('digital_core.png')

if __name__ == '__main__':
    generate_core_pattern()