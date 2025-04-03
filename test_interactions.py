from characters import *

def test_character_interactions():
    # Crear personajes
    character1 = Character("Héroe", health=120, attack_power=15, defense=12)
    character2 = Character("Villano", health=100, attack_power=12, defense=10)

    print("\n🔰 Estado inicial:")
    print(character1, "\n")
    print(character2, "\n")

    # Ataque entre personajes
    print("\n⚔️ Batalla:")
    character1.attack(character2)
    character2.attack(character1)

    print("\n🩹 Curación:")
    character1.heal(10)
    print(character1)

    # Ganar XP y subir de nivel
    print("\n📈 Experiencia:")
    character1.gain_xp(50)
    character1.gain_xp(60)  # Supone que con 100 XP sube de nivel
    character1.level_up()
    print(character1)

    print("\n🛑 Comprobando si un personaje ha muerto:")
    character2.take_damage(200)  # Daño letal
    print(character2)

test_character_interactions()
