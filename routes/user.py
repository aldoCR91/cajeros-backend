from flask import jsonify, request
import sqlite3
import threading
import queue

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
# Create nuevo usuario
#*****************************************************************************
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

        exist = user_exist(email)

        if(!exist):
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
# user exist
#*****************************************************************************
def user_exist(email):
    try:
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
    except:
        return False

    if usuario == None:
        return False
    if len(usuario) > 0:
        return True
        

#*****************************************************************************
# Update usuario
#*****************************************************************************
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
def delete_user(id):
    def delete_user_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()
        
        try:
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
    
    hilo = threading.Thread(target=delete_user_db, name='delete user - hilo')
    hilo.start()
    hilo.join()
    
    return jsonify({'msg': 'Usuario eliminado exitosamente'}), 200
