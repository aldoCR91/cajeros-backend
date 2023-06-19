

"""
    punto #1 Base de datos

    TODO
        1 - coneccion
        2 - crear tablas
            cajeros /cajero_id
            transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
            usuarios
            cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

        3 - C R U D
"""

"""
    punto #2 Flask Web Server

    TODO
        1 - coneccion
        2 - crear tablas
            cajeros /cajero_id
            transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
            usuarios
            cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

        3 - C R U D
"""

"""
    punto #3 Los hilos

    TODO
        1 - coneccion
        2 - crear tablas
            cajeros /cajero_id
            transaccion /id_cajero/id_usuario/fecha/tipo/saldos/
            usuarios
            cuentas / id_cajero/ n_cuenta/ id_usuario / saldo_disponible

        3 - C R U D
"""
import sqlite3

con = sqlite3.connect("cajeros.db")
cur = con.cursor()

# Crear tablas en la base de datos cajeros.db
#cur.execute("CREATE TABLE usuarios(name, email, pin)")
cur.execute("CREATE TABLE cajeros( codigo, stado, disponible)")

# cur.execute("""
#     INSERT INTO usuarios VALUES
#         ('Yari', 'yari@cuc.cr', 1234),
#         ('Aldo', 'aldo@cuc.cr', 1234)
# """)

cur.execute("""
    INSERT INTO cajeros VALUES
        ('01', 'ocupado', 10000000),
        ('02', 'disponible', 7500000)
""")
            
con.commit()
            
#res = cur.execute("SELECT * FROM cajeros")
# res.fetchall()

for row in cur.execute("SELECT * FROM cajeros"):
    print(row)

#print(res)
con.close()


#con.commit()