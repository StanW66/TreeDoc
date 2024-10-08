from PIL import Image, ImageDraw, ImageFont

# Create a blank image
width, height = 400, 300
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Draw lines
draw.line((10, 10, 390, 10), fill="blue", width=5)

# Add text
font = ImageFont.load_default()
draw.text((60, 60), "Hello, World!", fill="black", font=font)

# Save the image
image.save("drawing_example.png")
