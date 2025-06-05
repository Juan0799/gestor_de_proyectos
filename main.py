import sys
from proyecto import crear_proyecto
from tarea import crear_tarea, listar_tareas, actualizar_tarea, eliminar_tarea

#* Muesta los comando disponibles.
def print_help():
    print("\nLos estados válidos para las tareas son: 'PENDIENTE', 'EN_PROGRESO', 'COMPLETADA'.")
    print('La fecha ingresada es la fecha límite de la tarea o proyecto y debe tener el formato "FECHA".')
    print("\nComandos disponibles:")
    print('  crear_proyecto "Nombre" "Descripción" "FECHA"')
    print('  crear_tarea "Proyecto" "Tarea" "Descripción" "Responsable" "FECHA" "ESTADO"')
    print('  listar_tareas "Proyecto" ["ESTADO"]')
    print('  actualizar_tarea "Proyecto" "Tarea" "Nuevo Estado"')
    print('  eliminar_tarea "Proyecto" "Tarea"')
    print('  ayuda - Muestra esta ayuda')
    
#* Valida los argumentos de la operación.
def validate_args(operacion, args, expected_args, usage_message):
    if len(args) not in (expected_args if isinstance(expected_args, list) else [expected_args]): # Verifica el número de argumentos
        print(f"Uso: python main.py {usage_message}") # Muestra el mensaje de uso si el número de argumentos es incorrecto
        return False
    return True

def main():
    if len(sys.argv) < 2:
        print("Error: Debe indicar una operación. Usa 'ayuda' para ver los comandos disponibles.")
        return

    operacion = sys.argv[1]

    #? Diccionario de los comandos y sus argumentos esperados:
    #? Estos son los mensajes que se muestran si el usuario no usa los argumentos correctos
    #? o si la operación no es reconocida

    comandos = {
        "crear_proyecto": {
            "func": crear_proyecto,
            "args": 5,
            "usage": 'crear_proyecto "Nombre" "Descripción" "AAAA-MM-DD"'
        },
        "crear_tarea": {
            "func": crear_tarea,
            "args": 8,
            "usage": 'crear_tarea "Proyecto" "Tarea" "Descripción" "Responsable" "AAAA-MM-DD" "ESTADO"'
        },
        "listar_tareas": {
            "func": listar_tareas,
            "args": [3, 4],
            "usage": 'listar_tareas "Proyecto" ["ESTADO"]'
        },
        "actualizar_tarea": {
            "func": actualizar_tarea,
            "args": 5,
            "usage": 'actualizar_tarea "Proyecto" "Tarea" "NuevoEstado"'
        },
        "eliminar_tarea": {
            "func": eliminar_tarea,
            "args": 4,
            "usage": 'eliminar_tarea "Proyecto" "Tarea"'
        },
        "ayuda": {
            "func": print_help,
            "args": 2,
            "usage": "ayuda"
        }
    }

    if operacion not in comandos:
        print(f"Operación desconocida: {operacion}. Usa 'ayuda' para ver los comandos disponibles.")
        return

    comando = comandos[operacion]
    try:
        if not validate_args(operacion, sys.argv, comando["args"], comando["usage"]):
            return

        match operacion: # Utiliza un patrón de coincidencia para ejecutar la función correspondiente
            case "ayuda":
                comando["func"]()
            case "crear_proyecto":
                comando["func"](sys.argv[2], sys.argv[3], sys.argv[4])
            case "crear_tarea":
                comando["func"](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
            case "listar_tareas":
                estado = sys.argv[3] if len(sys.argv) == 4 else None
                comando["func"](sys.argv[2], estado)
            case "actualizar_tarea":
                comando["func"](sys.argv[2], sys.argv[3], sys.argv[4])
            case "eliminar_tarea":
                comando["func"](sys.argv[2], sys.argv[3])
    except Exception as e:
        print(f"Error al ejecutar la operación: {str(e)}")

if __name__ == "__main__":
    main()