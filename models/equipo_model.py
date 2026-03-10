from config.db import get_db_connection

class EquipoModel:
    @staticmethod
    def registrar_equipo(nombre, contacto, fecha_yape, id_evento, integrantes, logo_url): # 1. Agregamos logo_url aquí
        conexion = get_db_connection()
        if not conexion:
            return False
            
        try:
            with conexion.cursor() as cursor:
                # 2. Agregamos el último %s en VALUES para que coincida con la columna 'logo'
                sql_equipo = """INSERT INTO Equipos 
                                (nombre, nombre_contacto, contacto, fecha_yapeo, estado_validacion, fecha_creacion, idEventos, logo) 
                                VALUES (%s, %s, %s, %s, 'no', NOW(), %s, %s)"""
                                
                # Pasamos la variable logo_url en la ejecución
                cursor.execute(sql_equipo, (nombre, "Contacto Web", contacto, fecha_yape, id_evento, logo_url))
                
                # Capturamos el ID del equipo que se acaba de crear
                id_equipo_nuevo = cursor.lastrowid 
                
                # Insertamos a los integrantes vinculados a ese ID de equipo
                sql_integrante = "INSERT INTO Integrantes (apodo, idEquipos) VALUES (%s, %s)"
                for nick in integrantes:
                    if nick.strip(): # Solo lo guardamos si el campo no estaba vacío
                        cursor.execute(sql_integrante, (nick, id_equipo_nuevo))
                
                # Confirmamos TODOS los cambios en la base de datos
                conexion.commit()
                return True
                
        except Exception as e:
            print(f"Error crítico al registrar: {e}")
            if conexion:
                conexion.rollback() # Si algo falla, deshacemos la creación del equipo
            return False
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def obtener_pendientes():
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM Equipos WHERE estado_validacion = 'no'"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conexion.close()
            
    @staticmethod
    def obtener_aprobados():
        conexion = get_db_connection()
        if not conexion:
            return []
            
        try:
            with conexion.cursor() as cursor:
                # 3. Agregamos 'logo' a la consulta para poder mostrar la imagen en el HTML
                sql = "SELECT nombre, logo, fecha_creacion FROM Equipos WHERE estado_validacion = 'si'"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error en Modelo obtener_aprobados: {e}")
            return []
        finally:
            conexion.close()
            
    @staticmethod
    def aprobar_equipo(id_equipo, id_staff):
        conexion = get_db_connection()
        if not conexion:
            return False
            
        try:
            with conexion.cursor() as cursor:
                # Actualizamos el estado y le pasamos el idStaff_temporal para que el trigger lo capture
                sql = """UPDATE Equipos 
                         SET estado_validacion = 'si', idStaff_temporal = %s 
                         WHERE idEquipos = %s"""
                cursor.execute(sql, (id_staff, id_equipo))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error en Modelo aprobar_equipo: {e}")
            return False
        finally:
            if conexion:
                conexion.close()
    
    @staticmethod
    def obtener_pendientes():
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # Agregamos 'logo' a la consulta SQL
                sql = "SELECT idEquipos, nombre, contacto, fecha_creacion, fecha_yapeo, logo FROM Equipos WHERE estado_validacion = 'no'"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            if conexion:
                conexion.close()
                
    @staticmethod
    def obtener_detalle_completo(id_equipo):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # 1. Traer datos del equipo
                sql_equipo = "SELECT idEquipos, nombre, logo, fecha_creacion FROM Equipos WHERE idEquipos = %s AND estado_validacion = 'si'"
                cursor.execute(sql_equipo, (id_equipo,))
                equipo = cursor.fetchone()
                
                if equipo:
                    # 2. Traer sus integrantes
                    sql_integrantes = "SELECT apodo FROM Integrantes WHERE idEquipos = %s"
                    cursor.execute(sql_integrantes, (id_equipo,))
                    equipo['integrantes'] = cursor.fetchall()
                
                return equipo
        finally:
            conexion.close()