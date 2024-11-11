import torch
import torch.nn as nn
import numpy as np
import cv2
from collections import Counter

# Define the modified GAN Generator architecture
class ModifiedGenerator(nn.Module):
    def __init__(self, latent_dim=100, image_size=256, channels=3):
        super(ModifiedGenerator, self).__init__()
        self.init_size = image_size // 4
        self.fc = nn.Sequential(nn.Linear(latent_dim, 128 * self.init_size ** 2))

        # Style-based layers inspired by StyleGAN2
        self.conv_blocks = nn.Sequential(
            nn.BatchNorm2d(128),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 128, 3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, channels, 3, stride=1, padding=1),
            nn.Tanh()
        )

    def forward(self, z):
        out = self.fc(z)
        out = out.view(out.shape[0], 128, self.init_size, self.init_size)
        img = self.conv_blocks(out)
        return img

# Function to generate stego image
def generate_stego_image(generator, latent_dim=100):
    noise = torch.randn(1, latent_dim)  # Latent vector
    with torch.no_grad():
        stego_image = generator(noise)
        stego_image_np = stego_image.squeeze().cpu().numpy().transpose(1, 2, 0)
        stego_image_np = ((stego_image_np + 1) / 2 * 255).clip(0, 255).astype(np.uint8)
        return stego_image_np

# Function to blend images
def blend_images(stego_image, reference_image, alpha=0.15):
    stego_image = stego_image.astype(np.float64)
    reference_image = reference_image.astype(np.float64)
    blended_image = (alpha * stego_image + (1 - alpha) * reference_image)
    blended_image = np.clip(blended_image, 0, 255).astype(np.uint8)
    return blended_image

# Function to embed message with redundancy using LSB
def embed_message_lsb_redundant(image, message, redundancy=3):
    # Convert message to binary
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    # Append a null character to mark the end of the message
    binary_message += '00000000'
    # Repeat each bit 'redundancy' times
    binary_message_redundant = ''.join(bit * redundancy for bit in binary_message)
    message_length = len(binary_message_redundant)
    flat_image = image.flatten()

    if message_length > len(flat_image):
        raise ValueError("Message is too long to be embedded in the image.")

    # Embed the redundant message bits into the LSB of the image pixels
    for i in range(message_length):
        flat_image[i] = (flat_image[i] & ~1) | int(binary_message_redundant[i])

    # Reshape back to the original image shape
    stego_image = flat_image.reshape(image.shape)
    return stego_image

# Function to extract message with redundancy from LSB
def extract_message_lsb_redundant(image, redundancy=3):
    flat_image = image.flatten()
    # We don't know the exact length, so we'll read until we hit a null character
    binary_message_redundant = ''
    for i in range(len(flat_image)):
        binary_message_redundant += str(flat_image[i] & 1)

    # Process bits with redundancy
    binary_message = ''
    for i in range(0, len(binary_message_redundant), redundancy):
        bit_chunk = binary_message_redundant[i:i+redundancy]
        if len(bit_chunk) < redundancy:
            break
        # Use majority vote for error correction
        bit = '1' if bit_chunk.count('1') > bit_chunk.count('0') else '0'
        binary_message += bit
        # Check if we've reached the null character
        if len(binary_message) % 8 == 0:
            byte = binary_message[-8:]
            if byte == '00000000':
                break  # Null character detected, end of message

    # Convert binary string to text
    message_chars = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '00000000':
            break  # Stop at null character
        ascii_code = int(byte, 2)
        message_chars.append(chr(ascii_code))
    return ''.join(message_chars)
