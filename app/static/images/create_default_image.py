from PIL import Image, ImageDraw, ImageFont
import os

# Create a 400x300 image with a green background
img = Image.new('RGB', (400, 300), color=(25, 135, 84))
d = ImageDraw.Draw(img)

# Add text
d.text((150, 150), "FarmFresh", fill=(255, 255, 255))

# Save the image
img.save('default-product.jpg')

print("Default product image created successfully!")
