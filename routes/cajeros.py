from flask import jsonify, request, abort
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
def create_cajero():

    user_email = request.json['email']

    #validar usuario
    def validar_usuario():
        

        lock.acquire()

        try:
            cursor.execute('''SELECT * FROM usuarios WHERE email = ?''',(user_email,))
            user = cursor.fetchone()

            #validar que el usuario exista
            if user is None:
                return {"status":"error",
                        "msg":"usuario no encontrado"}


            #validar que el usuario sea admin
            if user[4] != "admin":
                return {"status":"error",
                        "msg":"usuario no autorizado"}
        finally:
            lock.release()
    
    print(validar_usuario())

    def insert_cajero():
        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('''
                INSERT INTO cajeros (state, amount)
                VALUES (?, ?)
                ''', ("Disponible",10000000))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=insert_cajero, name="Insertar cajero - hilo")
    hilo.start()
    hilo.join()

    
    return jsonify({'msg': 'Cajero creado correctamente'}), 201

#*****************************************************************************
# Read usuarios
#*****************************************************************************
def get_cajeros():

    def get_cajeros_db(q: queue.Queue):

        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('SELECT * FROM cajeros')
            cajeros = cursor.fetchall()
           
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

        q.put_nowait(cajeros)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()
    #Obtener todos los usuarios en un hilo
    hilo = threading.Thread(target=get_cajeros_db, name="Get cajeros - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()


    return jsonify(result), 200


#*****************************************************************************
# Show usuario
#*****************************************************************************
def get_cajero(id):

    def get_cajero_db(q: queue.Queue):
        # Adquirir el bloqueo de memoria
        lock.acquire()
        try:
            cursor.execute('SELECT * FROM cajeros WHERE id = ?', (id,))
            cajero = cursor.fetchone()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
        
        q.put_nowait(cajero)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()

    hilo = threading.Thread(target=get_cajero_db, name="Show cajero - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()

    return jsonify({'cajero': result }), 200


#*****************************************************************************
# Update usuario
#*****************************************************************************
def update_cajero(id):
    state = request.json['state']
    amount = request.json['amount']
    

    def update_cajero_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()

        try:
            cursor.execute('''
                UPDATE cajeros SET state = ?, amount = ? WHERE id = ?
            ''', (state, amount, id))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=update_cajero_db, name="Update cajero - hilo")
    hilo.start()
    hilo.join()

    return jsonify({'msg': 'Cajero actualizado correctamente' }), 201

#*****************************************************************************
# delete usuario
#*****************************************************************************
def delete_cajero(id):
    def delete_cajero_db():
        # Adquirir el bloqueo de memoria
        lock.acquire()
        
        try:
            cursor.execute('DELETE FROM cajeros WHERE id = ?', (id,))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
    
    hilo = threading.Thread(target=delete_cajero_db, name='delete cajero - hilo')
    hilo.start()
    hilo.join()
    
    return jsonify({'msg': 'Cajero eliminado exitosamente'}), 200