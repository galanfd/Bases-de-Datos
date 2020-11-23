# Entrega 4 - Proyecto Bases de Datos
## Grupos: 59 y 92
## **Integrantes**:
* Felipe Galán Donoso
* María Piedad Gonthier Rishmagüe
* Pablo Kipreos Palau
* Alejandro López

## Consideraciones generales y supuestos
* Se implementó todo lo solicitado. El único módulo creado fué ```main.py``` encontrado en la carpeta ```/API/main.py```, junto a los archivos ```Pipfile``` y ```Pipfile.lock``` correspondientes.
* Todas las rutas usan como *host* la dirección ```localhost:5000```
* Todos los *request* que se realizan tienen la misma respuesta base: un diccionario con dos valores
  * ```valid```: Un *bool* que representa si la respuesta es válida o hubo un error.
  * ```content```: El contenido de la respuesta, ya sea un mensaje de error o la respuesta de mongo.


* Antes de realizar la entrega se utilizaron las consultas de prueba, por lo que existen los mensajes con mid=1 y mid=291 con mensaje *"Mensaje para probar el POST"*

## Ejecución y funcionamiento
### **Rutas GET**
* ```/messages```: devuelve una lista con todos los mensajes presentes en la base de datos. La respuesta se encuentra con la llave ```mongo_response```
* ```/messages/:id```: devuelve el mensaje con el id especificado. En el caso de ser un id válido, se devuelve el diccionario del mensaje con la llave ```mongo_response```. Si no existe el id (o es un id inválido, si se sobrepasa la restricción de ```int``` por medios externos), entonces se devuelve un mensaje de error con la llave ```message```. 
  * La ruta acepta usar ```path variables``` o escribir directamente en el *request* la ruta ```localhost:5000/messages/id``` (ej: ```localhost:5000/messages/7```)
* ```/messages?id1=XX&id2=YY```: devuelve los mensajes intercambiados entre ambos id especificados, encontrados con la llave ```mongo_response```. Si alguno de los usuarios no existe, entonces se devuelve un error con llave ```message```.
  
    La ruta ```/messages``` solo entrega un resultado especial cuando se encuentran los 2 parámetros *id1* y *id2* (con *XX* y *YY* sus valores correspondientes). Si es que no se encuentran ambos parámetros, entonces se devuelven todos los mensajes. Si se encuentran más parámetros que estos dos, entonces cualquier parámetro distinto de *id1* y *id2* será ignorado. Ejemplos:
  * ```/messages?id1=1```: como falta el segundo id, se devuelven todos los mensajes.
  * ```/messages?id1=1&id2=2```: se devuelven todos los mensajes intercambiados entre 1 y 2
  * ```/messages?id1=3&id2=4&id4=9```: se devuelven todos los mensajes intercambiados entre 3 y 4
* ```/users```: devuelve una lista con todos los usuarios presentes en la base de datos. La respuesta se encuentra con la llave ```mongo_response```
* ```/users/:id```: devuelve el usuario con el id especificado. En el caso de ser un id válido, se devuelve el diccionario con los atributos correspondientes con la llave ```mongo_user``` y una lista con todos los mensajes que ha enviado con la llave ```mongo_messages``` (si el usuario no ha envíado mensajes, entonces será una lista vacía). De lo contrario, se devuelve un mensaje de error con llave ```message```.
### **Text search**
* **Importante**: el indice de texto creado está en **none**.
* La ruta *GET* de ```/text-search``` puede entregar las siguientes respuestas:
  * Si no hay *body*, o se envía un diccionario vacío, se entrega una lista con todos los mensajes presentes en la base de datos, con llave ```mongo_response```
  * Si el usuario especificado en "userID" no existe, entonces se devuelve un error, con llave ```message```
  * Si se entrega algun parámetro con un tipo inválido, entonces se devuelve un error, con llave ```message```
  * En otro caso, el *request* es válido y se devuelve una lista con los mensajes encontrados, contenida con llave ```mongo_response```
* Si se entregan palabras en cualquiera de los parámetros posibles, estas tendrán que ser *strings*. Si se entrega un id de usuario, este tendrá que ser un *int*. En caso que alguna de estas reglas no se cumpla, se devuelve un error.
* Cualquier llave inválida (distinta de las 4 solicitadas) es ignorada por el programa. Esto significa que un *request* con solo llaves inválidas es equivalente a un *request* con un diccionario vacío.


### **Ruta POST**
La ruta ```/messages``` llamada con el método *POST* entrega los siguientes mensajes:
* Si falta alguna llave en el diccionario entregado, se devuelve un mensaje de error con la primera llave faltante encontrada.
* Si se entrega un diccionario vacío o sin body, se notifica oportunamente.
* Para cada uno de los valores entregados al nuevo mensaje, **se intentará convertir el valor al tipo correspondiente** en caso de no serlo (ejemplo, si "mid" es un número como *string*, se intentará convertir a *int*). Si es que no es posible convertir todos los valores al tipo correspondiente, se notifica con error de tipo.
  
Este request siempre envía una respuesta con llave ```message```, con el error específico en caso de ser inválido, o un mensaje de éxito y el "mid" asignado en caso de ser válido. Cabe destacar que se le asignará al mensaje el "mid" más pequeño posible.

### **Ruta DELETE**
Si es que has leído hasta acá, significa que ya conoces el patrón de funcionamiento para un *request* con método *DELETE* con ruta ```/message```. Se devolverá siempre una respuesta con llave ```message```, con un mensaje de error en caso de no existir el "mid" entregado o de éxito en caso de existir.