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
# Create nueva transferencia
#*****************************************************************************
def create_transferencia():
    sender_id = request.json['sender_id']
    receiver_id = request.json['receiver_id']
    amount = request.json['amount']
    date = datetime.datetime.now()

    def insert_transferencia():
        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('''
                INSERT INTO transferencias (sender_id, receiver_id, amount, date)
                VALUES (?, ?, ?, ?)
                ''', (sender_id, receiver_id, amount, date))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=insert_transferencia, name="Insertar transferencia - hilo")
    hilo.start()
    hilo.join()

    
    return jsonify({'msg': 'transferencia creada correctamente'}), 201

#*****************************************************************************
# Read transferencias
#*****************************************************************************
def get_transferencias():

    def get_transferencias_db(q: queue.Queue):

        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('SELECT * FROM transferencias')
            transferencias = cursor.fetchall()
           
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

        q.put_nowait(transferencias)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()
    #Obtener todos los transferencias en un hilo
    hilo = threading.Thread(target=get_transferencias_db, name="Get transferencias - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()

    return jsonify({'transferencias': result}), 200