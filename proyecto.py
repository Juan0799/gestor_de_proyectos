from datetime import datetime
from guardado import cargar_datos, guardar_datos

def crear_proyecto(nombre, descripcion, fecha_limite):
    try:
        fecha = datetime.strptime(fecha_limite, "%Y-%m-%d").date()
    except ValueError:
        print("Error: La fecha debe tener el formato YYYY-MM-DD")
        return

    proyectos = cargar_datos()

    if any(p["nombre"] == nombre for p in proyectos):
        print(f'Error: Ya existe un proyecto con el nombre "{nombre}".')
        return

    nuevo_proyecto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "fecha_limite": fecha_limite,
        "tareas": []
    }

    proyectos.append(nuevo_proyecto)
    guardar_datos(proyectos)
    print("Proyecto creado con éxito.")