from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from utils import (
    ModifiedGenerator,
    generate_stego_image,
    blend_images,
    embed_message_lsb_redundant,
    extract_message_lsb_redundant,
)
import torch
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the generator model with random weights
latent_dim = 100
generator = ModifiedGenerator(latent_dim=latent_dim)
generator.eval()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'generate':
            return redirect(url_for('generate'))
        elif mode == 'extract':
            return redirect(url_for('extract'))
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        secret_message = request.form.get('secret_message')
        cover_image_file = request.files.get('cover_image')

        if not secret_message or not cover_image_file:
            return "Please provide a secret message and a cover image."

        # Generate a unique identifier for this session
        session_id = str(uuid.uuid4())

        # Save the uploaded cover image with a unique filename
        cover_image_filename = f'cover_image_{session_id}.png'
        cover_image_path = os.path.join(
            app.config['UPLOAD_FOLDER'], cover_image_filename
        )
        cover_image_file.save(cover_image_path)

        # Read and resize the cover image
        reference_image = cv2.imread(cover_image_path)
        reference_image = cv2.resize(reference_image, (256, 256))

        # Save the resized cover image for display
        resized_cover_image_filename = f'cover_image_resized_{session_id}.png'
        resized_cover_image_path = os.path.join(
            app.config['UPLOAD_FOLDER'], resized_cover_image_filename
        )
        cv2.imwrite(resized_cover_image_path, reference_image)

        # Generate stego image
        stego_image = generate_stego_image(generator, latent_dim)

        # Blend images
        alpha = 0.15
        blended_image = blend_images(stego_image, reference_image, alpha=alpha)

        # Embed the secret message
        redundancy = 3
        authenticated_image = embed_message_lsb_redundant(
            blended_image, secret_message, redundancy=redundancy
        )

        # Save authenticated image with a unique filename
        authenticated_image_filename = f'authenticated_image_{session_id}.png'
        authenticated_image_path = os.path.join(
            app.config['UPLOAD_FOLDER'], authenticated_image_filename
        )
        cv2.imwrite(authenticated_image_path, authenticated_image)

        return render_template(
            'result.html',
            mode='generate',
            original_image=url_for('static', filename=f'uploads/{resized_cover_image_filename}'),
            result_image=url_for('static', filename=f'uploads/{authenticated_image_filename}'),
        )

    return render_template('generate.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        authenticated_image_file = request.files.get('authenticated_image')

        if not authenticated_image_file:
            return "Please provide an authenticated image."

        # Generate a unique identifier for this session
        session_id = str(uuid.uuid4())

        # Save the uploaded authenticated image with a unique filename
        authenticated_image_filename = f'authenticated_image_{session_id}.png'
        authenticated_image_path = os.path.join(
            app.config['UPLOAD_FOLDER'], authenticated_image_filename
        )
        authenticated_image_file.save(authenticated_image_path)

        # Load the authenticated image
        authenticated_image = cv2.imread(authenticated_image_path)

        # Extract the secret message
        redundancy = 3
        extracted_message = extract_message_lsb_redundant(
            authenticated_image, redundancy=redundancy
        )

        return render_template(
            'result.html',
            mode='extract',
            result_image=url_for('static', filename=f'uploads/{authenticated_image_filename}'),
            extracted_message=extracted_message,
        )

    return render_template('extract.html')

if __name__ == '__main__':
    app.run(debug=True)
