from PIL import Image
import random
import os

def encrypt_swap(image_path, output_path):
    """
    Encrypts an image by randomly swapping pixel locations.
    The swap key is a list of tuples representing the original and new positions.
    This key is returned for use in decryption.
    """
    try:
        # Open the image file
        img = Image.open(image_path)
        img = img.convert("RGB") # Ensure image is in RGB format
        width, height = img.size
        pixels = list(img.getdata())

        # Create a list of all pixel indices
        indices = list(range(len(pixels)))
        
        # Shuffle the indices to create a random permutation
        shuffled_indices = indices[:]
        random.shuffle(shuffled_indices)
        
        # Create the new pixel data based on the shuffled indices
        encrypted_pixels = [pixels[i] for i in shuffled_indices]

        # Create a new image from the encrypted pixel data
        encrypted_img = Image.new("RGB", (width, height))
        encrypted_img.putdata(encrypted_pixels)
        
        # Save the encrypted image
        encrypted_img.save(output_path)
        print(f"Image encrypted successfully via pixel swapping. Saved to '{output_path}'.")

        # Create a map for decryption
        swap_key = list(zip(shuffled_indices, indices))
        return swap_key

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred during encryption: {e}")
        return None

def decrypt_swap(image_path, swap_key, output_path):
    """
    Decrypts an image by reversing the pixel swapping.
    Requires the original swap key generated during encryption.
    """
    try:
        # Open the encrypted image
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size
        encrypted_pixels = list(img.getdata())

        # Create a new list for the decrypted pixels
        decrypted_pixels = [0] * len(encrypted_pixels)
        
        # Re-map pixels to their original positions using the key
        for original_index, new_index in swap_key:
            decrypted_pixels[original_index] = encrypted_pixels[new_index]

        # Create the new, decrypted image
        decrypted_img = Image.new("RGB", (width, height))
        decrypted_img.putdata(decrypted_pixels)
        
        # Save the decrypted image
        decrypted_img.save(output_path)
        print(f"Image decrypted successfully via pixel swapping. Saved to '{output_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred during decryption: {e}")

def encrypt_xor(image_path, key, output_path):
    """
    Encrypts an image by applying a bitwise XOR operation to each pixel's
    RGB values with a given integer key.
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size
        
        # Create a new image for the encrypted pixels
        encrypted_img = Image.new("RGB", (width, height))

        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                
                # Apply XOR operation to each color channel
                encrypted_r = r ^ key
                encrypted_g = g ^ key
                encrypted_b = b ^ key
                
                encrypted_img.putpixel((x, y), (encrypted_r, encrypted_g, encrypted_b))
        
        encrypted_img.save(output_path)
        print(f"Image encrypted successfully via XOR. Saved to '{output_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred during encryption: {e}")

def decrypt_xor(image_path, key, output_path):
    """
    Decrypts an image by applying the same XOR operation again.
    (XOR is reversible: A ^ B ^ B = A)
    """
    # The decryption process is identical to the encryption process for XOR
    encrypt_xor(image_path, key, output_path)
    # The print statement in encrypt_xor is sufficient
    print(f"Image decrypted successfully via XOR. Saved to '{output_path}'.")

def main():
    """
    Main function to demonstrate the usage of the encryption and decryption tools.
    You must have a test image file in the same directory to run this.
    """
    input_image = 'test_image.png'  # <--- Change this to your image file name
    xor_key = 123  # A simple integer key for the XOR operation

    # Check if the input image file exists
    if not os.path.exists(input_image):
        print(f"Error: The file '{input_image}' does not exist.")
        print("Please place an image file in the same directory and update the 'input_image' variable.")
        return

    # --- Demonstrate Pixel Swapping Encryption/Decryption ---
    print("\n--- Testing Pixel Swapping Encryption ---")
    encrypted_swap_path = "encrypted_swap.png"
    swap_key = encrypt_swap(input_image, encrypted_swap_path)
    
    if swap_key:
        print("\n--- Testing Pixel Swapping Decryption ---")
        decrypted_swap_path = "decrypted_swap.png"
        decrypt_swap(encrypted_swap_path, swap_key, decrypted_swap_path)
    
    # --- Demonstrate XOR Encryption/Decryption ---
    print("\n--- Testing XOR Encryption ---")
    encrypted_xor_path = "encrypted_xor.png"
    encrypt_xor(input_image, xor_key, encrypted_xor_path)
    
    print("\n--- Testing XOR Decryption ---")
    decrypted_xor_path = "decrypted_xor.png"
    decrypt_xor(encrypted_xor_path, xor_key, decrypted_xor_path)

if __name__ == "__main__":
    main()