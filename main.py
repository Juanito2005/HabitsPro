import sys
from utils import pedir_entero_rango
from session_app import registrar_log, mostrar_log, limpiar_log
from tasks_app import menu_tareas
from habits_app import menu_habitos
from filters_app import menu_filtros
from stats_app import menu_estadisticas
# Los otros módulos se importarán aquí cuando los creemos

def mostrar_menu_principal():
    # Todo bien, armamos el menú principal tal cual pide el documento
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Gestión de tareas")
    print("2. Gestión de hábitos")
    print("3. Búsqueda y filtros")
    print("4. Estadísticas")
    print("5. Registro de sesión")
    print("6. Salir")

def iniciar_app():
    registrar_log("INICIO_APP", "La aplicación ha arrancado")

    while True:
        mostrar_menu_principal()
        opcion = pedir_entero_rango("\nSeleccione una opción: ", 1, 6)

        if opcion == 1:
            menu_tareas()
        elif opcion == 2:
            menu_habitos()
        elif opcion == 3:
            menu_filtros()
        elif opcion == 4:
            menu_estadisticas()
        elif opcion == 5:
            while True:
                print("\n--- REGISTRO DE SESIÓN ---")
                print("1. Ver log paginado")
                print("2. Limpiar log")
                print("3. Volver")
                sub_op = pedir_entero_rango("Selecciona: ", 1, 3)
                if sub_op == 1:
                    mostrar_log()
                elif sub_op == 2:
                    limpiar_log()
                elif sub_op == 3:
                    break
        elif opcion == 6:
            print("\nLos datos no se guardan. Al salir se perderá todo.")
            confirmacion = input("¿Confirmar salida? (s/n): ").strip().lower()
            # Aguanta, confirmamos pa' no embarrarla saliendo sin querer
            if confirmacion == 's':
                registrar_log("FIN_APP", "Cierre de la aplicación")
                print("Saliendo del sistema...")
                sys.exit(0)

if __name__ == "__main__":
    # Aquí arranca el script, mi pez
    iniciar_app()