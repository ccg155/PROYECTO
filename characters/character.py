
class Character:
    """
    Clase base para todos los personajes en el juego.
    
    Atributos:
        name (str): El nombre del personaje.
        health (int): Los puntos de vida del personaje.
        attack_power (int): El poder de ataque base del personaje.
        gold (int): La cantidad de oro que posee el personaje.
        defense (int): La cantidad de defensa que posee el personaje.
        xp (int): La cantidad de xp que posee el personaje.
    """
    def __init__(self, name: str, health: int = 100, max_health: int = 100, attack_power: int = 10, gold: int = 500, xp: int = 0, defense: int = 10, speed: int = 5, level: int = 1):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack_power = attack_power
        self.defense = defense
        self.gold = gold
        self.xp = xp
        self.speed = speed
        self.level = level
    
    def heal(self, amount: int):
        if self.health + amount >= self.max_health:
            self.health = self.max_health
        else:
            self.health += amount
    
    def take_damage(self, amount: int, attacker: 'Character' = None):
        damage_taken = max(0, amount - 0.25 * self.defense)
        if self.health - damage_taken < 0:
            self.health = 0
            print(f'{self.name} ha muerto.')
        else:
            self.health -= damage_taken
            print(f'{self.name} recibió {damage_taken} puntos de daño.')
            print(f'{self.name} tiene ahora {self.health} puntos de vida.')
    
    def level_up(self):
        self.level += 1
        self.xp = 0
    
    def gain_xp(self, amount):
        self.xp += amount
        print(f'{self.name} ganó {amount} puntos de xp.')
    
    def attack(self, target: 'Character'):
        if self.is_alive() and target.is_alive():
            print(f'{self.name} atacó a {target.name}.')
            target.take_damage(self.attack_power, self)
        else:
            print(f'{self.name} no puede atacar porque el atacante/atacado está muerto.')
    
    def is_alive(self) -> bool:
        """
        Returns:
            bool: Devuelve True si el personaje esta vivo, Falso de lo contrario_
        """
        return self.health > 0
    
    def __str__(self):
        return (f'🆔 Nombre: {self.name}\n'
                f'📈 Nivel: {self.level}\n'
                f'❤️  Salud: {self.health}/{self.max_health}\n'
                f'⚔️  Ataque: {self.attack_power}\n'
                f'🛡️  Defensa: {self.defense}\n'
                f'💰 Oro: {self.gold}\n'
                f'⭐ XP: {self.xp}\n'
                f'⚡ Velocidad: {self.speed}') 

"""
char1=Character('pepe')
char2=Character('Matias')
char1.attack(char2)
"""