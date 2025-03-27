from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np

def generate_noise_overlay(size, noise_intensity=3):
    """
    Create a noise overlay with random pixel distortion.
    This will be invisible but distort the image upon capture.
    """
    # Create an empty transparent image (RGBA mode)
    overlay = Image.new('RGBA', size, (0, 0, 0, 0))

    draw = ImageDraw.Draw(overlay)
    
    # Add random color noise to the overlay with higher intensity
    for i in range(size[0] * size[1] // noise_intensity):  # Increase noise density
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        color = (
            random.randint(0, 255),  # Random red component
            random.randint(0, 255),  # Random green component
            random.randint(0, 255),  # Random blue component
            random.randint(50, 150)  # Semi-transparent noise (make it more visible)
        )
        draw.point((x, y), fill=color)

    return overlay

def pixel_displacement(image, displacement_range=10):
    """
    Displace pixels more dramatically to add more distortion.
    Create more chaotic displacement.
    """
    pixels = np.array(image)
    for i in range(0, len(pixels), displacement_range):
        for j in range(0, len(pixels[i]), displacement_range):
            if random.random() > 0.4:  # Increase randomness for more mixed-up distortion
                x_disp = random.randint(-displacement_range, displacement_range)
                y_disp = random.randint(-displacement_range, displacement_range)
                # Ensure the displacement is within bounds
                if (0 <= i + x_disp < len(pixels)) and (0 <= j + y_disp < len(pixels[i])):
                    pixels[i, j] = pixels[i + x_disp, j + y_disp]
    return Image.fromarray(pixels)

def blur_overlay(image, blur_radius=8):
    """
    Apply a stronger blur to the overlay for more subtle distortion.
    """
    return image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

def generate_multiple_noise_layers(size, num_layers=5):
    """
    Generate multiple layers of noise and combine them to create more mixed-up distortion.
    """
    combined_overlay = Image.new('RGBA', size, (0, 0, 0, 0))
    
    for _ in range(num_layers):
        # Generate a random noise layer
        noise_layer = generate_noise_overlay(size, noise_intensity=random.randint(3, 5))
        # Combine the noise layers
        combined_overlay = Image.alpha_composite(combined_overlay, noise_layer)
    
    return combined_overlay

def create_protected_image(base_image_path, output_image_path):
    # Open the original artwork image
    base_image = Image.open(base_image_path).convert("RGBA")

    # Generate multiple noise layers for a more chaotic effect
    overlay = generate_multiple_noise_layers(base_image.size, num_layers=10)

    # Apply pixel displacement to the base image with stronger distortion
    displaced_image = pixel_displacement(base_image, displacement_range=10)

    # Apply a stronger blur to the overlay to make the distortion more chaotic
    blurred_overlay = blur_overlay(overlay, blur_radius=8)

    # Combine the artwork with the overlay (this will blend both images)
    combined_image = Image.alpha_composite(displaced_image, blurred_overlay)

    # Save the resulting image
    combined_image.save(output_image_path)
    print(f"Protected image saved as {output_image_path}")

# Example usage
base_image = 'medicinebottle.png'  # Path to your image
output_image = 'protected_medicinebottle_more_distorted.png'  # Path to save the protected image

create_protected_image(base_image, output_image)
