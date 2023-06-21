

"""
    punto #1 Base de datos

    TODO
        1 - coneccion
        2 - crear tablas
            cajeros /cajero_id
            transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
            usuarios
            cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

        3 - C R U D
"""

"""
    punto #2 Flask Web Server

    TODO
        1 - coneccion
        2 - crear tablas
            cajeros /cajero_id
            transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
            usuarios
            cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

        3 - C R U D
"""

"""
    punto #3 Los hilos

    TODO
        1 - coneccion
        2 - crear tablas
            cajeros /cajero_id
            transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
            usuarios
            cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

        3 - C R U D
"""


import sqlite3
import threading

# Conexión a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


#*****************************************************************************
# Creando CRUD con la base de datos
#*****************************************************************************

# Función para leer todos los usuarios
def obtener_usuarios():
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    return usuarios

# Función para leer un usuario por ID
def obtener_usuario_por_id(id):
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
    usuario = cursor.fetchone()
    return usuario

# Función para actualizar un usuario
def actualizar_usuario(id, nombre, email):
    cursor.execute('''
        UPDATE usuarios
        SET nombre = ?, email = ?
        WHERE id = ?
    ''', (nombre, email, id))
    conn.commit()

# Función para eliminar un usuario
def eliminar_usuario(id):
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()



#*****************************************************************************
# Implementando metodos en hilos
#*****************************************************************************

# Obtener todos los usuarios en un hilo
def obtener_usuarios_hilo():
    thread = threading.Thread(target=obtener_usuarios)
    thread.start()

# Obtener un usuario por ID en un hilo
def obtener_usuario_por_id_hilo(id):
    thread = threading.Thread(target=obtener_usuario_por_id, args=(id,))
    thread.start()

# Actualizar un usuario en un hilo
def actualizar_usuario_hilo(id, nombre, email):
    thread = threading.Thread(target=actualizar_usuario, args=(id, nombre, email))
    thread.start()

# Eliminar un usuario en un hilo
def eliminar_usuario_hilo(id):
    thread = threading.Thread(target=eliminar_usuario, args=(id,))
    thread.start()


#*****************************************************************************
# # Ejemplo de uso
#*****************************************************************************

# Ejemplo de uso
# crear_usuario_hilo('John Doe', 'john@example.com')
# obtener_usuarios_hilo()
# obtener_usuario_por_id_hilo(1)
# actualizar_usuario_hilo(1, 'John Smith', 'john.smith@example.com')
# eliminar_usuario_hilo(1)

# Corriendo servidor
if __name__ == '__main__':
    socketio.run(app)
# Cerrar la conexión a la base de datos
conn.close()


# Crear tablas en la base de datos cajeros.db
#cur.execute("CREATE TABLE usuarios(name, email, pin)")
#cur.execute("CREATE TABLE cajeros( codigo, stado, disponible)")

# cur.execute("""
#     INSERT INTO usuarios VALUES
#         ('Yari', 'yari@cuc.cr', 1234),
#         ('Aldo', 'aldo@cuc.cr', 1234)
# """)

# cur.execute("""
#     INSERT INTO cajeros VALUES
#         ('01', 'ocupado', 10000000),
#         ('02', 'disponible', 7500000)
# """)
            
# con.commit()
            
#res = cur.execute("SELECT * FROM cajeros")
# res.fetchall()

# for row in cur.execute("SELECT * FROM cajeros"):
#     print(row)

# #print(res)
# con.close()




#con.commit()
