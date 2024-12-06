from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.pdf_service import extract_text_from_pdf, sliding_window_chunking
from services.embedding_service import create_embeddings
from services.faiss_service import store_embeddings_faiss
import os
import globals

upload_bp = Blueprint('upload_bp', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"response": "No file part."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"response": "No selected file."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('./uploads', filename)
        file.save(filepath)

        try:
            pdf_text = extract_text_from_pdf(filepath)
            globals.chunks = sliding_window_chunking(pdf_text, 128, 16)
            embeddings = create_embeddings(globals.chunks)
            globals.index = store_embeddings_faiss(embeddings)

            return jsonify({"response": "File uploaded successfully."})
        except Exception as e:
            return jsonify({"response": f"Error processing PDF: {str(e)}"}), 500
    else:
        return jsonify({"response": "Invalid file type. Only PDFs are allowed."}), 400
