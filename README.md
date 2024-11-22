# Image Steganography Web Application

![Python 3.x](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green)
![PyTorch](https://img.shields.io/badge/PyTorch-1.8.1-orange)
![NumPy](https://img.shields.io/badge/NumPy-1.21.0-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5.3-brightgreen)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4.2-red)
![HTML/CSS](https://img.shields.io/badge/HTML%2FCSS-E34F26-blue)

This is a web application that allows users to embed and extract secret messages in images using steganography techniques. The application is built with Python and Flask, utilizing a modified GAN generator for image generation.

## Table of Contents

- [Features](README.md#features)
- [Demo](#demo)
- [Installation](installation)
- [Usage](#usage)
  - [Interactive Characteristics](#interactive-characteristics)   
  - [Generate Mode](#generate-mode)
  - [Extract Mode](#extract-mode)

## Features

- **Embed Secret Messages:** Users can embed secret text messages into images.
- **Extract Secret Messages:** Users can extract embedded messages from authenticated images.
- **Image Generation:** Utilizes a modified GAN generator to create stego images.
- **Blending:** Blends generated images with user-uploaded cover images.
- **LSB Steganography with Redundancy:** Implements Least Significant Bit (LSB) steganography with redundancy for robustness.
- **Web Interface:** Provides an intuitive web interface for interaction.

## Demo

<img width="1188" alt="image" src="https://github.com/user-attachments/assets/a9d3f7f6-04d9-47db-98b2-5ce44804f696">


## Installation

- Install Dependencies
```
pip install -r requirements.txt
```

### Prerequisites

- Python 3.x
- Git

## Usage

- Run the Flask App
```
python app.py
```

- Access the Web Application
Open your web browser and navigate to:
```
http://localhost:5000
```
### Interactive Characteristics

- Mode Selection: Upon starting, the application prompts you to choose between "Generate" or "Extract" modes.
- User-Friendly Forms: Provides forms for uploading images and entering secret messages.
- Real-Time Feedback: Displays results immediately after processing.
- Downloadable Images: Allows you to download the authenticated images.

## Generate Mode

1. Select "Generate" Mode on the home page.
2. Upload a Cover Image: Choose an image file from your computer.
3. Enter Secret Message: Type the text you want to embed.
4. Generate Authenticated Image: Click the button to process.
5. View Results:
    - Original Image: Displays the uploaded cover image.
    - Authenticated Image: Displays the image with the embedded message.
6. Download Authenticated Image: Option to download the result.

## Extract Mode

1. Select "Extract" Mode on the home page.
2. Upload Authenticated Image: Choose the image containing the embedded message.
3. Extract Secret Message: Click the button to process.
4. View Results:
    - Authenticated Image: Displays the uploaded image.
    - Extracted Message: Shows the hidden text extracted from the image.

>[!Note]
>**Uploads Directory:** The application uses static/uploads/ to store user-uploaded and generated images. Ensure this directory exists and is writable.

>[!Note]
>**Generator Model:** If you have a pre-trained generator model (generator_model.pth), place it in the models directory. Otherwise, the generator will use random weights.

>[!Note]
>**Message Length:** The maximum length of the secret message depends on the image size and redundancy factor. For larger messages, adjust the redundancy or image size accordingly.

>[!Note]
>**Image Formats:** Use lossless image formats like PNG to prevent compression artifacts from affecting the embedded data.
