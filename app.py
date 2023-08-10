

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import threading
import datetime

from routes.prueba import hello_world
from routes.user import create_user, get_users, get_user, update_user_saldo,update_user_pin,update_user_rol, delete_user, delete_all_users
from routes.cajeros import create_cajero, get_cajeros, get_cajero, update_cajero, delete_cajero
from routes.depositos import create_deposito, get_depositos , add_deposito
from routes.retiros import create_retiro, get_retiros , Update_Amount
from routes.transferencias import create_transferencia, get_transferencias

#*****************************************************************************
# Instanciando servidor de flask
#*****************************************************************************
app = Flask(__name__)
CORS(app)



# HOLA ESTO ES UN COMENTARIO 

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
# Creando tablas en DB
#*****************************************************************************
cursor.execute(
    """CREATE TABLE IF NOT EXISTS 
       usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT,
       name VARCHAR(80),
       email VARCHAR(80) UNIQUE,
       image, rol, pin, saldo )""") # Creando tabla de usuarios en la base de datos
conn.commit()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS 
       cajeros(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       state ,
       amount INTEGER)""") # Creando tabla de cajeros en la base de datos
conn.commit()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS 
       depositos(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER,
       amount INTEGER,
       date TIMESTAMP,
       foreign key(user_id) references usuarios(id) )""") # Creando tabla de depositos en la base de datos
conn.commit()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS 
       retiros(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER,
       amount INTEGER,
       date TIMESTAMP,
       foreign key(user_id) references usuarios(id))""") # Creando tabla de retiros en la base de datos
conn.commit()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS 
       transferencias(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       sender_id INTEGER,
       receiver_id INTEGER,
       amount INTEGER,
       date TIMESTAMP,
       foreign key(sender_id) references usuarios(id),
       foreign key(receiver_id) references usuarios(id))""") # Creando tabla de transferencias en la base de datos
conn.commit()


#Ruta de prueba
app.route('/prueba', methods = ['POST'])(hello_world)
#*****************************************************************************
# Creando API rutas de usuarios
#*****************************************************************************
app.route('/usuarios', methods = ['POST'])(create_user) # Create user
app.route('/usuarios', methods = ["GET"])(get_users) # Get users
app.route("/usuario/<email>", methods = ["GET"])(get_user) # get user

app.route('/usuario/update/saldo/<int:id>', methods=['PUT'])(update_user_saldo) # Update usuario saldo 
app.route('/usuario/update/rol/<int:id>', methods=['PUT'])(update_user_rol) # Update usuario rol
app.route('/usuario/update/pin/<int:id>', methods=['PUT'])(update_user_pin) # Update usuario pin

app.route('/usuario/<int:id>', methods=['DELETE'])(delete_user) # delete usuario 
app.route('/usuario/delete/all/users', methods=['DELETE'])(delete_all_users) # delete usuario        

#*****************************************************************************
# Creando API rutas de cajeros
#*****************************************************************************
app.route('/cajero', methods = ['POST'])(create_cajero) # Create nuevo cajero
app.route('/cajeros', methods = ["GET"])(get_cajeros) # Read cajeros
app.route("/cajero/<int:id>", methods = ["GET"])(get_cajero) # Show cajero
app.route('/cajero/<int:id>', methods=['PUT'])(update_cajero) # Update cajero
app.route('/cajero/<int:id>', methods=['DELETE'])(delete_cajero) # delete cajero

#*****************************************************************************
# Creando API rutas de depositos
#*****************************************************************************
app.route('/deposito', methods = ['POST'])(add_deposito) # Agrega Deposito a Tabla depositos
app.route('/depositos', methods = ["GET"])(get_depositos) # Read depositos
app.route('/depositos', methods = ["POST"])(create_deposito) # Create deposito

#*****************************************************************************
# Creando API rutas de retiros
#*****************************************************************************
app.route('/retiro', methods = ['POST'])(create_retiro) # Create nuevo retiro
app.route('/retiros', methods = ["GET"])(get_retiros) # Read retiros
app.route('/retiros', methods = ["POST"])(Update_Amount) # Update saldo(cajero y usuario)retiros

#*****************************************************************************
# Creando API rutas de transferencias
#*****************************************************************************
app.route('/transferencias', methods = ['POST'])(create_transferencia) # Create nuevo transferencia

app.route('/transferencias', methods = ["GET"])(get_transferencias) # Read transferencias


#*****************************************************************************
# Corriendo el servidor flask api
#*****************************************************************************
if __name__ == '__main__':
    app.run(debug=True)




# Cerrar la conexión a la base de datos
#conn.close()

