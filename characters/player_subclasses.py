from character import *

class Paladin(Character):
    """Clase para los personajes del tipo paladín.
       Alta defensa, bajo ataque

    Args:
        name (str): Nombre del paladín.
        gold (int): Oro del paladín.
        xp (int): Experiencia del paladín.
        level (int): Nivel del paladín.
        health (int): Salud del paladín, por defecto 150.
        max_health (int): Salud máxima del paladín, por defecto 150.
        attack_power (int): Poder de ataque, por defecto 7.
        defense (int): Defensa del paladín, por defecto 15.
        speed (int): Velocidad del paladín, por defecto 5.
    """
    def __init__(self, name, gold=500, xp=0, level=1,  health=150, max_health=150, attack_power=7,defense=15, speed=5):
        super().__init__(name, health, max_health, attack_power, gold, xp, defense, speed, level)

        
        
class Mage(Character):
       def __init__(self, name, gold=500, xp=0, level=1,  health=75, max_health=75, attack_power=18,defense=5, speed=12):
        super().__init__(name, health, max_health, attack_power, gold, xp, defense, speed, level)

        
class Warrior(Character):
    def __init__(self, name, gold=500, xp=0, level=1,  health=80, max_health=80, attack_power=15,defense=10, speed=15):
        super().__init__(name, health, max_health, attack_power, gold, xp, defense, speed, level)
      

class TestChar(Character):
        def __init__(self, name, gold=500, xp=0, level=1,  health=80, max_health=80, attack_power=1000,defense=10, speed=15):
            super().__init__(name, health, max_health, attack_power, gold, xp, defense, speed, level)
