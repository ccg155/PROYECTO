import sqlite3
import json
from typing import Dict

class DataBase:
    """
    Clase para gestionar interacciones de la base de datos con el juego,
    como obtener información del jugador, enemigos, objetos e inventario.

    Métodos
    -------
    __init__():
        Inicializa la base de datos y la creación de las tablas.

    create_tables():
        Crea las tablas necesarias para el guardado de datos.

    update_player():
        Actualiza los datos del jugador en base a la partida actual.

    save_enemy_state():
        Actualiza el estado de un enemigo en base a la partida actual.

    add_item_to_inventory():
        Añade los objetos adquiridos por el juagdor durante la partida a su inventario.

    close():
        Cierra la conexión con la base de datos.
    """

    def __init__(self, db_name: str = 'db.py'):
        """
        Inicializa la conexión con la base de datos y se encarga de llamar a la
        creación de tablas donde guardar los datos.

        Parámetros
        ----------
        db_name: Nombre del archivo de la base de datos.
        """

        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Crea las tablas necesarias en la base de datos: players, enemies, items,
        player_inventory, player_abilities
        """

        # Tabla de jugadores
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS players (
                save_id INTEGER,
                position_x REAL NOT NULL,
                position_y REAL NOT NULL,
                health REAL NOT NULL,
                max_health REAL NOT NULL,
                energy REAL NOT NULL,
                max_energy REAL NOT NULL,
                exp INTEGER NOT NULL,
                speed INTEGER NOT NULL,
                attack INTEGER NOT NULL,
                magic INTEGER NOT NULL,
                gold INTEGER DEFAULT 0,
                weapon_index INTEGER DEFAULT 0,
                magic_index INTEGER DEFAULT 0,
                stats TEXT NOT NULL
            )
        ''')

        # Tabla de enemigos
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS enemies (
                enemy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER,
                enemy_name TEXT NOT NULL,
                position_x REAL NOT NULL,
                position_y REAL NOT NULL,
                health REAL NOT NULL,
                is_alive INTEGER DEFAULT 1
            )
        ''')

        # Tabla de objetos disponibles
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER,
                item_type TEXT NOT NULL,
                item_name TEXT NOT NULL,
                position_x REAL,
                position_y REAL,
                is_collected INTEGER DEFAULT 0,
                quantity INTEGER DEFAULT 1,
                properties TEXT
            )
        ''')

        # Tabla de inventario del jugador
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS player_inventory (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER,
                item_id INTEGER,
                quantity INTEGER DEFAULT 1,
                is_equipped INTEGER DEFAULT 0
            )
        ''')

        # Tabla de habilidades
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS player_abilities (
                ability_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER,
                ability_name TEXT NOT NULL,
                ability_type TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                unlocked INTEGER DEFAULT 1
            )
        ''')

        self.conn.commit()

    def update_player(self, save_id: int, player_data: Dict):
        """
        Actualiza los datos del jugador en la base de datos.

        Parámetros
        ----------
        save_id: ID de guardado del jugador.
        player_data: Diccionario con los datos del jugador.
        """

        self.cur.execute('''
            UPDATE players SET
                position_x = ?,
                position_y = ?,
                health = ?,
                max_health = ?,
                energy = ?,
                max_energy = ?,
                exp = ?,
                speed = ?,
                attack = ?,
                magic = ?,
                gold = ?,
                weapon_index = ?,
                magic_index = ?,
                stats = ?
            WHERE save_id = ?
        ''', (
            player_data['position'][0],
            player_data['position'][1],
            player_data['health'],
            player_data['max_health'],
            player_data['energy'],
            player_data['max_energy'],
            player_data['exp'],
            player_data['speed'],
            player_data['attack'],
            player_data['magic'],
            player_data.get('gold', 0),
            player_data.get('weapon_index', 0),
            player_data.get('magic_index', 0),
            json.dumps(player_data['stats']),
            save_id
        ))

        self.conn.commit()

    def save_enemy_state(self, save_id: int, enemy_name: str, health: float, is_alive: bool):
        """
        Actualiza el estado de un enemigo.

        Parámetros
        ----------
        save_id: ID de guardado.
        enemy_name: nombre.
        health: vida actual.
        is_alive: estado de vida.
        """

        self.cur.execute('''
            UPDATE enemies SET
                health = ?,
                is_alive = ?
            WHERE save_id = ? AND enemy_name = ?
        ''', (health, int(is_alive), save_id, enemy_name))
        self.conn.commit()

    def add_item_to_inventory(self, save_id: int, item_id: int, quantity: int = 1):
        """
        Añade un objeto al inventario del jugador o incrementa su cantidad.

        Parámetros
        ----------
        save_id: ID de guardado del jugador.
        item_id: ID del objeto.
        quantity: cantidad del objeto..
        """

        self.cur.execute('''
            SELECT quantity FROM player_inventory 
            WHERE git push origin db
save_id = ? AND item_id = ?
        ''', (save_id, item_id))

        existing = self.cur.fetchone()

        if existing:
            new_quantity = existing[0] + quantity
            self.cur.execute('''
                UPDATE player_inventory SET
                    quantity = ?
                WHERE save_id = ? AND item_id = ?
            ''', (new_quantity, save_id, item_id))
        else:
            self.cur.execute('''
                INSERT INTO player_inventory (save_id, item_id, quantity)
                VALUES (?, ?, ?)
            ''', (save_id, item_id, quantity))

        self.conn.commit()

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.conn.close()

