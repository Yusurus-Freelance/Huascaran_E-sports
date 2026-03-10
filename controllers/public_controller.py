import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.equipo_model import EquipoModel

# Creamos el Blueprint para las rutas públicas
public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    return render_template('public/index.html')

@public_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre_equipo']
        contacto = request.form['contacto']
        fecha_yape = request.form['fecha_yapeo']
        integrantes = request.form.getlist('integrante')
        id_evento_actual = 1 
        
        # --- LÓGICA DE SUBIDA A LA NUBE ---
        logo_url = None
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename != '':
                try:
                    # Subimos el archivo directamente a Cloudinary
                    respuesta = cloudinary.uploader.upload(file, folder="huascaran_esports")
                    # Extraemos el link seguro (https)
                    logo_url = respuesta.get('secure_url')
                except Exception as e:
                    print(f"Error subiendo imagen a Cloudinary: {e}")
        # ----------------------------------
        
        # Le enviamos la URL (texto) al modelo
        exito = EquipoModel.registrar_equipo(nombre, contacto, fecha_yape, id_evento_actual, integrantes, logo_url)
        
        if exito:
            flash('✅ ¡Tu equipo fue registrado con éxito! Tu inscripción está en estado PENDIENTE.', 'success')
        else:
            flash('Hubo un error al guardar los datos. Intenta nuevamente.', 'error')
            
        return redirect(url_for('public.index'))
        
    return render_template('public/registro.html')

@public_bp.route('/equipos')
def lista_equipos():
    # Llamamos al modelo para traer solo los aprobados
    equipos_confirmados = EquipoModel.obtener_aprobados()
    
    return render_template('public/equipos.html', equipos=equipos_confirmados)
