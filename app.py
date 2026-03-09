from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'clave_super_secreta_para_sesiones' # Cambia esto en producción

# --- RUTAS PÚBLICAS ---
@app.route('/')
def index():
    # Aquí luego harás el SELECT de equipos con estado 'si'
    return render_template('public/index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Aquí irá la lógica para guardar el equipo y sus integrantes
    return render_template('public/registro.html')

# --- RUTAS DEL STAFF ---
@app.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    return render_template('staff/login.html')

@app.route('/staff/dashboard')
def staff_dashboard():
    # Aquí cargarás los equipos con estado 'no' (pendientes de yape)
    return render_template('staff/dashboard.html')

if __name__ == '__main__':
    # Modo debug activado para facilitar el desarrollo
    app.run(debug=True, port=5000)