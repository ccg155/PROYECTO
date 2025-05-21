import requests

API_URL = "http://localhost:5000/api"  # Cambia si está en otra máquina o puerto

def obtener_personajes():
    try:
        res = requests.get(f"{API_URL}/personajes")
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print("Error al obtener personajes:", e)
    return []

def obtener_personaje_por_id(pid):
    try:
        res = requests.get(f"{API_URL}/personajes/{pid}")
        return res.json() if res.status_code == 200 else None
    except Exception as e:
        print("Error al obtener personaje:", e)
        return None

def actualizar_personaje(pid, salud, xp, nivel, dinero):
    try:
        payload = {
            "salud": salud,
            "xp": xp,
            "nivel": nivel,
            "dinero": dinero
        }
        res = requests.put(f"{API_URL}/personajes/{pid}", json=payload)
        return res.status_code == 200
    except Exception as e:
        print("Error al actualizar personaje:", e)
        return False

from api_client import obtener_personajes, obtener_personaje_por_id, actualizar_personaje
personajes = obtener_personajes()
print("PERSONAJES DISPONIBLES:")
for p in personajes:
    print(f"{p['id']}: {p['nombre']} (Nivel {p['nivel']}, Salud {p['salud']})")

# Selección por terminal por ahora (podés hacer un selector bonito en Pygame más adelante)
try:
    personaje_id = int(input("Selecciona un personaje por ID: "))
    personaje_actual = obtener_personaje_por_id(personaje_id)
    print("Seleccionaste a:", personaje_actual["nombre"])
except Exception as e:
    print("Error seleccionando personaje:", e)
    return
