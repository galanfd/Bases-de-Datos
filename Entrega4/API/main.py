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


def date_check(date):
    year, month, day = date.split("-")
    if len(year)==4 and year.isnumeric() and month.isnumeric() and day.isnumeric() and int(month) <= 12 and int(month) >= 0 and int(day) >= 1 and int(day) <= 31:
        return True
    else:
        return False


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
    except Exception:
        response['valid'] = False
        response['content']['message'] = \
            f'Error en la validacion de parametros: no hay body en el request'
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
@app.route("/message/<int:mid>", methods=['DELETE'])
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
    info = None
    response = {
        'valid': True,
        'content': {}
    }
    # Tratamos el caso de que no se envie nada, que lanza un error con request.json
    if not request.get_data():
        final = list(mensajes.find({}, {"_id": 0}))
        response['content']['mongo_response'] = final
        return json.jsonify(response)

    # Tenemos que verificar que parametros estan
    try:
        # Si el diccionario no existe o esta vacio, devolvemos todos los mensajes
        if not request.json:
            final = list(mensajes.find({}, {"_id": 0}))
            response['content']['mongo_response'] = final
            return json.jsonify(response)

        # Creamos el diccionario con las palabras
        # NOTA: esta parte es un poco redundante, originalmente consideramos que tenian que estar
        # todas las llaves y listas para el request. Para no rehacer too, en el caso de que no este
        # alguna key, se agrega con una lista vacia.
        info = {}
        for key in TEXT_KEYS:
            # Si la llave no esta en el request, se agrega una lista vacia
            if key not in request.json.keys():
                # Si la llave es el userid, no lo agregamos
                if key == "userId":
                    continue
                info[key] = []
            else:
                info[key] = request.json[key]

        # Desde aqui hacemos la validacion que originalmente revisaba que todas los valores fueran
        # una llave valida con una lista valida, que aun sirve para validar los valores que envian
        # (si envian algo, sean listas con strings y no otra cosa)

        # Esta vez solo puede haber texto, asique levantamos excepcion si alguno no es string
        for data_key, data_value in info.items():
            # Si es que la llave es userId, vemos si el valor es un int
            if data_key == "userId":
                if type(data_value) is not int:
                    raise TypeError
                continue
            # Si no es userId, el valor tiene que ser una lista
            if type(data_value) is not list:
                raise TypeError
            # Cada valor de la lista tiene que ser un string
            for word in data_value:
                if type(word) is not str:
                    raise TypeError
    except TypeError:
        response['valid'] = False
        response['content']['message'] = \
            f'Error en la validacion de parametros: no se recibio datos en el formato correcto'

    # Para no hacer dos casos separados si se busca el userid o no, la consulta se va a asegurar que
    # el sender este en una lista con el userId. Si es que no hay id dado, entonces sera todos
    # los uid.

    # Si hay usuario, se revisa si el usuario existe y se hace la lista
    if 'userId' in info.keys():
        user = info['userId']
        user_check = list(usuarios.find({"uid": user}, {"_id": 0}))
        # Si es vacio, el usuario no existe
        if not user_check:
            response['valid'] = False
            response['content']['message'] = 'El usuario solicitado no existe'
        # Si no, tenemos que hacer la lista
        else:
            user = [user]
    # Si no se da un userId, entonces la lista son todos los ids
    else:
        user = mensajes.distinct("sender")

    # Vemos si ocurrio algun error, si no, estamos listos para la busqueda
    if not response['valid']:
        return json.jsonify(response)

    # Iniciamos la busqueda creando el query
    query = ""
    for palabra in info['desired']:
        if not palabra:
            continue
        query += palabra + " "
    for palabra in info['required']:
        if not palabra:
            continue
        query += "\\" + "\"" + palabra + "\"" + "\\ "
    # Si hasta ahora no hay query, entonces solo tendremos forbidden
    if not query:
        # Tomamos las palabras prohibidas y las volvemos un required
        for palabra in info['forbidden']:
            if not palabra:
                continue
            query += palabra + " "
        # Vemos si hay un query, si no, se maneja como un query vacio normal
        if query:
            results = list(mensajes.find(
                {"$text": {"$search": query}, "sender": {"$in": user}}, {"_id": 0})
            )
            # Extraemos los ids de todos los mensajes con las palabras prohibidas
            forb_msg = []
            for result in results:
                forb_msg.append(result['mid'])
            # Tomamos todos los mensajes que su mid no este en la lista
            final = list(mensajes.find(
                {
                    "$and": [
                        {"sender": {"$in": user}},
                        {"mid": {"$nin": forb_msg}}
                    ]
                }, {"_id": 0}
            ))
            response['content']['mongo_response'] = final
            return json.jsonify(response)
    else:
        # En este caso, hay palabras required y/o desired
        for palabra in info['forbidden']:
            if not palabra:
                continue
            query += f"-{palabra} "
    if query:
        final = list(mensajes.find(
            {"$text": {"$search": query}, "sender": {"$in": user}}, {"_id": 0})
        )
    else:
        final = list(mensajes.find({"sender": {"$in": user}}, {"_id": 0}))
    response['content']['mongo_response'] = final
    return json.jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
