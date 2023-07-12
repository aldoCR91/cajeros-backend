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
# Create nuevo retiro
#*****************************************************************************
def create_retiro():
    user_id = request.json['user_id']
    amount = request.json['amount']
    date = datetime.datetime.now()

    def insert_retiro():
        # Bloquear de memoria
        lock.acquire()

        try:
            #get saldo actual de la cuenta
            cursor.execute('SELECT saldo FROM usuarios WHERE id = ?', (user_id,))
            saldo = cursor.fetchone()
            
            #validar cantidad solicitada
            if saldo < amount:
                return jsonify({'msg':'Saldo insuficiente'}),401

            #rebajar monto solicitado del saldo
            nuevo_saldo = saldo - amount

            #actualizar saldo en base de datos
            cursor.execute('''
                UPDATE usuarios SET saldo = ? WHERE id = ?
            ''', (saldo,user_id))
            conn.commit()

            cursor.execute('''
                INSERT INTO retiros (user_id, amount, date)
                VALUES (?, ?, ?)
                ''', (user_id, amount, date))
            conn.commit()
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

    hilo = threading.Thread(target=insert_retiro, name="Insertar retiro - hilo")
    hilo.start()
    hilo.join()

    
    return jsonify({'msg': 'retiro creado correctamente'}), 201

#*****************************************************************************
# Read retiros
#*****************************************************************************
def get_retiros():

    def get_retiros_db(q: queue.Queue):

        # Bloquear de memoria
        lock.acquire()

        try:
            cursor.execute('SELECT * FROM retiros')
            retiros = cursor.fetchall()
           
        finally:
            # Liberar el bloqueo de memoria
            lock.release()

        q.put_nowait(retiros)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()
    #Obtener todos los retiros en un hilo
    hilo = threading.Thread(target=get_retiros_db, name="Get retiros - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()

    return jsonify({'retiros': result}), 200
