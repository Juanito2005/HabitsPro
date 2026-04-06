import datetime
import memory_db
from utils import pedir_entero_rango, pedir_texto_obligatorio, pedir_fecha_opcional
from session_app import registrar_log

def mostrar_menu_habitos():
    # armamos el menu de habitos para la consola
    print("\n--- GESTIÓN DE HÁBITOS ---")
    print("1. Crear hábito")
    print("2. Listar hábitos")
    print("3. Marcar hábito como realizado")
    print("4. Ver detalle de hábito")
    print("5. Editar hábito")
    print("6. Eliminar hábito")
    print("7. Volver")

def crear_habito():
    print("\n--- NUEVO HÁBITO ---")
    nombre = pedir_texto_obligatorio("Nombre del hábito: ")
    
    while True:
        frecuencia = input("Frecuencia (diaria/semanal): ").strip().lower()
        if frecuencia in ["diaria", "semanal"]:
            break
        print("Error: Escribe 'diaria' o 'semanal'.")
        
    objetivo = pedir_entero_rango("Objetivo (veces por periodo, ej. 5): ", 1, 999)
    
    nuevo_habito = {
        "id": memory_db.next_habito_id,
        "nombre": nombre,
        "frecuencia": frecuencia,
        "objetivo": objetivo,
        "registros": []
    }
    
    memory_db.habitos.append(nuevo_habito)
    registrar_log("CREAR_HABITO", f"Creado hábito ID {nuevo_habito['id']} - '{nombre}'")
    print(f"\nHábito creado con éxito con ID: {nuevo_habito['id']}")
    
    memory_db.next_habito_id += 1

def listar_habitos():
    if not memory_db.habitos:
        print("\nNo hay hábitos registrados todavía.")
        return

    print("\nID | Frecuencia | Obj | Nombre")
    print("-" * 50)
    for h in memory_db.habitos:
        print(f"{h['id']:<2} | {h['frecuencia']:<10} | {h['objetivo']:<3} | {h['nombre']}")
    print("-" * 50)

def marcar_habito():
    if not memory_db.habitos:
        print("\nNo hay hábitos para marcar.")
        return

    id_buscar = pedir_entero_rango("\nID del hábito a marcar (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return

    habito = next((h for h in memory_db.habitos if h["id"] == id_buscar), None)
    if not habito:
        print("Error: Hábito no encontrado.")
        return

    fecha_input = pedir_fecha_opcional("Fecha de realización (YYYY-MM-DD, Enter para hoy): ")
    fecha_marca = fecha_input if fecha_input else datetime.datetime.now().strftime("%Y-%m-%d")

    # validamos la regla de no duplicar si es diario
    if habito["frecuencia"] == "diaria" and fecha_marca in habito["registros"]:
        print(f"Aviso: El hábito ya está marcado para la fecha {fecha_marca}.")
        return

    habito["registros"].append(fecha_marca)
    # ordenamos las fechas por si el usuario metio una fecha antigua
    habito["registros"].sort()
    
    registrar_log("MARCAR_HABITO", f"Hábito ID {habito['id']} marcado el {fecha_marca}")
    print("Hábito marcado como realizado.")

def ver_detalle_habito():
    if not memory_db.habitos:
        print("\nNo hay hábitos para ver.")
        return

    id_buscar = pedir_entero_rango("\nID del hábito (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return

    habito = next((h for h in memory_db.habitos if h["id"] == id_buscar), None)
    if not habito:
        print("Error: Hábito no encontrado.")
        return

    print(f"\n--- DETALLE: {habito['nombre']} ---")
    print(f"Frecuencia: {habito['frecuencia']}")
    print(f"Objetivo: {habito['objetivo']} veces por periodo")
    
    hoy = datetime.datetime.now().date()
    
    if habito["frecuencia"] == "diaria":
        print("\nCumplimiento últimos 7 días:")
        # sacamos los ultimos 7 dias restando fechas
        for i in range(6, -1, -1):
            dia = hoy - datetime.timedelta(days=i)
            dia_str = dia.strftime("%Y-%m-%d")
            estado = "[X] Hecho" if dia_str in habito["registros"] else "[ ] No hecho"
            print(f"{dia_str}: {estado}")
            
    elif habito["frecuencia"] == "semanal":
        año_actual, semana_actual, _ = hoy.isocalendar()
        registros_semana = 0
        
        # filtramos los registros que caigan en la misma semana del año
        for reg in habito["registros"]:
            fecha_reg = datetime.datetime.strptime(reg, "%Y-%m-%d").date()
            año_reg, semana_reg, _ = fecha_reg.isocalendar()
            if año_reg == año_actual and semana_reg == semana_actual:
                registros_semana += 1
                
        print(f"\nProgreso semana actual: {registros_semana} / {habito['objetivo']}")

def menu_habitos():
    while True:
        mostrar_menu_habitos()
        opcion = pedir_entero_rango("\nElige una opción: ", 1, 7)

        if opcion == 1:
            crear_habito()
        elif opcion == 2:
            listar_habitos()
        elif opcion == 3:
            marcar_habito()
        elif opcion == 4:
            ver_detalle_habito()
        elif opcion == 5:
            editar_habito()
        elif opcion == 6:
            eliminar_habito()
        elif opcion == 7:
            break

def editar_habito():
    if not memory_db.habitos:
        print("\nNo hay hábitos para editar.")
        return

    id_buscar = pedir_entero_rango("\nID del hábito a editar (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return

    habito = next((h for h in memory_db.habitos if h["id"] == id_buscar), None)
    if not habito:
        print("Error: Hábito no encontrado.")
        return

    print("\n--- EDITANDO HÁBITO (Presiona ENTER para dejar igual) ---")
    cambios = []

    nuevo_nombre = input(f"Nombre [{habito['nombre']}]: ").strip()
    if nuevo_nombre:
        habito['nombre'] = nuevo_nombre
        cambios.append("nombre")

    while True:
        nueva_frec = input(f"Frecuencia (diaria/semanal) [{habito['frecuencia']}]: ").strip().lower()
        if not nueva_frec:
            break
        if nueva_frec in ["diaria", "semanal"]:
            habito['frecuencia'] = nueva_frec
            cambios.append("frecuencia")
            break
        print("Error: Escribe 'diaria' o 'semanal'.")

    while True:
        nuevo_obj = input(f"Objetivo [{habito['objetivo']}]: ").strip()
        if not nuevo_obj:
            break
        try:
            obj_int = int(nuevo_obj)
            if obj_int >= 1:
                habito['objetivo'] = obj_int
                cambios.append("objetivo")
                break
            print("Error: Debe ser mayor o igual a 1.")
        except ValueError:
            print("Error: Ingresa un número.")

    if cambios:
        registrar_log("EDITAR_HABITO", f"Hábito {habito['id']} editado: {', '.join(cambios)}")
        print("Hábito actualizado, que chevere.")
    else:
        print("No se hicieron cambios.")

def eliminar_habito():
    if not memory_db.habitos:
        print("\nNo hay hábitos registrados.")
        return

    id_buscar = pedir_entero_rango("\nID del hábito a eliminar (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return

    habito = next((h for h in memory_db.habitos if h["id"] == id_buscar), None)
    if not habito:
        print("Error: Hábito no encontrado.")
        return

    print(f"\nResumen -> ID: {habito['id']} | Nombre: {habito['nombre']}")
    confirmacion = input("Escribe exactamente ELIMINAR para confirmar: ")
    
    if confirmacion == "ELIMINAR":
        memory_db.habitos.remove(habito)
        registrar_log("ELIMINAR_HABITO", f"Eliminado hábito ID {habito['id']}")
        print("Hábito borrado.")
    else:
        print("Operación cancelada.")