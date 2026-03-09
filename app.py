from flask import Flask
from controllers.public_controller import public_bp
from controllers.staff_controller import staff_bp

app = Flask(__name__)
app.secret_key = 'huascaran_esports_secreto_2026'

# Registramos los Controladores (Blueprints)
app.register_blueprint(public_bp)
app.register_blueprint(staff_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)