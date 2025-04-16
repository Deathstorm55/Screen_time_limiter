from PIL import Image, ImageDraw, ImageFont

# Create base image (256x256 is standard for .ico)
img = Image.new('RGBA', (256, 256), (25, 118, 210, 255))  # Blue background
draw = ImageDraw.Draw(img)

# Draw timer circle
draw.ellipse([(30, 30), (226, 226)], outline='white', width=15)

# Add progress indicator
draw.pieslice([(30, 30), (226, 226)], start=30, end=150, fill='#FFC107', outline='#FFC107')

# Add screen elements
draw.rectangle([(80, 100), (176, 140)], fill='white')
draw.text((95, 110), "ST", font=ImageFont.truetype('arial.ttf', 40), fill='#1976D2')

# Create icon with multiple sizes
img.save('screen_timer.ico', format='ICO', sizes=[(256,256), (128,128), (64,64), (48,48), (32,32), (16,16)])