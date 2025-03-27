from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np
import os
import io
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

def generate_noise_overlay(size, noise_intensity=10):
    overlay = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for i in range(size[0] * size[1] // noise_intensity): 
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(50, 150)
        )
        draw.point((x, y), fill=color)

    return overlay

def pixel_displacement(image, displacement_range=3):
    pixels = np.array(image)
    for i in range(0, len(pixels), displacement_range):
        for j in range(0, len(pixels[i]), displacement_range):
            if random.random() > 0.7:
                x_disp = random.randint(-displacement_range, displacement_range)
                y_disp = random.randint(-displacement_range, displacement_range)
                pixels[i, j] = pixels[i + x_disp, j + y_disp] if (0 <= i + x_disp < len(pixels)) and (0 <= j + y_disp < len(pixels[i])) else pixels[i, j]
    return Image.fromarray(pixels)

def blur_overlay(image, blur_radius=1):
    return image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400

    # Open the uploaded image
    img = Image.open(file.stream).convert("RGBA")

    # Apply distortions
    overlay = generate_noise_overlay(img.size, noise_intensity=5)
    displaced_image = pixel_displacement(img, displacement_range=2)
    blurred_overlay = blur_overlay(overlay, blur_radius=2)

    # Combine the artwork with the overlay
    combined_image = Image.alpha_composite(displaced_image, blurred_overlay)

    # Save the resulting image to a BytesIO object to send back as a response
    img_byte_arr = io.BytesIO()
    combined_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
