from character import *
from player_subclasses import *


class Goblin(Character):
    """Clase para los enemigos de tipo Goblin.
    
    Args:
        name (str): Nombre del goblin.
        health (int): Salud del goblin (por defecto 50).
        attack_power (int): Poder de ataque (por defecto 5).
        defense (int): Defensa del goblin (por defecto 3).
        speed (int): Velocidad del goblin (por defecto 4).
        gold_reward (int): Oro otorgado al morir (por defecto 20).
        xp_reward (int): Experiencia otorgada al morir (por defecto 15).
    """
    def __init__(self, level, name='Goblin'):
        health = 50 + 3 * level
        max_health = 50 + 3 * level
        attack_power = 5 + 0.1 * level
        defense = 5 + 0.05 * level
        speed = 5 + level
        xp_reward = 15 * 0.05 * level
        gold_reward = 20 * 0.05 * level
        
        super().__init__(name, health=health, max_health=max_health, attack_power=attack_power, defense=defense, speed=speed, level=level, gold=0)
        
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
    def take_damage(self, amount, attacker=None):
        super().take_damage(amount)
        
        if not self.is_alive():
            attacker.xp += self.xp_reward
            attacker.gold += self.gold_reward


paladin1 = TestChar('Arthur')
print(paladin1)
goblin1 = Goblin(level=5)
print(goblin1)
#
