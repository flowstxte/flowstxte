import math
from PIL import Image, ImageDraw

# Your specific palette
COLOR_BG = (10, 10, 10) # Dark background
COLOR_GLOW = (242, 86, 35) # Your F25623 primary
COLOR_ALT = (255, 69, 0) # Your FF4500 secondary
COLOR_ACCENT = (255, 255, 255) # White data nodes

def draw_hexagon(draw, center, radius, rotation, color, width):
    cx, cy = center
    points = []
    for i in range(6):
        angle = math.radians(rotation + i * 60)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    points.append(points[0]) # close the loop
    draw.line(points, fill=color, width=width)

def generate_animated_core():
    width, height = 800, 400
    frames = []
    num_frames = 60 # 60 frames for a smooth 2-second loop
    
    for f in range(num_frames):
        # Using RGB for GIF compatibility
        img = Image.new('RGB', (width, height), COLOR_BG)
        draw = ImageDraw.Draw(img)
        
        center = (width // 2, height // 2)
        time = f / num_frames # Percentage of the loop (0.0 to 1.0)
        
        # 1. Background grid with a moving scanline effect
        scan_y = int(time * height)
        for y in range(0, height, 40):
            dist = abs(y - scan_y)
            # Make the grid line glow slightly if the scanline is near it
            if dist < 40 or abs(y - (scan_y - height)) < 40:
                draw.line((0, y, width, y), fill=(30, 30, 30), width=1)
            else:
                draw.line((0, y, width, y), fill=(15, 15, 15), width=1)

        # 2. Draw rotating architectural structures (Hexagons)
        for i in range(6):
            radius = 35 + i * 25
            direction = 1 if i % 2 == 0 else -1
            
            # Continuous rotation
            rotation = time * 360 * direction + (i * 20)
            
            # Pulsing line thickness using a sine wave
            thickness = int(2 + math.sin(time * math.pi * 2 + i) * 1.5)
            color = COLOR_GLOW if i % 2 == 0 else COLOR_ALT
            
            draw_hexagon(draw, center, radius, rotation, color, thickness)
            
            # 3. Add orbiting data nodes that move faster than the rings
            node_angle = math.radians(rotation + (time * 360 * direction * 2))
            nx = center[0] + radius * math.cos(node_angle)
            ny = center[1] + radius * math.sin(node_angle)
            draw.ellipse((nx-3, ny-3, nx+3, ny+3), fill=COLOR_ACCENT)
            
        frames.append(img)
        
    # Save the frames as a seamlessly looping GIF
    frames[0].save(
        'digital_core.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=33, # 33ms per frame = ~30fps
        loop=0 # 0 means loop forever
    )

if __name__ == '__main__':
    generate_animated_core()