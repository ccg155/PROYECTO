import sqlite3 #Importo la librería de sql para crear una base de datos

# Defino una clase que cree la base de datos
class BaseDeDatos:
    def __init__(self, nombre: str = 'juego.db'):
        self.conn = sqlite3.connect(nombre) # Crea el archivo donde se guardará la db
        self.cur = self.conn.cursor() # Permite operar con los datos de la db
        self.crear_tablas() # Llama al metodo que inicializa la creación de sus la tabla de cada clase

    # Metodo que iniclializa la creación de las tablas
    def crear_tablas(self):
        self.tabla_personajes()
        self.tabla_enemigos()
        self.tabla_objetos()
        self.tabla_inventarios()
        self.tabla_habilidades()
        self.tabla_mazmorras()
        self.tabla_batallas()

    def cerrar(self):
        self.conn.close()

# Creo una clase para guardar los personajes del juego
class Personajes(BaseDeDatos):
    def __init__(self, db = 'juego.db'):
        super().__init__(db)

    def tabla_personajes(self):
        self.cur.execute(''' 
            CREATE TABLE IF NOT EXISTS Personajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE,
                clase TEXT,
                nivel INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                salud INTEGER,
                max_salud INTEGER,
                fuerza INTEGER,
                defensa INTEGER DEFAULT 0,
                velocidad INTEGER DEFAULT 5,
                oro INTEGER
            )
        ''') # El metodo execute se utiliza para realizar consultas en la db
        self.conn.commit() # Añade la tabla a la base de datos

    def añadir_personaje(self, nombre, clase, nivel, experiencia, salud, max_salud, fuerza, defensa, inteligencia, oro):
        self.cur.execute('''
            INSERT INTO Personajes 
                (nombre, clase, nivel, experiencia, salud, max_salud, fuerza, defensa, inteligencia, oro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (nombre, clase, nivel, experiencia, salud, max_salud, fuerza, defensa, inteligencia, oro)
        )
        self.conn.commit() # Añade el nuevo personaje a la tabla 'Personajes' de la db

    def actualizar_salud(self): # para cura/ataque
        self.cur.execute('''
            UPDATE Personajes 
            SET salud = ? WHERE id = ?''',
            (self.salud, self.id)
        )
        self.conn.commit()

    def actualizar_nivel(self):
        self.cur.execute('''
            UPDATE Personajes 
            SET nivel = ?, xp = 0 WHERE id = ?''',
            (self.nivel, self.id)
        )
        self.conn.commit()

    def actualizar_xp(self):
        self.cur.execute('''
            UPDATE Personajes 
            SET xp = ? WHERE id = ?''',
            (self.xp, self.id)
        )
        self.conn.commit()

    def recompensa_ataque(self):
        self.cur.execute('''
            UPDATE Personajes 
            SET xp = ? WHERE id = ?''',
            (self.xp, self.id)
        )
        self.conn.commit()

    def mostrar_personajes(self):
        self.cur.execute('SELECT * FROM Personajes')
        return self.cur.fetchall() # muestra los resultados de la consulta anterior

class Jugadores (Personajes):
    def __init__(self, db = 'juego.db'):
        super().__init__(db)

class Enemigos(Personajes):
    def __init__(self, db):
        super().__init__(db)

    def tabla_enemigos(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Enemigos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                nivel INTEGER DEFAULT 1,
                salud INTEGER DEFAULT 30,
                fuerza INTEGER DEFAULT 5,
                defensa INTEGER DEFAULT 3,
                recompensa_xp INTEGER DEFAULT 10,
                recompensa_oro INTEGER DEFAULT 1
            )
        ''')

class Objetos(BaseDeDatos):
    def __init__(self, db):
        super().__init__(db)

    def tabla_objetos(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Objetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,  -- Por ejemplo: "arma", "pocion", "armadura"
                descripcion TEXT,
                efecto TEXT,  -- Por ejemplo: "aumenta fuerza en 5", "restaura 50 de vida"
                precio INTEGER DEFAULT 10
            )
        ''')

    def añadir_objeto(self, nombre, tipo, descripcion, efecto, precio):
        self.cur.execute('''
            INSERT INTO Objetos (nombre, tipo, descripcion, efecto, precio)
            VALUES (?, ?, ?, ?, ?)''',
            (nombre, tipo, descripcion, efecto, precio)
        )
        self.conn.commit()

class Inventarios(BaseDeDatos):
    def __init__(self, db):
        super().__init__(db)

    def tabla_inventarios(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Inventario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personaje_id INTEGER,
            objeto_id INTEGER,
            cantidad INTEGER DEFAULT 1,
            FOREIGN KEY(personaje_id) REFERENCES Personajes(id),
            FOREIGN KEY(objeto_id) REFERENCES Objetos(id)
            )
        ''')
        self.conn.commit()

    def añadir_objeto(self, personaje_id, objeto_id, cantidad):
        self.cur.execute('''
            INSERT INTO Inventarios (personaje_id, objeto_id, cantidad)
            VALUES (?, ?, ?)''',
            (personaje_id, objeto_id, cantidad)
        )
        self.conn.commit()

# Las habilidades las crea otra persona
class Habilidades(BaseDeDatos):
    def __init__(self, db):
        super().__init__(db)

    def tabla_habilidades(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Habilidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                descripcion TEXT,
                clase TEXT
            )
        ''')
        self.conn.commit()

    def añadir_habilidad(self, personaje_id, nombre, nivel):
        self.cur.execute('''
        INSERT INTO Habilidades (personaje_id, nombre, nivel)
        VALUES(?, ?, ?)''',
        (personaje_id, nombre, nivel)
        )
        self.conn.commit()

class Mazmorras(BaseDeDatos):
    def __init__(self, db):
        super().__init__(db)

    def tabla_mazmorras(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Mazmorras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personaje_id INTEGER,
            enemigo_id INTEGER,
            resultado TEXT NOT NULL, -- "Victoria" o "Derrota"
            experiencia_ganada INTEGER DEFAULT 0,
            FOREIGN KEY(personaje_id) REFERENCES Personajes(id),
            FOREIGN KEY(enemigo_id) REFERENCES Enemigos(id)
            )
        ''')
        self.conn.commit()

    def añadir_mazmorra(self, nombre, estado = 'No explorada'):
        self.cur.execute('''
        INSERT INTO Mazmorras (nombre, estado)
        VALUES (?, ?)''',
        (nombre, estado)
        )
        self.conn.commit()