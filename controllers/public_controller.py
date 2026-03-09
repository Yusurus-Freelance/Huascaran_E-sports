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
        yape = request.form['operacion_yape']
        
        # Asumimos que el ID del Evento activo es 1
        id_evento_actual = 1 
        
        # Llamamos al MODELO para guardar en MySQL
        nuevo_id = EquipoModel.registrar_equipo(nombre, contacto, yape, id_evento_actual)
        
        if nuevo_id:
            flash('¡Equipo inscrito! El staff validará tu Yape pronto.', 'success')
            # Aquí podrías recorrer el request.form.getlist('integrante') y guardarlos también
        else:
            flash('Hubo un error al conectar con la base de datos.', 'error')
            
        return redirect(url_for('public.index'))
        
    return render_template('public/registro.html')

@public_bp.route('/equipos')
def lista_equipos():
    # Llamamos al modelo para traer solo los aprobados
    equipos_confirmados = EquipoModel.obtener_aprobados()
    
    return render_template('public/equipos.html', equipos=equipos_confirmados)