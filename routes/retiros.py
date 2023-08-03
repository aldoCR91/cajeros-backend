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
# Update Amount 
#*****************************************************************************
def Update_Amount():
    user_id = request.json['user_id']
    amount = request.json['amount']

    try:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT Saldo FROM Usuarios 
                          WHERE id = (?)''', (user_id,))
        saldo_actual = cursor.fetchone()
        
        if saldo_actual:
            saldo_actual = saldo_actual[0]
            saldo_actualizado = int(saldo_actual) - int(amount)

            cursor.execute('''UPDATE Usuarios
                              SET Saldo = (?)
                              WHERE id = (?)''',
                           (saldo_actualizado, user_id))

            # Confirmar los cambios
            conn.commit()
            print("Retiro exitoso. Saldo actualizado:", saldo_actualizado)
        else:
            print("Usuario no encontrado.")
    except Exception as e:
        # En caso de error, deshacer los cambios
        conn.rollback()
        print("Error:", str(e))
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()

    
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
            cursor.close()
            conn.close()

        q.put_nowait(retiros)

    # Cola para guardar el resultado del hilo.
    q = queue.Queue()
    #Obtener todos los retiros en un hilo
    hilo = threading.Thread(target=get_retiros_db, name="Get retiros - hilo", args=(q,))
    hilo.start()
    hilo.join()

    result = q.get_nowait()

    return jsonify({'retiros': result}), 200