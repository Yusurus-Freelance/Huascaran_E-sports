import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv # Asegúrate de importar load_dotenv
from controllers.public_controller import public_bp
from controllers.staff_controller import staff_bp 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=7)

# --- CONFIGURACIÓN DE CLOUDINARY ---
cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key = os.getenv('CLOUDINARY_API_KEY'),
  api_secret = os.getenv('CLOUDINARY_API_SECRET')
)
# -----------------------------------

app.register_blueprint(public_bp)
app.register_blueprint(staff_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)