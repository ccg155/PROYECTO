#pip install flask
#importar desde la librería flask: Flask: el motor del servidor web,
#request: para recibir datos de los usuarios,
# jsonify: para devolver datos en formato JSON (lo que usan las apps/webs)
from flask import Flask, request, jsonify
#para trabajar con bases de datos, importar:
import sqlite3

app = Flask(__name__) #Crea el servidor y permite crear rutas como /api/personajes
database = 'juego.db' #El archivo de base de datos se llama 'juego.db'

#Función que abre la base de datos
def get_db():
    conn = sqlite3.connect(f'database/{database}') #Abre el archivo
    conn.row_factory = sqlite3.Row #Para que los datos vengan con nombre, no solo con números, en vez de personaje[1]--> personaje['nombre']
    return conn #Devuelve la conexión a la base


# PERSONAJES

# GET PERSONAJES (obtener)
'''Es una ruta web, si se entra en http://tuservidor/api/personajes y use el
GET se activará la función get_personajes'''
@app.route('/api/personajes', methods=['GET'])
def get_personajes():
    conn = get_db() #abre la base de datos
    cur = conn.cursor() #para poder escribir o leer en la base
    cur.execute('SELECT * FROM Personajes') #busca todos los personajes en la tabla 'Personajes'
    personajes = [dict(row) for row in cur.fetchall()] #convierte los resultados en diccionarios
    conn.close() #cierra la base de datos
    return jsonify(personajes) #manda los personajes al navegador en formato JSON (así se ve en la web)

# POST PERSONAJES (añadir)
#Ruta con POST, envia un personaje nuevo
@app.route('/api/personajes', methods=['POST'])
def add_personaje():
    data = request.get_json() #Coge los datos  que se mandan desde una web o aplicación
    campos = (
        data['nombre'],
        data['raza'],
        data['clase'],
        data['nivel'],
        data['xp'],
        data['salud'],
        data['fuerza'],
        data['destreza'],
        data['velocidad'],
        data['dinero']
    ) #Ordena los datos bien para meterlos en la base de datos
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Personajes (nombre, raza, clase, nivel, xp, salud, fuerza, destreza, velocidad, dinero)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', campos) #escribe el nuevo personaje en la tabla Personajes, los ?  son espacios vacíos que  se rellenan con los datos de campos
    conn.commit() #Guarda los cambios
    conn.close() #Devuelve un mensajes confirmando la creación del personaje
    return jsonify({'mensaje': 'Personaje creado'}), 201 #significa  'Creado correctamente' en código HTTP


# RUTA BASE
# Creación de una ruta web para cuando alguien entra a la página principal
@app.route('/')
#Código que se ejecuta cuando se visita /
def home():
    return 'API del juego de roles activa 🚀' #Mensaje que se muestra al entrar en el navegador


# ENEMIGOS

# GET ENEMIGOS (obtener)
'''Si vas a la dirección /api/enemigos, el servidor te manda la lista
completa de enemigos guardados'''
@app.route('/api/enemigos', methods=['GET'])
def get_enemigos():
    conn = get_db() #abre la base de datos
    cur = conn.cursor() #prepara para leer
    cur.execute('SELECT * FROM Enemigos') #da todos los enemigos
    data = [dict(row) for row in cur.fetchall()] #convierte a formato diccionario
    conn.close() #cierra la base de datos
    return jsonify(data) #devuelve en formato JSON

# POST ENEMIGOS (añadir un enemigo nuevo)
'''Guarda en la base de datos el enemigo mandado desde una app/web'''
@app.route('/api/enemigos', methods=['POST'])
def add_enemigo():
    data = request.get_json() #recibe los datos del enemigo
    conn = get_db() #abre la base de datos
    cur = conn.cursor() #prepara para escribir
    cur.execute('''
        INSERT INTO Enemigos (nombre, tipo, nivel, vida, fuerza, defensa, recompensa)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['nombre'],
        data['tipo'],
        data.get('nivel', 1), #si no se pone nivel, se pone 1 por defecto
        data.get('vida', 30), #se pone 30 por defecto
        data.get('fuerza', 5), #se pone 5 por defecto
        data.get('defensa', 3), #3 por defecto
        data.get('recompensa', 10) #10 por defecto
    ))
    conn.commit() #guarda los cambios
    conn.close() #cierra la base
    return jsonify({'mensaje': 'Enemigo creado'}), 201


# OBJETOS

# GET OBJETOS (ver todos los objetos disponibles)
@app.route('/api/objetos', methods=['GET'])
def get_objetos():
    conn = get_db() #abre la base de datos
    cur = conn.cursor() #prepara para leer
    cur.execute('SELECT * FROM Objetos') #busca todos los objetos
    data = [dict(row) for row in cur.fetchall()] #convierte en formato diccionario
    conn.close() #cierra la base
    return jsonify(data) #devuelve como JSON

# POST OBJETOS (añadir)
@app.route('/api/objetos', methods=['POST'])
def add_objeto():
    data = request.get_json() #toma los datos del objeto mandado
    conn = get_db() #abre la base
    cur = conn.cursor() #prepara para escribir
    cur.execute('''
        INSERT INTO Objetos (nombre, tipo, descripcion, efecto, precio)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['nombre'], #obligatorio
        data['tipo'], #obligatorio
        data['descripcion'], #obligatorio
        data['efecto'], #obligatorio
        data.get('precio', 10) #se pone 10 por defecto
    ))
    conn.commit() #guarda los cambios
    conn.close() #cierra la base
    return jsonify({'mensaje': 'Objeto añadido'}), 201


# INVENTARIO

# GET INVENTARIO (ver qué hay en el inventario)
@app.route('/api/inventario', methods=['GET'])
def get_inventario():
    conn = get_db() #abre la base de datos
    cur = conn.cursor() #prepara para leer datos
    cur.execute('SELECT * FROM Inventario') #busca lo que hay en la tabla 'Inventario'
    data = [dict(row) for row in cur.fetchall()] #pone cada fila como un diccionario
    conn.close() #cierra la base
    return jsonify(data) #devuelve la info como JSON

# POST INVENTARIO (añadir objeto al inventario de un personaje)
@app.route('/api/inventario', methods=['POST'])
def add_inventario():
    data = request.get_json() #recibe los datos que se mandan (personaje, objeto, cantidad)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Inventario (personaje_id, objeto_id, cantidad)
        VALUES (?, ?, ?)
    ''', (
        data['personaje_id'],
        data['objeto_id'],
        data.get('cantidad', 1) #1 por defecto
    ))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Objeto añadido al inventario'}), 201


# HABILIDADES

# GET HABILIDADES (obtener)
@app.route('/api/habilidades', methods=['GET'])
def get_habilidades():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Habilidades')
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

# POST HABILIDADES (añadir)
@app.route('/api/habilidades', methods=['POST'])
def add_habilidad():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Habilidades (nombre, descripcion, clase)
        VALUES (?, ?, ?)
    ''', (
        data['nombre'],
        data['descripcion'],
        data['clase']
    ))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Habilidad añadida'}), 201


# MAZMORRAS

# GET MAZMORRAS (obtener)
@app.route('/api/mazmorras', methods=['GET'])
def get_mazmorras():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Mazmorras')
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

# POST MAZMORRAS (añadir)
@app.route('/api/mazmorras', methods=['POST'])
def add_mazmorra():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Mazmorras (personaje_id, enemigo_id, resultado, experiencia_ganada)
        VALUES (?, ?, ?, ?)
    ''', (
        data['personaje_id'],
        data['enemigo_id'],
        data['resultado'],
        data.get('experiencia_ganada', 0)
    ))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Registro de mazmorra añadido'}), 201


#Si se ejecuta el archivo directamente
if __name__ == '__main__':
    app.run(debug=True) #Enciende el servidor y si algo no funciona, muestra el error en pantalla