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
    cajero_id = request.json['cajero_id']

    def insert_retiro():
        # Bloquear de memoria
        lock.acquire()

        try:
            #validar usuario
            cursor.execute('SELECT * FROM usuarios WHERE id = ?',(user_id))
            usuario = cursor.fetchone()
            return usuario
            #validar cajero
            #get saldo actual de la cuenta
            cursor.execute('SELECT saldo FROM usuarios WHERE id = ?', (user_id,))
            saldo_cuenta = cursor.fetchone()
            
            #validar cantidad solicitada
            if saldo_cuenta < amount:
                return jsonify({'msg':'Saldo insuficiente'}),401
            
            #get disponible en el cajero
            cursor.execute('SELECT amount FROM cajeros WHERE id = ?', (cajero_id,))
            saldo_cajero = cursor.fetchone()

            #validar efectivo del cajero
            if saldo_cajero < amount:
                return jsonify({"status":"error","msg":"Efectivo no disponible en este cajero"})

            #rebajar monto solicitado del saldo
            nuevo_saldo_cajero = saldo_cajero - amount

            #rebajar monto solicitado del saldo
            nuevo_saldo = saldo_cuenta - amount

            #rebajar disponible en el cajero
            cursor.execute('''
                           UPDATE cajeros SET amount ? WHERE id = ?
                           ''',(nuevo_saldo_cajero,cajero_id))

            #actualizar saldo en base de datos
            cursor.execute('''
                UPDATE usuarios SET saldo = ? WHERE id = ?
            ''', (nuevo_saldo,user_id))
            conn.commit()

            #crear registro del retiro en la base de datos
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
