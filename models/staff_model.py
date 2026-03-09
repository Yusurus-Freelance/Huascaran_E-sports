from config.db import get_db_connection

class StaffModel:
    @staticmethod
    def verificar_credenciales(usuario, password):
        conexion = get_db_connection()
        if not conexion:
            return None
            
        try:
            with conexion.cursor() as cursor:
                # Buscamos al usuario en la BD
                # Cambia esta línea:
                sql = "SELECT idStaffs, usuario, password_hash FROM Staffs WHERE usuario = %s"
                cursor.execute(sql, (usuario,))
                staff = cursor.fetchone()
                
                # Por ahora hacemos una validación directa (luego puedes agregar el hash real)
                if staff and staff['password_hash'] == password: 
                    return staff
                return None
        except Exception as e:
            print(f"Error en Modelo verificar_credenciales: {e}")
            return None
        finally:
            conexion.close()