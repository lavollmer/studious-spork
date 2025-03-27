from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np

def generate_noise_overlay(size, noise_intensity=10):
    """
    Create a noise overlay with random pixel distortion.
    This will be invisible but distort the image upon capture.
    """
    # Create an empty transparent image (RGBA mode)
    overlay = Image.new('RGBA', size, (0, 0, 0, 0))

    draw = ImageDraw.Draw(overlay)
    
    # Add random color noise to the overlay
    for i in range(size[0] * size[1] // noise_intensity):  # Adjust noise intensity
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        color = (
            random.randint(0, 255),  # Random red component
            random.randint(0, 255),  # Random green component
            random.randint(0, 255),  # Random blue component
            random.randint(50, 150)  # Semi-transparent noise
        )
        draw.point((x, y), fill=color)

    return overlay

def pixel_displacement(image, displacement_range=3):
    """
    Displace pixels slightly to add distortion.
    """
    pixels = np.array(image)
    for i in range(0, len(pixels), displacement_range):
        for j in range(0, len(pixels[i]), displacement_range):
            if random.random() > 0.7:  # Add displacement with a certain probability
                x_disp = random.randint(-displacement_range, displacement_range)
                y_disp = random.randint(-displacement_range, displacement_range)
                pixels[i, j] = pixels[i + x_disp, j + y_disp] if (0 <= i + x_disp < len(pixels)) and (0 <= j + y_disp < len(pixels[i])) else pixels[i, j]
    return Image.fromarray(pixels)

def blur_overlay(image, blur_radius=1):
    """
    Apply a slight blur to the overlay to simulate more subtle distortion.
    """
    return image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

def create_protected_image(base_image_path, output_image_path):
    # Open the original artwork image
    base_image = Image.open(base_image_path).convert("RGBA")

    # Generate a custom noise overlay
    overlay = generate_noise_overlay(base_image.size, noise_intensity=5)

    # Optionally, apply pixel displacement to the base image
    displaced_image = pixel_displacement(base_image, displacement_range=2)

    # Optionally, apply blur to the overlay to make the distortion less obvious
    blurred_overlay = blur_overlay(overlay, blur_radius=2)

    # Combine the artwork with the overlay (this will blend both images)
    combined_image = Image.alpha_composite(displaced_image, blurred_overlay)

    # Save the resulting image
    combined_image.save(output_image_path)
    print(f"Protected image saved as {output_image_path}")

# Example usage
base_image = 'your_artwork_image.jpg'  # Path to your artwork image
output_image = 'protected_artwork_with_customization.png'  # Path to save the protected image

create_protected_image(base_image, output_image)
