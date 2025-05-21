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
