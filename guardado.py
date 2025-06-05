import json
import os

ARCHIVO_DATOS = "proyectos.json"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS): # Verifica si el archivo existe
        return []
    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f: # Lee el archivo
        return json.load(f) # Carga los datos del archivo JSON

def guardar_datos(proyectos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f: # Lee el archivo
        json.dump(proyectos, f, indent=4, ensure_ascii=False) # Guarda los datos en formato JSON, con indentación de 4 espacios y sin codificar caracteres no ASCII