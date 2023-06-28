

# """
#     punto #1 Base de datos

#     TODO
#         1 - coneccion
#         2 - crear tablas
#             cajeros /cajero_id
#             transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
#             usuarios
#             cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

#         3 - C R U D
# """

# """
#     punto #2 Flask Web Server

#     TODO
#         1 - coneccion
#         2 - crear tablas
#             cajeros /cajero_id
#             transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
#             usuarios
#             cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

#         3 - C R U D
# """

# """
#     punto #3 Los hilos

#     TODO
#         1 - coneccion
#         2 - crear tablas
#             cajeros /cajero_id
#             transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
#             usuarios
#             cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

#         3 - C R U D
# """

from flask import Flask, jsonify, request
import sqlite3
import threading

#*****************************************************************************
# Instanciando servidor de flask
#*****************************************************************************
app = Flask(__name__)

#*****************************************************************************
# Conexión a la base de datos
#*****************************************************************************
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

#*****************************************************************************
# Crear un objeto de bloqueo de memoria
#*****************************************************************************
lock = threading.Lock()

#*****************************************************************************
# Creando tablas en DB
#*****************************************************************************
def crear_tabla_usuarios():
    cursor.execute("CREATE TABLE usuarios(name VARCHAR(80), email VARCHAR(80), image, rol, pin, saldo )")
    conn.commit()

#*****************************************************************************
# Creando API rutas
#*****************************************************************************

#Prueba
@app.route("/", methods = ["GET"])
def hello_world():
    return "<p>Hello, World proyecto cajeros!</p>"


#*****************************************************************************
# Create nuevo usuario
#*****************************************************************************
@app.route("/usuarios", methods = ["POST"])
def create_user():
    name = request.json['name']
    email = request.json['email']
    image = request.json['image']
    rol = request.json['rol']
    pin = request.json['pin']
    saldo = request.json['saldo']

    def insert_user():
        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('''
                INSERT INTO usuarios (name, email, image, rol, pin, saldo)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, email, image, rol, pin, saldo))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=crear_usuario, name="Insertar usuario - hilo")
    hilo.start()
    hilo.join()
    
    return jsonify({'mensaje': 'Usuario creado correctamente'}), 201

#*****************************************************************************
# Read usuarios
#*****************************************************************************
@app.route("/usuarios", methods = ["GET"])
    users = []
    def obtener_usuarios():
        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('SELECT * FROM usuarios')
            usuarios = cursor.fetchall()
            return usuarios
        finally:
            lock.release()

    # Obtener todos los usuarios en un hilo
    def obtener_usuarios_hilo():
        thread = threading.Thread(target=obtener_usuarios)
        thread.start()
        thread.join()
        
#*****************************************************************************
# Show usuario
#*****************************************************************************

#*****************************************************************************
# Update usuario
#*****************************************************************************

#*****************************************************************************
# delete usuario
#*****************************************************************************

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







# Devuelve todos los usuarios en la base de datos
@app.route('/usuarios', methods = ['GET'])
def get_users():

    usuarios_result = []

    def obtener_usuarios():
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        usuarios_result.append(usuarios)   
    
    hilo = threading.Thread(target=obtener_usuarios)
    hilo.start()
    hilo.join()
  
    usuarios = usuarios_result[0] 
    return jsonify(usuarios)




    




#*****************************************************************************
# Corriendo el servidor flask api
#*****************************************************************************
if __name__ == '__main__':
    app.run(debug=True)

#*****************************************************************************
# # Ejemplo de uso
#*****************************************************************************

# Ejemplo de uso
# crear_usuario_hilo('John Doe', 'john@example.com')
# obtener_usuarios_hilo()
# obtener_usuario_por_id_hilo(1)
# actualizar_usuario_hilo(1, 'John Smith', 'john.smith@example.com')
# eliminar_usuario_hilo(1)


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
