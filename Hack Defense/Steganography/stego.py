# stego.py — Interactive Steganography Image Encoder/Decoder
# Author: V. Greeshma Gowda
# Project: Cyber Shield - Steganography Image Encoder/Decoder

from PIL import Image
import os

IMAGE_DIR = "images"

def encode(infile, outfile, message):
    """Hide a secret message inside an image using LSB encoding."""
    img = Image.open(infile)
    img = img.convert("RGB")
    data = list(img.getdata())

    # Convert message to binary bits + null terminator
    bits = ''.join(f"{ord(c):08b}" for c in message) + "00000000"

    if len(bits) > len(data) * 3:
        raise ValueError("❌ Message too long for this image! Use a larger image.")

    new_data = []
    bit_index = 0
    for pixel in data:
        r, g, b = pixel[:3]
        if bit_index < len(bits):
            r = (r & ~1) | int(bits[bit_index])
            bit_index += 1
        if bit_index < len(bits):
            g = (g & ~1) | int(bits[bit_index])
            bit_index += 1
        if bit_index < len(bits):
            b = (b & ~1) | int(bits[bit_index])
            bit_index += 1
        new_data.append((r, g, b))

    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(new_data)
    encoded_img.save(outfile)

    print(f"\n✅ Message successfully hidden inside '{outfile}'")

def decode(infile):
    """Extract a hidden message from an image encoded with LSB steganography."""
    img = Image.open(infile)
    img = img.convert("RGB")
    data = list(img.getdata())

    bits = ''.join(str(channel & 1) for pixel in data for channel in pixel[:3])
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]

    message = ""
    for byte in chars:
        char = chr(int(byte, 2))
        if char == '\x00':  # end of message
            break
        message += char

    print(f"\n🔓 Hidden message found:\n>>> {message}\n")

def choose_file_from_dir(prompt_text, base_dir=IMAGE_DIR):
    """Lists image files in a directory and prompts the user to choose one."""
    image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"}

    if not os.path.isdir(base_dir):
        print(f"INFO: Image directory '{base_dir}' not found. Creating it.")
        try:
            os.makedirs(base_dir)
        except OSError as e:
            print(f"❌ Error creating directory {base_dir}: {e}")
            return None
    try:
        files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f)) and os.path.splitext(f)[1].lower() in image_extensions]
    except OSError as e:
        print(f"❌ Error accessing directory: {e}")
        return None

    if not files:
        print(f"\n❌ No image files found in the '{base_dir}' directory. Please add some images to it.")
        return None

    print(prompt_text)
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")

    while True:
        try:
            choice = int(input(f"\nEnter your choice (1-{len(files)}): ").strip())
            if 1 <= choice <= len(files):
                return os.path.join(base_dir, files[choice - 1])
            else:
                print(f"❌ Invalid choice. Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def main():
    print("\n🖼️  Steganography Image Encoder/Decoder (Cyber Shield)")
    print("-----------------------------------------------------")
    print("1. Encode a secret message into an image")
    print("2. Decode a hidden message from an image")
    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "1":
        infile = choose_file_from_dir("\nSelect an image to hide a message in:")
        if not infile: return
        outfile_name = input("Enter output image file name (e.g., secret.png) to be saved in the 'Steganography/images' folder: ").strip()
        outfile = os.path.join(IMAGE_DIR, outfile_name)
        message = input("Enter the secret message to hide: ").strip()
        encode(infile, outfile, message)
    elif choice == "2":
        infile = choose_file_from_dir("\nSelect an image to decode:")
        if not infile: return
        decode(infile)
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
