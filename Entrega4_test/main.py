from flask import Flask, json, request
from pymongo import MongoClient

USER = "grupo59"
PASS = "grupo59"
DATABASE = "grupo59"

URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
client = MongoClient(URL)

USER_KEYS = ['uid', 'name', 'age', 'description']
MSG_KEYS = ['mid', 'message', 'sender', 'receptant', 'lat', 'long', 'date']
TEXT_KEYS = ['desired', 'required', 'forbidden', 'userId']
# Usuarios: uid, name, age, description
# Mensaje: mid, message, sender, receptant, lat, long, date

# Base de datos del grupo
db = client["grupo59"]

# Seleccionamos la collección de usuarios
usuarios = db.usuarios
mensajes = db.mensajes

# Iniciamos la aplicación de flask
app = Flask(__name__)


@app.route("/")
def home():
    """
    Página de inicio
    """
    return "<h1>Home</h1>"


# Rutas GET
# /messages - Todos los atributos de todos los mensajes en la base de datos
# /messages/:id1 & id2 - Todos los mensajes intercambiados entre los dos id de usuario
@app.route("/messages")
def get_messages():
    response = {
        'valid': True,
        'content': {}
    }
    id_1 = request.args.get('id1', None)
    id_2 = request.args.get('id2', None)

    if id_1 and id_2:
        response = conversation_request(id_1, id_2)
        return json.jsonify(response)

    response['content']['mongo_response'] = list(mensajes.find({}, {"_id": 0}))
    return json.jsonify(response)


def conversation_request(id_1, id_2):
    id_1 = int(id_1)
    id_2 = int(id_2)
    response = {
        'valid': True,
        'content': {}
    }
    user_1 = list(usuarios.find({"uid": id_1}, {"_id": 0}))
    user_2 = list(usuarios.find({"uid": id_2}, {"_id": 0}))

    if not (user_1 and user_2):
        response['valid'] = False
        response['content']['message'] = 'Alguno de los usuarios solicitados no existe'
    else:
        messages = mensajes.find(
            {
                "$or": [
                    {
                        "$and": [
                            {"sender": id_1},
                            {"receptant": id_2}
                        ]
                    },
                    {
                        "$and": [
                            {"sender": id_2},
                            {"receptant": id_1}
                        ]
                    }
                ]
            },
            {"_id": 0}
        )
        response['content']['mongo_response'] = list(messages)
    return response


@app.route("/messages/<int:mid>")
def get_message(mid):
    response = {
        'valid': True,
        'content': {}
    }
    mid = int(mid)
    message = list(mensajes.find({"mid": mid}, {"_id": 0}))
    if not message:
        response['valid'] = False
        response['content']['message'] = 'El mensaje solicitado no existe'
    else:
        response['content']['mongo_response'] = message
    return json.jsonify(response)


@app.route("/users")
def get_users():
    response = {
        'valid': True,
        'content': {}
    }
    response['content']['mongo_response'] = list(usuarios.find({}, {"_id": 0}))
    return json.jsonify(response)


@app.route("/users/<int:uid>")
def get_user(uid):
    uid = int(uid)
    response = {
        'valid': True,
        'content': {}
    }
    user = list(usuarios.find({"uid": uid}, {"_id": 0}))
    if not user:
        response['valid'] = False
        response['content']['message'] = 'El usuario solicitado no existe'
    else:
        messages = list(mensajes.find({"sender": uid}, {"_id": 0}))
        response['content']['mongo_user'] = user
        response['content']['mongo_messages'] = messages
    return json.jsonify(response)


# Rutas POST
# /messages - Inserta un nuevo mensaje a partir de un JSON. Solo lo inserta si los parametros son
# validos. Se añade con un id numerico unico
# Input: JSON CON atributos de nuevo mensaje, como body del request.
@app.route("/messages", methods=['POST'])
def new_message():
    data = None
    response = {
        'valid': True,
        'content': {}
    }
    # Intentamos obtener todos los parametros del mensaje
    try:
        if not request.json:
            raise TypeError
        data = {key: request.json[key] for key in MSG_KEYS[1:]}
    # Si se levanta un KeyError, entonces falta algun parametro del mensaje
    except KeyError as error:
        response['valid'] = False
        response['content']['message'] = \
            f'Error en la validacion de parametros: el parametro {error} no esta presente'
    # Si se levanta un TypeError, entonces el json del request es None
    except TypeError:
        response['valid'] = False
        response['content']['message'] = \
            f'Error en la validacion de parametros: no se recibio datos en el formato correcto'
    else:
        # Por ultimo, chequeamos que esten todos los tipos y si no, lo convertimos
        type_list = [str, int, int, float, float, str]
        for data_value, data_type, data_key in zip(data.values(), type_list, data.keys()):
            # Vemos si el tipo es el indicado
            if type(data_value) is not data_type:
                # Si es que no es el tipo indicado, intentamos convertirlo
                try:
                    data[data_key] = data_type(data_value)
                # Si hay excepcion, el valor no es convertible
                except ValueError:
                    response['valid'] = False
                    response['content']['message'] = 'Error en el tipo de parametros'
                    break

    if response['valid']:
        posible_id = 1
        while True:
            message = list(mensajes.find({"mid": posible_id}, {"_id": 0}))
            # Si el mensaje con el id no existe, entonces el id no esta utilizado
            if not message:
                break
            posible_id += 1
        data["mid"] = posible_id
        mensajes.insert_one(data)
        response['content']['message'] = f'Mensaje insertado con id {posible_id}'
    return json.jsonify(response)


# Rutas DELETE
# /messages/:id - Con un id de mensaje, lo elimina de la base de datos
@app.route("/messages/<int:mid>", methods=['DELETE'])
def delete_message(mid):
    """
    Elimina el usuario de id entregada
    """
    mid = int(mid)
    response = {
        'valid': True,
        'content': {}
    }
    message = list(mensajes.find({"mid": mid}, {"_id": 0}))
    if not message:
        response['valid'] = False
        response['content']['message'] = 'El mensaje solicitado no existe'
    else:
        mensajes.remove({"mid": mid})
        response['content']['message'] = 'Eliminacion existosa'
    return json.jsonify(response)


# Text search
@app.route("/text-search")
def text_search():
    info = {key: request.json[key] for key in TEXT_KEYS}
    user = int(info['userId'])
    query = ""
    for palabra in info['desired']:
        if not palabra:
            continue
        query += palabra + " "
    for palabra in info['required']:
        if not palabra:
            continue
        query += "\\" + "\"" + palabra + "\"" + "\\ "
    for palabra in info['forbidden']:
        if not palabra:
            continue
        query += f"-{palabra} "
    if query:
        final = list(mensajes.find({"$text": {"$search": query}, "sender": user}, {"_id": 0}))
        return json.jsonify(final)
    else:
        final = list(mensajes.find({"sender": user}, {"_id": 0}))
        return json.jsonify(final)


if __name__ == '__main__':
    app.run(debug=True)
