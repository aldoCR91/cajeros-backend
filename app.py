

from flask import Flask, jsonify, request
import sqlite3
import threading
import queue

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
# Creando tabla usuarios en DB
#*****************************************************************************
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT ,name VARCHAR(80), email VARCHAR(80), image, rol, pin, saldo )")
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
@app.route('/usuarios', methods = ['POST'])
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

    hilo = threading.Thread(target=insert_user, name="Insertar usuario - hilo")
    hilo.start()
    hilo.join()
    
    return jsonify({'mensaje': 'Usuario creado correctamente'}), 201

#*****************************************************************************
# Read usuarios
#*****************************************************************************
@app.route('/usuarios', methods = ["GET"])
def get_users():

    def get_users_db(q: queue.Queue):

        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('SELECT * FROM usuarios')
            usuarios = cursor.fetchall()
           
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

        q.put_nowait(usuarios)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()
    #Obtener todos los usuarios en un hilo
    hilo = threading.Thread(target=get_users_db, name="Get users - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()

    return jsonify({'usuarios': result}), 200
        
#*****************************************************************************
# Show usuario
#*****************************************************************************
@app.route("/usuario/<int:id>", methods = ["GET"])
def get_user(id):

    def get_user_db(q: queue.Queue):
        # Adquirir el bloqueo de memoria
        lock.acquire()
        try:
            cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
            usuario = cursor.fetchone()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
        
        q.put_nowait(usuario)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()

    hilo = threading.Thread(target=get_user_db, name="Show user - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()

    return jsonify({'usuario': result }), 200
         

        
#*****************************************************************************
# Update usuario
#*****************************************************************************
@app.route('/usuario/<int:id>', methods=['PUT'])
def update_user(id):
    rol = request.json['rol']
    pin = request.json['pin']
    saldo = request.json['saldo']

    def update_user_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()

        try:
            cursor.execute('''
                UPDATE usuarios SET rol = ?, pin = ?, saldo = ? WHERE id = ?
            ''', (rol,pin,saldo,id))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=update_user_db, name="Update user - hilo")
    hilo.start()
    hilo.join()

    return jsonify({'msg': 'Usuario actualizado correctamente' }), 201

#*****************************************************************************
# delete usuario
#*****************************************************************************

# Función para leer un usuario por ID
# def obtener_usuario_por_id(id):
#     cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
#     usuario = cursor.fetchone()
#     return usuario



# Función para actualizar un usuario
# def actualizar_usuario(id, nombre, email):
#     cursor.execute('''
#         UPDATE usuarios
#         SET nombre = ?, email = ?
#         WHERE id = ?
#     ''', (nombre, email, id))
#     conn.commit()

# Función para eliminar un usuario
# def eliminar_usuario(id):
#     cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
#     conn.commit()





#*****************************************************************************
# Implementando metodos en hilos
#*****************************************************************************



# # Obtener un usuario por ID en un hilo
# def obtener_usuario_por_id_hilo(id):
#     thread = threading.Thread(target=obtener_usuario_por_id, args=(id,))
#     thread.start()

# # Actualizar un usuario en un hilo
# def actualizar_usuario_hilo(id, nombre, email):
#     thread = threading.Thread(target=actualizar_usuario, args=(id, nombre, email))
#     thread.start()

# # Eliminar un usuario en un hilo
# def eliminar_usuario_hilo(id):
#     thread = threading.Thread(target=eliminar_usuario, args=(id,))
#     thread.start()







# # Devuelve todos los usuarios en la base de datos
# @app.route('/usuarios', methods = ['GET'])
# def get_users():

#     usuarios_result = []

#     def obtener_usuarios():
#         cursor.execute('SELECT * FROM usuarios')
#         usuarios = cursor.fetchall()
#         usuarios_result.append(usuarios)   
    
#     hilo = threading.Thread(target=obtener_usuarios)
#     hilo.start()
#     hilo.join()
  
#     usuarios = usuarios_result[0] 
#     return jsonify(usuarios)




    




#*****************************************************************************
# Corriendo el servidor flask api
#*****************************************************************************
if __name__ == '__main__':
    app.run(debug=True)




# Cerrar la conexión a la base de datos
#conn.close()

