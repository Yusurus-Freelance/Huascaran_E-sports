from config.db import get_db_connection

class EquipoModel:
    @staticmethod
    def registrar_equipo(nombre, contacto, yape, id_evento):
        conexion = get_db_connection()
        if not conexion:
            return False
            
        try:
            with conexion.cursor() as cursor:
                # Insertamos el equipo con estado 'no' (pendiente)
                sql = """INSERT INTO Equipos 
                         (nombre, nombre_contacto, contacto, estado_validacion, fecha_creacion, idEventos) 
                         VALUES (%s, %s, %s, 'no', NOW(), %s)"""
                # Nota: Ajusté 'nombre_contacto' a un valor genérico temporal para el ejemplo
                cursor.execute(sql, (nombre, "Contacto Web", contacto, id_evento))
                
                conexion.commit()
                return cursor.lastrowid # Devuelve el ID del equipo recién creado
        except Exception as e:
            print(f"Error en Modelo registrar_equipo: {e}")
            return False
        finally:
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
                # Solo traemos los equipos que ya fueron validados
                sql = "SELECT nombre, fecha_creacion FROM equipos WHERE estado_validacion = 'si'"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error en Modelo obtener_aprobados: {e}")
            return []
        finally:
            conexion.close()