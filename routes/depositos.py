from flask import jsonify, request
import sqlite3
import threading
import queue
import datetime

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
# Create nuevo deposito
#*****************************************************************************
def create_deposito():
    user_id = request.json['user_id']
    amount = request.json['amount']
    date = datetime.datetime.now()

    #validar usuario
    def validate_user():
        # Bloquear memoria
        lock.acquire()

        #variable de retorno
        user_exist = FALSE
        
        try:
            #getting user
            cursor.execute('''
                SELECT * FROM usuarios WHERE id = ?
                ''',(user_id,)
            user = cursor.fetchone()
            
            #si el usuario es distinto de none
            if user is not NONE:
                user_exist = TRUE
                
                
        finally:
            # Liberar el bloqueo de memoria
            lock.release()
        
        return user_exist

    #insertar registro en la tabla de depositos
    def insert_deposito(q: queue.Queue):
        
        # Bloquear de memoria
        lock.acquire()

        try:
            if validate_amount and validate_user():
                cursor.execute('''
                    INSERT INTO depositos (user_id, amount, date)
                    VALUES (?, ?, ?)
                    ''', (user_id, amount, date))
                conn.commit()
            
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

        q.put_nowait(depositos)

    hilo = threading.Thread(target=insert_deposito, name="Insertar deposito - hilo")
    hilo.start()
    hilo.join()

    
    return jsonify({'msg': 'deposito creado correctamente'}), 201

#*****************************************************************************
# Read depositos
#*****************************************************************************
def get_depositos():

    def get_depositos_db(q: queue.Queue):

        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('SELECT * FROM depositos')
            depositos = cursor.fetchall()
           
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

        q.put_nowait(depositos)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()
    #Obtener todos los depositos en un hilo
    hilo = threading.Thread(target=get_depositos_db, name="Get depositos - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()

    return jsonify({'depositos': result}), 200


#*****************************************************************************
# Show deposito
#*****************************************************************************
# def get_deposito(id):

#     def get_deposito_db(q: queue.Queue):
#         # Adquirir el bloqueo de memoria
#         lock.acquire()
#         try:
#             cursor.execute('SELECT * FROM depositos WHERE id = ?', (id,))
#             deposito = cursor.fetchone()
#         finally:
#             # Liberar el bloqueo de memoria
#             lock.release()
        
#         q.put_nowait(deposito)

#     # Cola para guardar el resultado del hilo.
#     q = queue.Queue()

#     hilo = threading.Thread(target=get_deposito_db, name="Show deposito - hilo", args=(q,))
#     hilo.start()
#     hilo.join()

#     result = q.get_nowait()

#     return jsonify({'deposito': result }), 200


#*****************************************************************************
# Update deposito
#*****************************************************************************
# def update_deposito(id):
#     rol = request.json['rol']
#     pin = request.json['pin']
#     saldo = request.json['saldo']

#     def update_deposito_db():
#         # Adquirir el bloqueo de memoria
#         lock.acquire()

#         try:
#             cursor.execute('''
#                 UPDATE depositos SET rol = ?, pin = ?, saldo = ? WHERE id = ?
#             ''', (rol,pin,saldo,id))
#             conn.commit()
#         finally:
#             # Liberar el bloqueo de memoria
#             lock.release()

#     hilo = threading.Thread(target=update_deposito_db, name="Update deposito - hilo")
#     hilo.start()
#     hilo.join()

#     return jsonify({'msg': 'deposito actualizado correctamente' }), 201

#*****************************************************************************
# delete deposito
#*****************************************************************************
# def delete_deposito(id):
#     def delete_deposito_db():
#         # Adquirir el bloqueo de memoria
#         lock.acquire()
        
#         try:
#             cursor.execute('DELETE FROM depositos WHERE id = ?', (id,))
#             conn.commit()
#         finally:
#             # Liberar el bloqueo de memoria
#             lock.release()
    
#     hilo = threading.Thread(target=delete_deposito_db, name='delete deposito - hilo')
#     hilo.start()
#     hilo.join()
    
#     return jsonify({'msg': 'deposito eliminado exitosamente'}), 200

#validar amount
def validate_amount():
    value = TRUE
    if type(amount) != type(1) or type(amount) != type(1.1) or amount < 0:
        value = FALSE
    return value
