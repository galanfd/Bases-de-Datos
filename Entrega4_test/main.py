from flask import Flask, json, request
from pymongo import MongoClient

USER = "grupo59"
PASS = "grupo59"
DATABASE = "grupo59"

URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
client = MongoClient(URL)

USER_KEYS = ['uid', 'name', 'age', 'description']
MSG_KEYS = ['mid', 'message', 'sender', 'receptant', 'lat', 'long', 'date']
# Usuarios: uid, name, age, description
# Mensaje: mid, message, sender, receptant, lat, long, date

# Base de datos del grupo
db = client["grupo59"]

# Seleccionamos la collección de usuarios
usuarios = db.usuarios
mensajes = db.mensajes

#Iniciamos la aplicación de flask
app = Flask(__name__)

@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>Home</h1>"

# Rutas GET
# /messages - Todos los atributos de todos los mensajes en la base de datos
# /messages/:id1 & id2 - Todos los mensajes intercambiados entre los dos id de usuario
@app.route("/messages")
def get_messages():
    id_1 = request.args.get('id1', None)
    id_2 = request.args.get('id2', None)
    if id_1 and id_2:
        id_1 = int(id_1)
        id_2 = int(id_2)
        mensajes_1 = list(mensajes.find({"sender": id_1}, {"_id": 0}))
        mensajes_2 = list(mensajes.find({"sender": id_2}, {"_id": 0}))
        matches = []
        for mensaje in mensajes_1:
            if mensaje["receptant"] == id_2:
                matches.append(mensaje)
        for mensaje in mensajes_2:
            if mensaje["receptant"] == id_1:
                matches.append(mensaje)
        return json.jsonify(matches)
    messages = list(mensajes.find({}, {"_id": 0}))
    return json.jsonify(messages)

@app.route("/messages/<int:mid>")
def get_message(mid):
    message = list(mensajes.find({"mid": mid}, {"_id": 0}))
    return json.jsonify(message)

@app.route("/users")
def get_users():
    users = list(usuarios.find({}, {"_id": 0}))
    return json.jsonify(users)

@app.route("/users/<int:uid>")
def get_user(uid):
    user = list(usuarios.find({"uid": uid}, {"_id": 0}))
    messages = list(mensajes.find({"sender": uid}, {"_id": 0}))
    response = {
        "user": user,
        "messages": messages
    }
    return json.jsonify(response)


# Text search

# Rutas POST
# /messages - Inserta un nuevo mensaje a partir de un JSON. Solo lo inserta si los parametros son
# validos. Se añade con un id numerico unico
# Input: JSON CON atributos de nuevo mensaje, como body del request.
@app.route("/messages", methods=['POST'])
def new_message():
    pass

# Rutas DELETE
# /messages/:id - Con un id de mensaje, lo elimina de la base de datos
@app.route("/messages/<int:mid>", methods=['DELETE'])
def delete_message(mid):
    '''
    Elimina el usuario de id entregada
    '''
    if mid == None:
        res = 'Error 204: No Content  -  Debe ingresar un id'
        return json.jsonify(res)
    else:
        try:
            mid = int(mid)
        except:
            return json.jsonify('Formato de id ingresado no es valido')
        message = list(mensajes.find({"mid": mid}, {"_id": 0}))
        if message == []:
            return json.jsonify('Mensaje con id asociado no existente')
        else:
            mensajes.remove({"mid": mid})
            return json.jsonify({"Mensaje eliminado": True})

if __name__ == '__main__':
    app.run(debug=True)
