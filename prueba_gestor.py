import unittest
import os
from unittest.mock import patch
from proyecto import crear_proyecto
from tarea import crear_tarea, listar_tareas, actualizar_tarea, eliminar_tarea
from guardado import cargar_datos, guardar_datos
from main import validate_args

# Los test se ejecutan con "python -m unittest prueba_gestor.py" en la consola

# Archivo de datos para pruebas
TEST_ARCHIVO = "proyectos_test.json"

class TestGestorProyectos(unittest.TestCase):

    # Configura el entorno antes de cada prueba, parcheando ARCHIVO_DATOS
    def setUp(self):
        self.patcher = patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
        self.patcher.start()
        if os.path.exists(TEST_ARCHIVO):
            os.remove(TEST_ARCHIVO)
        # Crear un proyecto base para pruebas que lo necesiten
        crear_proyecto("TestProy", "Proyecto de prueba", "2025-06-30")

    # Limpia después de cada prueba
    def tearDown(self):
        if os.path.exists(TEST_ARCHIVO):
            os.remove(TEST_ARCHIVO)
        self.patcher.stop()

    # Test para crear un proyecto exitosamente
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_crear_proyecto_exito(self):
        crear_proyecto("Proyecto2", "Otro proyecto", "2025-07-15")
        data = cargar_datos()
        self.assertEqual(len(data), 2)  # Proyecto base + nuevo proyecto
        self.assertEqual(data[1]["nombre"], "Proyecto2")
        self.assertEqual(data[1]["descripcion"], "Otro proyecto")
        self.assertEqual(data[1]["fecha_limite"], "2025-07-15")
        self.assertEqual(data[1]["tareas"], [])

    # Test para crear un proyecto con fecha inválida
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_crear_proyecto_fecha_invalida(self):
        with patch("builtins.print") as mocked_print:
            crear_proyecto("Proyecto3", "Descripción", "2025-13-01")
            mocked_print.assert_called_with("Error: La fecha debe tener el formato YYYY-MM-DD")

    # Test para crear un proyecto con nombre duplicado
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_crear_proyecto_duplicado(self):
        with patch("builtins.print") as mocked_print:
            crear_proyecto("TestProy", "Descripción duplicada", "2025-06-30")
            mocked_print.assert_called_with('Error: Ya existe un proyecto con el nombre "TestProy".')

    # Test para crear una tarea
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_crear_tarea_exito(self):
        crear_tarea("TestProy", "Tarea1", "Descripción tarea", "Juan", "2025-06-15", "PENDIENTE")
        data = cargar_datos()
        self.assertEqual(len(data[0]["tareas"]), 1)
        self.assertEqual(data[0]["tareas"][0]["nombre"], "Tarea1")
        self.assertEqual(data[0]["tareas"][0]["estado"], "PENDIENTE")
        self.assertEqual(data[0]["tareas"][0]["responsable"], "Juan")
        self.assertEqual(data[0]["tareas"][0]["fecha_limite"], "2025-06-15")

    # Test para crear una tarea con fecha inválida
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_crear_tarea_proyecto_inexistente(self):
        with patch("builtins.print") as mocked_print:
            crear_tarea("NoExiste", "Tarea1", "Descripción", "Juan", "2025-06-15", "PENDIENTE")
            mocked_print.assert_called_with('Error: No se encontró el proyecto "NoExiste".')

    # Test para crear una tarea con estado inválido
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_crear_tarea_estado_invalido(self):
        with patch("builtins.print") as mocked_print:
            crear_tarea("TestProy", "Tarea1", "Descripción", "Juan", "2025-06-15", "INVALIDO")
            # Checkea el mensaje de error independientemente del orden de los estados
            called_args = mocked_print.call_args[0][0]
            self.assertTrue(
                called_args.startswith("Error: Estado inválido. Debe ser uno de:") and
                "PENDIENTE" in called_args and
                "EN_PROGRESO" in called_args and
                "COMPLETADA" in called_args
            )

    # Test para crear una tarea con fecha posterior a la del proyecto
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_crear_tarea_fecha_posterior(self):
        with patch("builtins.print") as mocked_print:
            crear_tarea("TestProy", "Tarea1", "Descripción", "Juan", "2025-07-01", "PENDIENTE")
            mocked_print.assert_called_with('Error: La fecha límite de la tarea no puede ser posterior a la del proyecto "TestProy".')

    # Test para listar tareas
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_listar_tareas_exito(self):
        crear_tarea("TestProy", "Tarea1", "Descripción", "Juan", "2025-06-15", "PENDIENTE")
        with patch("builtins.print") as mocked_print:
            listar_tareas("TestProy")
            mocked_print.assert_any_call('Tareas del proyecto "TestProy":')
            mocked_print.assert_any_call("1. Tarea1 - Descripción - Responsable: Juan - Fecha Límite: 2025-06-15 - Estado: PENDIENTE")

    # Test para listar tareas con estado específico
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_listar_tareas_con_estado(self):
        crear_tarea("TestProy", "Tarea1", "Descripción", "Juan", "2025-06-15", "PENDIENTE")
        crear_tarea("TestProy", "Tarea2", "Otra tarea", "Ana", "2025-06-15", "COMPLETADA")
        with patch("builtins.print") as mocked_print:
            listar_tareas("TestProy", "PENDIENTE")
            mocked_print.assert_any_call('Tareas del proyecto "TestProy" en estado "PENDIENTE":')
            mocked_print.assert_any_call("1. Tarea1 - Descripción - Responsable: Juan - Fecha Límite: 2025-06-15 - Estado: PENDIENTE")
            self.assertFalse(any("Tarea2" in call[0][0] for call in mocked_print.call_args_list))

    # Test para listar tareas de un proyecto inexistente
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_listar_tareas_proyecto_inexistente(self):
        with patch("builtins.print") as mocked_print:
            listar_tareas("NoExiste")
            mocked_print.assert_called_with('Error: No se encontró el proyecto "NoExiste".')

    # Test para listar tareas con estado inválido
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_actualizar_tarea_exito(self):
        crear_tarea("TestProy", "Tarea1", "Descripción", "Juan", "2025-06-15", "PENDIENTE")
        actualizar_tarea("TestProy", "Tarea1", "COMPLETADA")
        data = cargar_datos()
        self.assertEqual(data[0]["tareas"][0]["estado"], "COMPLETADA")

    # Test para actualizar una tarea que no existe
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_actualizar_tarea_estado_invalido(self):
        crear_tarea("TestProy", "Tarea1", "Descripción", "Juan", "2025-06-15", "PENDIENTE")
        with patch("builtins.print") as mocked_print:
            actualizar_tarea("TestProy", "Tarea1", "INVALIDO")
            # Check error message regardless of order
            called_args = mocked_print.call_args[0][0]
            self.assertTrue(
                called_args.startswith("Error: Estado inválido. Debe ser uno de:") and
                "PENDIENTE" in called_args and
                "EN_PROGRESO" in called_args and
                "COMPLETADA" in called_args
            )

    # Test para actualizar una tarea que no existe
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_eliminar_tarea_exito(self):
        crear_tarea("TestProy", "Tarea1", "Descripción", "Juan", "2025-06-15", "PENDIENTE")
        eliminar_tarea("TestProy", "Tarea1")
        data = cargar_datos()
        self.assertEqual(len(data[0]["tareas"]), 0)

    # Test para eliminar una tarea que no existe
    @patch("guardado.ARCHIVO_DATOS", TEST_ARCHIVO)
    def test_eliminar_tarea_inexistente(self):
        with patch("builtins.print") as mocked_print:
            eliminar_tarea("TestProy", "TareaNoExiste")
            mocked_print.assert_called_with('Error: No se encontró la tarea "TareaNoExiste" en el proyecto "TestProy".')

    # Test para validar argumentos de la función validate_args
    def test_validate_args_correcto(self):
        args = ["main.py", "crear_proyecto", "Proyecto1", "Descripción", "2025-06-30"]
        result = validate_args("crear_proyecto", args, 5, "crear_proyecto \"Nombre\" \"Descripción\" \"AAAA-MM-DD\"")
        self.assertTrue(result)

    # Test para validar argumentos incorrectos
    def test_validate_args_incorrecto(self):
        args = ["main.py", "crear_proyecto", "Proyecto1"]
        with patch("builtins.print") as mocked_print:
            result = validate_args("crear_proyecto", args, 5, "crear_proyecto \"Nombre\" \"Descripción\" \"AAAA-MM-DD\"")
            self.assertFalse(result)
            mocked_print.assert_called_with("Uso: python main.py crear_proyecto \"Nombre\" \"Descripción\" \"AAAA-MM-DD\"")

if __name__ == "__main__":
    unittest.main()