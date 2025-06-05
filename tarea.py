from datetime import datetime
from guardado import cargar_datos, guardar_datos

# Estados válidos para las tareas
ESTADOS_VALIDOS = {"PENDIENTE", "EN_PROGRESO", "COMPLETADA"} 

# Creación de una nueva tarea
# Cada tarea pertenece a un proyecto y tiene un nombre, descripción, responsable, fecha límite y estado
def crear_tarea(nombre_proyecto, nombre_tarea, descripcion, responsable, fecha_limite, estado):
    if estado not in ESTADOS_VALIDOS: # Verifica si el estado es válido
        print(f"Error: Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}")
        return

    try: # Intenta convertir la fecha límite a un objeto de fecha
        fecha_tarea = datetime.strptime(fecha_limite, "%Y-%m-%d").date()
    except ValueError:
        print("Error: La fecha debe tener el formato YYYY-MM-DD")
        return

    proyectos = cargar_datos()

    for proyecto in proyectos:
        if proyecto["nombre"] == nombre_proyecto:
            fecha_proyecto = datetime.strptime(proyecto["fecha_limite"], "%Y-%m-%d").date()
            if fecha_tarea > fecha_proyecto:
                print(f"Error: La fecha límite de la tarea no puede ser posterior a la del proyecto \"{nombre_proyecto}\".")
                return

            if any(t["nombre"] == nombre_tarea for t in proyecto["tareas"]):
                print(f"Error: Ya existe una tarea con el nombre \"{nombre_tarea}\" en el proyecto \"{nombre_proyecto}\".")
                return

            nueva_tarea = {
                "nombre": nombre_tarea,
                "descripcion": descripcion,
                "responsable": responsable,
                "fecha_limite": fecha_limite,
                "estado": estado
            }
            proyecto["tareas"].append(nueva_tarea)
            guardar_datos(proyectos)
            print("Tarea creada con éxito.")
            return

    print(f"Error: No se encontró el proyecto \"{nombre_proyecto}\".")

def listar_tareas(nombre_proyecto, estado_filtro=None):
    proyectos = cargar_datos()

    for proyecto in proyectos:
        if proyecto["nombre"] == nombre_proyecto:
            tareas = proyecto["tareas"]

            if estado_filtro:
                if estado_filtro not in ESTADOS_VALIDOS:
                    print(f"Error: Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}")
                    return
                tareas = [t for t in tareas if t["estado"] == estado_filtro]
                print(f'Tareas del proyecto "{nombre_proyecto}" en estado "{estado_filtro}":')
            else:
                print(f'Tareas del proyecto "{nombre_proyecto}":')

            if not tareas:
                print("No hay tareas para mostrar.")
                return

            for i, tarea in enumerate(tareas, 1):
                print(f"{i}. {tarea['nombre']} - {tarea['descripcion']} - Responsable: {tarea['responsable']} - "
                      f"Fecha Límite: {tarea['fecha_limite']} - Estado: {tarea['estado']}")
            return

    print(f'Error: No se encontró el proyecto "{nombre_proyecto}".')

def actualizar_tarea(nombre_proyecto, nombre_tarea, nuevo_estado):
    if nuevo_estado not in ESTADOS_VALIDOS:
        print(f"Error: Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}")
        return

    proyectos = cargar_datos()

    for proyecto in proyectos:
        if proyecto["nombre"] == nombre_proyecto:
            for tarea in proyecto["tareas"]:
                if tarea["nombre"] == nombre_tarea:
                    tarea["estado"] = nuevo_estado
                    guardar_datos(proyectos)
                    print(f'Estado de la tarea "{nombre_tarea}" actualizado a "{nuevo_estado}".')
                    return

            print(f'Error: No se encontró la tarea "{nombre_tarea}" en el proyecto "{nombre_proyecto}".')
            return

    print(f'Error: No se encontró el proyecto "{nombre_proyecto}".')

def eliminar_tarea(nombre_proyecto, nombre_tarea):
    proyectos = cargar_datos()

    for proyecto in proyectos:
        if proyecto["nombre"] == nombre_proyecto:
            tareas = proyecto["tareas"]
            for i, tarea in enumerate(tareas):
                if tarea["nombre"] == nombre_tarea:
                    del tareas[i]
                    guardar_datos(proyectos)
                    print(f'Tarea "{nombre_tarea}" eliminada del proyecto "{nombre_proyecto}".')
                    return

            print(f'Error: No se encontró la tarea "{nombre_tarea}" en el proyecto "{nombre_proyecto}".')
            return

    print(f'Error: No se encontró el proyecto "{nombre_proyecto}".')