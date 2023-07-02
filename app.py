

from flask import Flask, jsonify, request
import sqlite3
import threading
import queue

from routes.prueba import hello_world
from routes.user import create_user, get_users, get_user, update_user, delete_user

#*****************************************************************************
# Instanciando servidor de flask
#*****************************************************************************
app = Flask(__name__)

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
# Creando tabla usuarios en DB
#*****************************************************************************
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT ,name VARCHAR(80), email VARCHAR(80), image, rol, pin, saldo )")
conn.commit()


#Ruta de prueba
app.route('/', methods = ['GET'])(hello_world)
#*****************************************************************************
# Creando API rutas de usuarios
#*****************************************************************************
app.route('/usuarios', methods = ['POST'])(create_user) # Create nuevo usuario
app.route('/usuarios', methods = ["GET"])(get_users) # Read usuarios
app.route("/usuario/<int:id>", methods = ["GET"])(get_user) # Show usuario
app.route('/usuario/<int:id>', methods=['PUT'])(update_user) # Update usuario
app.route('/usuario/<int:id>', methods=['DELETE'])(delete_user) # delete usuario        



#*****************************************************************************
# Corriendo el servidor flask api
#*****************************************************************************
if __name__ == '__main__':
    app.run(debug=True)




# Cerrar la conexión a la base de datos
#conn.close()

