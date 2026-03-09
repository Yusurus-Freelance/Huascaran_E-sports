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

# --- RUTA DE PRUEBA DE CLOUDINARY ---
@app.route('/test-cloudinary')
def test_cloudinary():
    # 1. Primero, revisamos qué está leyendo Python de tu .env
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    
    html_debug = f"<h3>Datos leídos del .env:</h3>"
    html_debug += f"<ul><li>Cloud Name: {cloud_name}</li><li>API Key: {api_key}</li></ul>"
    
    # 2. Intentamos hacer "Ping" a los servidores
    try:
        respuesta = cloudinary.api.ping()
        return html_debug + f"<h3 style='color:green;'>✅ Conexión exitosa a Cloudinary:</h3> <p>{respuesta}</p>"
    except Exception as e:
        return html_debug + f"<h3 style='color:red;'>❌ Error de conexión:</h3> <p>{str(e)}</p>"

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