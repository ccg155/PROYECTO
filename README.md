#  🐉 Juego de RPG en Python con pygame

Este proyecto es una aplicación de juego de rol basada en texto, desarrollada en Python, que permite a los jugadores simular aventuras al estilo de *RPG*. Los jugadores pueden crear personajes, explorar mundos, interactuar con otros personajes y enfrentar diversos desafíos. (De momento en progreso, puede que falten algunos atributos)

---

##  Estructura del Proyecto

```bash
├── battle/                   # Módulo para la lógica de combate
├── characters/               # Definición de clases y atributos de personajes
├── database/                 # Gestión de datos y persistencia
├── items/                    # Implementación de objetos y equipamiento(Sprites, personajes, etc.)
├── ui/                       # Interfaz de usuario y menús interactivos
├── utils/                    # Funciones utilitarias y herramientas auxiliares
├── game.py                   # Lógica principal del juego
├── main.py                   # Menu de entrada para la ejecución del juego
├── requirements.txt          # Lista de dependencias del proyecto(librerias)
└── test_interactions.py      # Pruebas para las interacciones del juego
```

---

##  Cómo Ejecutar el Juego

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/ccg155/PROYECTO.git
   ```

2. **Instalar las dependencias**:

   Navega al directorio del proyecto y ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar el juego**:

   Ejecuta el siguiente comando:

   ```bash
   python main.py
   ```

   A partir de aquí, podrás:

   - Crear y personalizar tu personaje.
   - Explorar diferentes escenarios y misiones.
   - Interactuar con personajes no jugadores (PNJs).

---

## 🛠️ Dependencias

Este proyecto utiliza las siguientes bibliotecas de Python:

- [pygame](https://pypi.org/project/pyame/):  Biblioteca para el desarrollo de videojuegos en Python. Ofrece funciones para gráficos, sonido y manejo de eventos.
- [pytest](https://pypi.org/project/pytest/): Framework para escribir y ejecutar pruebas unitarias
*Nota*: Asegúrate de tener Python 3.x instalado en tu sistema.

---

## 🧪 Pruebas

Para ejecutar las pruebas incluidas en el proyecto:

```bash
python test_interactions.py
```

Estas pruebas cubren las interacciones básicas del juego y aseguran que las funcionalidades principales operen correctamente.

---

## 🚀 Próximas Mejoras

- Implementación de una interfaz gráfica de usuario (GUI).
- Ampliación del universo del juego con nuevas misiones y escenarios.
- Incorporación de funcionalidades multijugador en línea.
- Optimización del rendimiento y uso de recursos.

---

## 📬 Contacto

Contacta con el coordinador por [Carlos Crespo Gutiérrez](https://github.com/ccg155).

Para consultas o sugerencias, por favor, abre un issue en el repositorio o contacta a través de GitHub.

---
