# Gestor de Tareas

Este programa permite gestionar proyectos y tareas desde la línea de comandos.

## Requisitos

- Python 3.8 o superior

## Instalación

1. Clona o descarga este repositorio.
2. Asegúrate de tener los archivos: `main.py`, `proyecto.py`, `tarea.py`, `guardado.py`.

## Uso

Ejecuta el programa desde la terminal:

```sh
python main.py <comando> [argumentos...]
```

### Comandos disponibles

- **crear_proyecto**  
  Crea un nuevo proyecto.
  ```
  python main.py crear_proyecto "Nombre" "Descripción" "AAAA-MM-DD"
  ```

- **crear_tarea**  
  Crea una tarea en un proyecto existente.
  ```
  python main.py crear_tarea "Proyecto" "Tarea" "Descripción" "Responsable" "AAAA-MM-DD" "ESTADO"
  ```

- **listar_tareas**  
  Lista las tareas de un proyecto, opcionalmente filtrando por estado.
  ```
  python main.py listar_tareas "Proyecto"
  python main.py listar_tareas "Proyecto" "ESTADO"
  ```

- **actualizar_tarea**  
  Cambia el estado de una tarea.
  ```
  python main.py actualizar_tarea "Proyecto" "Tarea" "NuevoEstado"
  ```

- **eliminar_tarea**  
  Elimina una tarea de un proyecto.
  ```
  python main.py eliminar_tarea "Proyecto" "Tarea"
  ```

- **ayuda**  
  Muestra la ayuda de comandos.
  ```
  python main.py ayuda
  ```

### Estados válidos para tareas

- `PENDIENTE`
- `EN_PROGRESO`
- `COMPLETADA`

### Notas

- Las fechas deben tener el formato `AAAA-MM-DD`.
- Los datos se guardan en el archivo `proyectos.json` en el mismo directorio.
- Los test se ejecutan con `python -m unittest prueba_gestor.py` en la consola

---

**Ejemplo de uso:**

```sh
python main.py crear_proyecto "Mi Proyecto" "Descripción de ejemplo" "2025-06-30"
python main.py crear_tarea "Mi Proyecto" "Tarea1" "Descripción tarea" "Juan" "2025-06-15" "PENDIENTE"
python main.py listar_tareas "Mi Proyecto"
python main.py actualizar_tarea "Mi Proyecto" "Tarea1" "COMPLETADA"
python main.py eliminar_tarea "Mi Proyecto" "Tarea1"
```

## Autores
Juan Pablo Villamil
Joaquín Royes
