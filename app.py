from flask import Flask, render_template
from routes.chat_routes import chat_bp
from routes.upload_routes import upload_bp
import os

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register Blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(upload_bp)

# Route for the HTML interface
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # Serves the HTML frontend

if __name__ == "__main__":
    app.run(debug=True)
