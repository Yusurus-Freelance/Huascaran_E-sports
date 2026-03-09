from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.staff_model import StaffModel
from models.equipo_model import EquipoModel

# Importante: Definimos el Blueprint y le ponemos un prefijo a las URLs
staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        # Llamamos al modelo para verificar en MySQL
        staff = StaffModel.verificar_credenciales(usuario, password)
        
        if staff:
            # Agrégale la "s" aquí también:
            session['staff_id'] = staff['idStaffs'] 
            session['staff_user'] = staff['usuario']
            return redirect(url_for('staff.dashboard'))
        else:
            flash('Credenciales incorrectas.', 'error')
            
    return render_template('staff/login.html')

@staff_bp.route('/dashboard')
def dashboard():
    # Protegemos la ruta
    if 'staff_id' not in session:
        return redirect(url_for('staff.login'))
        
    # Traemos los equipos pendientes desde la BD
    equipos_pendientes = EquipoModel.obtener_pendientes()
    return render_template('staff/dashboard.html', equipos=equipos_pendientes)

@staff_bp.route('/logout')
def logout():
    session.clear() # Destruye la sesión
    return redirect(url_for('public.index'))

@staff_bp.route('/aprobar/<int:id_equipo>', methods=['POST'])
def aprobar(id_equipo):
    # Verificamos que el staff siga logueado
    if 'staff_id' not in session:
        return redirect(url_for('staff.login'))
        
    # Obtenemos el ID del staff desde la sesión actual
    id_staff_actual = session['staff_id']
    
    # Ejecutamos la actualización
    exito = EquipoModel.aprobar_equipo(id_equipo, id_staff_actual)
    
    if exito:
        flash('¡Equipo validado exitosamente!', 'success')
    else:
        flash('Hubo un error al validar el equipo.', 'error')
        
    # Recargamos el panel
    return redirect(url_for('staff.dashboard'))