from flask import jsonify, request

#Prueba
def hello_world():
    texto = request.json['texto']
    return jsonify({'texto': texto})
