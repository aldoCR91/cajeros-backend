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

        not_exist = user_not_exist(email)

        try:
            if not_exist:
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

    
    return jsonify({'mensaje': 'Usuario creado correctamente', }), 201

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
# Get usuario
#*****************************************************************************
def get_user(email):

    def get_user_db(q: queue.Queue):
        # Adquirir el bloqueo de memoria
        lock.acquire()

        try:
            cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
            usuario = cursor.fetchone()
            #print(usuario)
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
        
        q.put(usuario)


    # Cola para guardar el resultado del hilo.
    q = queue.Queue()

    hilo = threading.Thread(target=get_user_db, name="Show user - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()
    print("*********** 112",result)

    user = {"id":result[0],
            "name":result[1],
            "email":result[2],
            "image":result[3],
            "rol":result[4],
            "pin":result[5],
            "saldo":result[6]}
    

    if result == None:
        return jsonify({}), 404
    else:
        return jsonify(user), 200

    

#*****************************************************************************
# user exist
#*****************************************************************************
def user_not_exist(email):
    try:
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
    except:
        return False

    if usuario == None:
        return True
    if len(usuario) > 0:
        return False
        

#*****************************************************************************
# Update user saldo
#*****************************************************************************
def update_user_saldo(id):

    saldo = request.json['saldo']

    def update_user_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()

        try:
            cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (saldo,id))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=update_user_db, name="Update user - hilo")
    hilo.start()
    hilo.join()

    return jsonify({'msg': 'Saldo acutualizado' }), 201

#*****************************************************************************
# Update user pin
#*****************************************************************************
def update_user_pin(id):

    pin = request.json['pin']

    def update_user_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()

        try:
            cursor.execute('UPDATE usuarios SET pin = ? WHERE id = ?', (pin,id))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=update_user_db, name="Update user - hilo")
    hilo.start()
    hilo.join()

    return jsonify({'msg': 'Pin acutualizado' }), 201

#*****************************************************************************
# Update user rol
#*****************************************************************************
def update_user_rol(id):

    rol = request.json['rol']

    def update_user_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()

        try:
            cursor.execute('UPDATE usuarios SET rol = ? WHERE id = ?', (rol,id))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=update_user_db, name="Update user - hilo")
    hilo.start()
    hilo.join()

    return jsonify({'msg': 'Saldo acutualizado' }), 201

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

#*****************************************************************************
# delete usuarios
#*****************************************************************************
def delete_all_users():
    def delete_users_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()
        
        try:
            cursor.execute('DELETE FROM usuarios')
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
    
    hilo = threading.Thread(target=delete_users_db, name='delete all users - hilo')
    hilo.start()
    hilo.join()
    
    return jsonify({'msg': 'todos los usuarios han sido borrados'}), 200


def Get_Saldo_User(id):
    user_id = request.json['user_id']
    saldoUsuario = 0
    def Get_Saldo_UserDB():
        # Adquirir el bloqueo de memoria
        try:
            cursor.execute('SELECT saldo FROM usuarios WHERE id = ?', (user_id))
            saldoUsuario = cursor.fetchone()

            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            print("")
            
    hilo = threading.Thread(target=Get_Saldo_UserDB, name='get saldo user - hilo')
    hilo.start()
    hilo.join()
    
    return jsonify(saldoUsuario), 200