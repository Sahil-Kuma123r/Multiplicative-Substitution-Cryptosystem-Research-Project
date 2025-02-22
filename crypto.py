import numpy as np
from PIL import Image

# ------------------------------
# Improved Key Expansion Function
# ------------------------------
def generate_key(length, key):
    """Expands the key using cyclic repetition to match the required length."""
    key = [ord(char) for char in key]  # Convert key to ASCII values
    
    # If key is shorter than required length, expand it using cyclic repetition
    while len(key) < length:
        key.append(key[len(key) % len(key)])  # Cycle through the existing key

    return key[:length]  # Trim key if too long

# ------------------------------
# Image Encryption using MSC
# ------------------------------
def encrypt_image(image_path, key):
    """Encrypts an image using MSC."""
    image = Image.open(image_path).convert("RGB")
    pixels = np.array(image)
    height, width, _ = pixels.shape
    total_pixels = height * width * 3  # Total R, G, B values

    key = generate_key(total_pixels, key)  # Ensure key is long enough

    encrypted_pixels = np.zeros_like(pixels)
    index = 0  # Key index tracker

    for i in range(height):
        for j in range(width):
            for k in range(3):  # Iterate over R, G, B channels
                K = key[index]  # Get key
                A = index + 1
                B = 1 if (K**3 + A * K) % 2 == 0 else 0
                Q = (K**3 + A * K + B) % 256
                encrypted_pixels[i, j, k] = (pixels[i, j, k] * Q) % 256
                index += 1

    encrypted_image = Image.fromarray(encrypted_pixels, "RGB")
    encrypted_image.save("encrypted_image.png")
    print("Encrypted Image saved as 'encrypted_image.png'")

# ------------------------------
# Image Decryption using MSC
# ------------------------------
def mod_inverse(a, m=256):
    """Computes the modular inverse for decryption."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return 1  # Return 1 if no modular inverse found

def decrypt_image(image_path, key):
    """Decrypts an MSC-encrypted image."""
    image = Image.open(image_path).convert("RGB")
    pixels = np.array(image)
    height, width, _ = pixels.shape
    total_pixels = height * width * 3  # Total R, G, B values

    key = generate_key(total_pixels, key)  # Ensure key is long enough

    decrypted_pixels = np.zeros_like(pixels)
    index = 0  # Key index tracker

    for i in range(height):
        for j in range(width):
            for k in range(3):
                K = key[index]
                A = index + 1
                B = 1 if (K**3 + A * K) % 2 == 0 else 0
                Q = (K**3 + A * K + B) % 256
                D = mod_inverse(Q, 256)  # Compute modular inverse
                decrypted_pixels[i, j, k] = (pixels[i, j, k] * D) % 256
                index += 1

    decrypted_image = Image.fromarray(decrypted_pixels, "RGB")
    decrypted_image.save("decrypted_image.png")
    print("Decrypted Image saved as 'decrypted_image.png'")

# ------------------------------
# Ask User for Image Input
# ------------------------------
if __name__ == "__main__":
    key = input("Enter encryption key: ")  # Ask user for key

    # Ask user to provide an image
    image_path = input("Enter the path of the image to encrypt: ")

    # Encrypt the Image
    encrypt_image(image_path, key)

    # Ask if the user wants to decrypt it
    decrypt_choice = input("Do you want to decrypt the image? (yes/no): ")
    if decrypt_choice.lower() == "yes":
        decrypt_image("encrypted_image.png", key)
