from PIL import Image, ImageDraw, ImageFont

# Create a blank image
width, height = 400, 300
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Draw lines
draw.line((10, 10, 390, 10), fill="blue", width=5)
draw.line((10, 20, 390, 20), fill="red", width=3)

# Draw a rectangle
draw.rectangle([50, 50, 350, 250], outline="green", fill="lightgreen")

# Draw an ellipse
draw.ellipse([100, 100, 300, 200], outline="purple", fill="violet")

# Add text
font = ImageFont.load_default()
draw.text((60, 60), "Hello, World!", fill="black", font=font)

# Save the image
image.save("drawing_example.png")
