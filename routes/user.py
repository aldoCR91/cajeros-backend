from flask import jsonify, request
import sqlite3
import threading
import queue

### Esta es una prueba de git 
### para trabajar en equipo

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
    

    # Revisar si ya existe un usuario en ese email
    user = user_exist(email=email)
    print("user 34" ,user)

    def insert_user():
        # Bloquear de memoria
        lock.acquire()
        try:
            cursor.execute('''
                INSERT INTO usuarios (name, email, image, rol, pin, saldo, state)
                VALUES (?, ?, ?, ?, ?, ?, "activo")
                ''', (name, email, image, rol, pin, saldo,))
            conn.commit()
        except:
            return jsonify({
                'ok': False,
                'msg': 'Error al insertar usuario'
                }), 400
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
    
    if(user):
        return jsonify({'ok': False,
                        'msg': 'Ya existe un usuario con este email user 56'
                        }), 401
    else:
        hilo = threading.Thread(target=insert_user, name="Insertar usuario - hilo")
        hilo.start()
        hilo.join()
        return jsonify({
            'mensaje': 'Usuario creado correctamente',
            'ok': True,
            'email': email}), 201

    

    

    
    

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
def get_user(email):

    # email = request.json['email']

    def get_user_db(q: queue.Queue):
        # Adquirir el bloqueo de memoria
        lock.acquire()
        try:
            cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
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

    if result != None:
        user = {"id": result[0],
                "name":result[1],
                "email":result[2],
                "image":result[3],
                "rol":result[4],
                "pin":result[5],
                "saldo":result[6],
                "state":result[7]}
        return jsonify(user), 200

    return jsonify(result), 404

    


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


def user_exist(email):

    lock.acquire()

    try:
        cursor.execute('''SELECT * FROM usuarios WHERE email = ? ''',(email,))
        usuario = cursor.fetchone()
    finally:
        lock.release()
    
    return usuario