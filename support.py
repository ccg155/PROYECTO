from csv import reader
from os import walk
import pygame 

def import_csv_layout(path):
    """
    Importa un archivo CSV que define el diseño del mapa de terreno de un nivel.

    El archivo CSV debe tener una estructura de filas y columnas donde cada valor
    representa un tipo de terreno (como '1' para pared, '0' para suelo, etc.). La función
    lee cada fila del archivo y la convierte en una lista de listas.

    Parámetros
    ----------
    path : str
        Ruta del archivo CSV que contiene el diseño del mapa de terreno.

    Retorna
    -------
    list
        Lista de listas que representan el mapa de terreno. Cada sublista corresponde a una fila
        del archivo CSV, y cada valor de la sublista representa un tipo de terreno.

    Ejemplo
    --------
    >>> import_csv_layout('level_1.csv')
    [['1', '0', '1'],
     ['0', '1', '0'],
     ['1', '0', '1']]

    """


    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
        
def import_folder(path):
    """
       Importa todas las imágenes de un directorio y las convierte en superficies de Pygame.

       Recorre todas las imágenes del directorio especificado, carga cada una de ellas como una
       superficie de Pygame y las agrega a una lista. Esta lista de superficies se retorna.

       Parámetros
       ----------
       path : str
           Ruta del directorio desde donde se deben cargar las imágenes.

       Retorna
       -------
       list
           Lista de superficies de Pygame correspondientes a las imágenes en el directorio.

       Ejemplo
       --------
       >>> import_folder('graphics/monsters')
       [<Surface(64x64x32 SW)>, <Surface(64x64x32 SW)>]
       """

    surface_list = []
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

