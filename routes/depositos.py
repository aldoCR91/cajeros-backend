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

    def insert_deposito():
        # Bloquear de memoria
        lock.acquire()

        try:
            #get saldo actual del usuario
            cursor.execute('''SELECT saldo FROM usuarios WHERE id ''',(user_id))
            saldo = cursor.fetchone()
            
            #sumar al saldo actual el monto del deposito
            nuevo_saldo = amount + saldo
            
            #guardar saldo despues del deposito en base de datos
            curso.execute('''UPDATE usuarios SET saldo = ? WHERE id = ?
            ''', (nuevo_saldo,user_id))
            conn.commit()

            #insertar nuevo registro en la tabla de depositos
            cursor.execute('''
                INSERT INTO depositos (user_id, amount, date)
                VALUES (?, ?, ?)
                ''', (user_id, amount, date))
            conn.commit()
            
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

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
