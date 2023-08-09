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

    try:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()

        # SE DESCUENTA EL DINERO DE LA TRANSFERENCIA
        
        cursor.execute('''SELECT saldo FROM usuarios 
                            WHERE id = (?)''', (sender_id,))
            
        saldo_actual = cursor.fetchone()
    
        if saldo_actual:
            saldo_actual = saldo_actual[0]
            saldo_actualizado = int(saldo_actual) - int(amount)

            cursor.execute('''UPDATE usuarios
                            SET saldo = (?)
                            WHERE id = (?)''',
                        (saldo_actualizado, sender_id))

            # Confirmar los cambios
            conn.commit()
            print("Transferencia exitosa. Usuario que envia :", saldo_actualizado)
        else:
            print("Usuario que envia no encontrado.")


    # UPDATE DEL SALDO DEL USUARIO QUE RECIBE EL DINERO

        cursor.execute('''SELECT saldo FROM usuarios 
                          WHERE id = (?)''', (receiver_id,))
        
        saldo_actual = cursor.fetchone()
        
        if saldo_actual:
            saldo_actual = saldo_actual[0]
            saldo_actualizado = int(saldo_actual) + int(amount)

            cursor.execute('''UPDATE usuarios
                              SET saldo = (?)
                              WHERE id = (?)''',
                           (saldo_actualizado, receiver_id))

            # Confirmar los cambios
            conn.commit()
            print("Transferencia exitosa. Usuario que recibe:", saldo_actualizado)
        else:
            print("Usuario que recibe no encontrado.")
    except Exception as e:
        # En caso de error, deshacer los cambios
        conn.rollback()
        print("Error:", str(e))
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()

    
    return jsonify({'msg': 'tranferencia realizada correctamente'}), 201

# def create_transferencia():
#     sender_id = request.json['sender_id']
#     receiver_id = request.json['receiver_id']
#     amount = request.json['amount']
#     date = datetime.datetime.now()

#     def insert_transferencia():
#         # Bloquear de memoria
#         lock.acquire()

#         try:
#             cursor.execute('''
#                 INSERT INTO transferencias (sender_id, receiver_id, amount, date)
#                 VALUES (?, ?, ?, ?)
#                 ''', (sender_id, receiver_id, amount, date))
#             conn.commit()
#         finally:
#             # Liberar el bloqueo de memoria
#             lock.release()

#     hilo = threading.Thread(target=insert_transferencia, name="Insertar transferencia - hilo")
#     hilo.start()
#     hilo.join()

    
#     return jsonify({'msg': 'transferencia creada correctamente'}), 201

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