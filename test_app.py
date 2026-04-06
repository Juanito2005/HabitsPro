import unittest
from unittest.mock import patch
import memory_db
from tasks_app import crear_tarea, cambiar_estado_tarea, editar_tarea, eliminar_tarea, listar_tareas
from habits_app import marcar_habito
from filters_app import aplicar_filtros, restablecer_filtros, filtros_activos

class TestProductividadCLI(unittest.TestCase):

    def setUp(self):
        # reseteamos la memoria antes de cada test para que no choquen entre si
        memory_db.tareas.clear()
        memory_db.habitos.clear()
        memory_db.log_sesion.clear()
        memory_db.next_tarea_id = 1
        memory_db.next_habito_id = 1
        restablecer_filtros()

    # Casos 1, 2 y 3: Título vacío, Prioridad 9, Sin vencimiento
    @patch('builtins.input', side_effect=[
        "", "Mi Tarea",      # Falla titulo, luego acierta
        "",                  # Descripcion opcional
        "9", "2",            # Falla prioridad, luego acierta
        "",                  # Vencimiento opcional (prueba 3: lo permite)
        "",                  # Etiquetas
        ""                   # Tiempo estimado
    ])
    def test_crear_tarea_validaciones(self, mock_input):
        crear_tarea()
        self.assertEqual(len(memory_db.tareas), 1)
        tarea = memory_db.tareas[0]
        self.assertEqual(tarea["titulo"], "Mi Tarea")
        self.assertEqual(tarea["prioridad"], 2)
        self.assertIsNone(tarea["fecha_vencimiento"])

    # Caso 4: Marcar hecha pide tiempo real
    @patch('builtins.input', side_effect=[
        "1",     # ID de la tarea
        "3",     # Opcion 3 (hecha)
        "45"     # Tiempo real en min
    ])
    def test_marcar_hecha_pide_tiempo(self, mock_input):
        # metemos una tarea directo a memoria para saltar la creacion
        memory_db.tareas.append({"id": 1, "estado": "pendiente", "tiempo_real_min": None})
        cambiar_estado_tarea()
        
        self.assertEqual(memory_db.tareas[0]["estado"], "hecha")
        self.assertEqual(memory_db.tareas[0]["tiempo_real_min"], 45)

    # Caso 5: Filtrar por etiqueta inexistente
    def test_filtrar_etiqueta_inexistente(self):
        memory_db.tareas.append({"id": 1, "etiquetas": ["urgente"], "estado": "pendiente", "prioridad": 1, "titulo": "A", "fecha_vencimiento": None})
        
        filtros_activos["etiqueta"] = "python"
        resultados = aplicar_filtros()
        
        # no debe dar error, solo devolver una lista vacia
        self.assertEqual(len(resultados), 0)

    # Caso 6: Hábito diario no se duplica
    @patch('builtins.input', side_effect=[
        "1",           # ID del habito
        "2024-10-10"   # Fecha manual
    ])
    def test_habito_diario_no_duplica(self, mock_input):
        memory_db.habitos.append({
            "id": 1,
            "frecuencia": "diaria",
            "registros": ["2024-10-10"] # ya tiene esta fecha
        })
        
        marcar_habito()
        
        # la longitud de registros debe seguir siendo 1
        self.assertEqual(len(memory_db.habitos[0]["registros"]), 1)

    # Caso 7: Listar con paginación n/p no rompe
    @patch('builtins.input', side_effect=[
        "5",   # Orden por defecto
        "n",   # Siguiente
        "p",   # Anterior
        "0"    # Salir
    ])
    @patch('sys.stdout') # silenciamos los prints de la consola para no ensuciar el test
    def test_paginacion_lista_tareas(self, mock_stdout, mock_input):
        for i in range(15):
            memory_db.tareas.append({"id": i+1, "titulo": f"T{i}", "prioridad": 1, "estado": "pendiente", "fecha_vencimiento": None})
        
        # si esta funcion termina sin lanzar excepciones, el test pasa, que chevere
        listar_tareas()
        self.assertTrue(True)

    # Caso 8: Editar con ENTER en todo no cambia nada
    @patch('builtins.input', side_effect=[
        "1", # ID a editar
        "",  # Titulo
        "",  # Desc
        "",  # Prio
        "",  # Fecha
        "",  # Etiquetas
        ""   # Tiempo
    ])
    def test_editar_con_enter_no_muta(self, mock_input):
        original = {"id": 1, "titulo": "Original", "descripcion": None, "prioridad": 1, "fecha_vencimiento": "2026-12-31", "etiquetas": [], "tiempo_estimado_min": 10}
        memory_db.tareas.append(original.copy())
        
        editar_tarea()
        
        # comprobamos que el diccionario siga exactamente igual
        self.assertEqual(memory_db.tareas[0], original)

    # Caso 9: Eliminar sin escribir ELIMINAR cancela
    @patch('builtins.input', side_effect=[
        "1",      # ID
        "NO"      # Escribe algo distinto a ELIMINAR
    ])
    def test_eliminar_sin_confirmacion_exacta(self, mock_input):
        memory_db.tareas.append({"id": 1, "titulo": "Prueba", "estado": "pendiente"})
        
        eliminar_tarea()
        
        # la lista sigue teniendo la tarea
        self.assertEqual(len(memory_db.tareas), 1)

if __name__ == '__main__':
    unittest.main()