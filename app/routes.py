from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.pdf_parser import extract_pdf_data
from app.config import Config
import os

# Define a Blueprint for modular routing
main = Blueprint('main', __name__)

# Endpoint to handle PDF uploads
@main.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    # Check if the file is actually selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        # Ensure the upload folder exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        # Secure the filename and save it
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        try:
            # Parse the PDF and extract data
            extracted_data = extract_pdf_data(file_path)
        except Exception as e:
            return jsonify({'error': 'Failed to parse PDF', 'details': str(e)}), 500
        finally:
            # Always clean up the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

        # Return the parsed data as JSON
        return jsonify(extracted_data), 200

    return jsonify({'error': 'Unknown error occurred'}), 500
