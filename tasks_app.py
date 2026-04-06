import datetime
import memory_db
import math
from utils import pedir_entero_rango, pedir_texto_obligatorio, pedir_fecha_opcional, pedir_etiquetas
from session_app import registrar_log

def mostrar_menu_tareas():
    # un menu simplecito para navegar por las tareas
    print("\n--- GESTIÓN DE TAREAS ---")
    print("1. Crear tarea")
    print("2. Listar tareas")
    print("3. Ver detalle de una tarea")
    print("4. Cambiar estado")
    print("5. Editar tarea")
    print("6. Eliminar tarea")
    print("7. Plan del día")
    print("8. Volver")

def crear_tarea():
    print("\n--- NUEVA TAREA ---")
    
    # pidiendo los datos con las utilidades para que la consola no crashee
    titulo = pedir_texto_obligatorio("Título (máx 60 chars): ", 60)
    descripcion = input("Descripción (opcional, Enter para saltar): ").strip()
    prioridad = pedir_entero_rango("Prioridad (1=baja, 2=media, 3=alta): ", 1, 3)
    fecha_vencimiento = pedir_fecha_opcional("Fecha de vencimiento (YYYY-MM-DD, Enter para saltar): ")
    
    print("Etiquetas (separadas por coma, ej: urgente, casa). Enter para saltar.")
    etiquetas = pedir_etiquetas("Etiquetas: ")
    
    # hacemos un while rapido para validar el entero opcional sin crear otra funcion gigante
    while True:
        tiempo_input = input("Tiempo estimado en min (opcional, Enter para saltar): ").strip()
        if not tiempo_input:
            tiempo_estimado_min = None
            break
        try:
            tiempo_estimado_min = int(tiempo_input)
            if tiempo_estimado_min >= 0:
                break
            print("Error: El tiempo no puede ser negativo, bro.")
        except ValueError:
            print("Error: Pon un número válido o dale Enter.")

    # armamos el diccionario tipo JSON para guardar en la lista de memoria
    nueva_tarea = {
        "id": memory_db.next_tarea_id,
        "titulo": titulo,
        "descripcion": descripcion if descripcion else None,
        "prioridad": prioridad,
        "estado": "pendiente",
        "fecha_creacion": datetime.datetime.now().strftime("%Y-%m-%d"),
        "fecha_vencimiento": fecha_vencimiento if fecha_vencimiento else None,
        "etiquetas": etiquetas,
        "tiempo_estimado_min": tiempo_estimado_min,
        "tiempo_real_min": None
    }

    memory_db.tareas.append(nueva_tarea)
    registrar_log("CREAR_TAREA", f"Creada tarea ID {memory_db.next_tarea_id} - '{titulo}'")
    print(f"\nTarea creada con éxito con ID: {memory_db.next_tarea_id}")
    
    memory_db.next_tarea_id += 1

def menu_tareas():
    while True:
        mostrar_menu_tareas()
        opcion = pedir_entero_rango("\nElige una opción: ", 1, 8)

        if opcion == 1:
            crear_tarea()
        elif opcion == 2:
            listar_tareas()
        elif opcion == 3:
            ver_detalle_tarea()
        elif opcion == 4:
            cambiar_estado_tarea()
        elif opcion == 5:
            editar_tarea()
        elif opcion == 6:
            eliminar_tarea()
        elif opcion == 7:
            plan_del_dia()
        elif opcion == 8:
            break

def listar_tareas():
    if not memory_db.tareas:
        print("\nNo hay tareas registradas todavía.")
        return

    print("\nOpciones de orden:")
    print("1. Por prioridad (alta a baja)")
    print("2. Por fecha de vencimiento (sin fecha al final)")
    print("3. Por estado")
    print("4. Por título (A-Z)")
    print("5. Sin orden (por ID)")
    
    orden_op = input("Elige cómo ordenar (1-5, Enter para default): ").strip()
    
    # clonamos la lista para no alterar el orden real en memoria, todo seguro
    lista_mostrar = memory_db.tareas.copy()
    
    if orden_op == '1':
        lista_mostrar.sort(key=lambda x: x['prioridad'], reverse=True)
    elif orden_op == '2':
        # usamos una tupla en el lambda para mandar los None al final
        lista_mostrar.sort(key=lambda x: (x['fecha_vencimiento'] is None, x['fecha_vencimiento']))
    elif orden_op == '3':
        lista_mostrar.sort(key=lambda x: x['estado'])
    elif orden_op == '4':
        lista_mostrar.sort(key=lambda x: x['titulo'].lower())

    por_pagina = 10
    total_paginas = math.ceil(len(lista_mostrar) / por_pagina)
    pagina_actual = 1

    while True:
        inicio = (pagina_actual - 1) * por_pagina
        fin = inicio + por_pagina
        
        print(f"\n--- LISTA DE TAREAS (Página {pagina_actual}/{total_paginas}) ---")
        print("ID | Prio | Estado     | Vence      | Título")
        print("-" * 65)
        
        for t in lista_mostrar[inicio:fin]:
            vence = t["fecha_vencimiento"] if t["fecha_vencimiento"] else "Sin fecha"
            print(f"{t['id']:<2} | {t['prioridad']:<4} | {t['estado']:<10} | {vence:<10} | {t['titulo']}")
        print("-" * 65)

        print("\nControles: [n] Siguiente | [p] Anterior | [0] Volver")
        comando = input("Comando: ").strip().lower()

        if comando == '0':
            break
        elif comando == 'n' and pagina_actual < total_paginas:
            pagina_actual += 1
        elif comando == 'p' and pagina_actual > 1:
            pagina_actual -= 1
        else:
            print("Comando no válido o fin de la lista.")

def ver_detalle_tarea():
    if not memory_db.tareas:
        print("\nNo hay tareas para buscar.")
        return

    id_buscar = pedir_entero_rango("\nID de la tarea a ver (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return
    
    # buscamos la tarea iterando la lista como unos pros
    tarea_encontrada = next((t for t in memory_db.tareas if t["id"] == id_buscar), None)

    if not tarea_encontrada:
        print("Error: No existe ninguna tarea con ese ID.")
        return

    print("\n--- DETALLE DE TAREA ---")
    for clave, valor in tarea_encontrada.items():
        if clave == "etiquetas":
            valor = ", ".join(valor) if valor else "Ninguna"
        print(f"{clave.capitalize()}: {valor}")

def cambiar_estado_tarea():
    if not memory_db.tareas:
        print("\nNo hay tareas registradas.")
        return

    id_buscar = pedir_entero_rango("\nID de la tarea a modificar (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return

    tarea = next((t for t in memory_db.tareas if t["id"] == id_buscar), None)
    
    if not tarea:
        print("Error: Tarea no encontrada.")
        return

    print(f"\nEstado actual: {tarea['estado']}")
    print("1. pendiente\n2. en_progreso\n3. hecha\n4. cancelada\n5. cancelar operación")

    opcion = pedir_entero_rango("Selecciona el nuevo estado: ", 1, 5)
    estados = {1: "pendiente", 2: "en_progreso", 3: "hecha", 4: "cancelada"}
    
    if opcion == 5:
        return
        
    nuevo_estado = estados[opcion]
    estado_anterior = tarea["estado"]

    if nuevo_estado == estado_anterior:
        print("La tarea ya tiene ese estado.")
        return

    # aplicando las reglas locas de negocio del documento
    if estado_anterior == "hecha" and nuevo_estado == "en_progreso":
        conf = input("La tarea ya estaba hecha. ¿Seguro que quieres pasarla a en progreso? Escribe SI: ")
        if conf != "SI":
            print("Operación cancelada.")
            return
    
    if estado_anterior == "cancelada" and nuevo_estado == "en_progreso":
        print("Error: Una tarea cancelada debe pasar a pendiente antes de estar en progreso.")
        return

    if nuevo_estado == "hecha":
        while True:
            tiempo_input = input("¿Tiempo real (min)? (Enter para 0): ").strip()
            if not tiempo_input:
                tarea["tiempo_real_min"] = 0
                break
            try:
                t_real = int(tiempo_input)
                if t_real >= 0:
                    tarea["tiempo_real_min"] = t_real
                    break
                print("Error: No puedes poner tiempo negativo.")
            except ValueError:
                print("Error: Pon un número válido.")
    
    tarea["estado"] = nuevo_estado
    registrar_log("CAMBIO_ESTADO", f"Tarea {tarea['id']} pasó de {estado_anterior} a {nuevo_estado}")
    print("Estado actualizado :)")

def editar_tarea():
    if not memory_db.tareas:
        print("\nNo hay tareas para editar.")
        return

    id_buscar = pedir_entero_rango("\nID de la tarea a editar (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return

    tarea = next((t for t in memory_db.tareas if t["id"] == id_buscar), None)
    if not tarea:
        print("Error: Tarea no encontrada.")
        return

    print("\n--- EDITANDO TAREA (Presiona ENTER para dejar el valor igual) ---")
    cambios_log = []

    # para el titulo validamos la longitud si el usuario decide cambiarlo
    nuevo_titulo = input(f"Título [{tarea['titulo']}]: ").strip()
    if nuevo_titulo:
        while len(nuevo_titulo) > 60:
            print("Error: Máximo 60 caracteres.")
            nuevo_titulo = input(f"Título [{tarea['titulo']}]: ").strip()
        tarea['titulo'] = nuevo_titulo
        cambios_log.append("titulo")

    nueva_desc = input(f"Descripción [{tarea['descripcion'] or ''}]: ").strip()
    if nueva_desc:
        tarea['descripcion'] = nueva_desc
        cambios_log.append("descripcion")

    while True:
        nueva_prio = input(f"Prioridad (1-3) [{tarea['prioridad']}]: ").strip()
        if not nueva_prio:
            break
        try:
            prio_int = int(nueva_prio)
            if prio_int in [1, 2, 3]:
                tarea['prioridad'] = prio_int
                cambios_log.append("prioridad")
                break
            print("Error: Debe ser 1, 2 o 3.")
        except ValueError:
            print("Error: Ingresa un número.")

    # las fechas en python se pueden comparar directo como strings si tienen formato YYYY-MM-DD
    nueva_fecha = input(f"Vencimiento (YYYY-MM-DD) [{tarea['fecha_vencimiento'] or 'Ninguna'}]: ").strip()
    if nueva_fecha:
        try:
            datetime.datetime.strptime(nueva_fecha, "%Y-%m-%d")
            tarea['fecha_vencimiento'] = nueva_fecha
            cambios_log.append("fecha_vencimiento")
        except ValueError:
            print("Error: Formato inválido. Se mantiene la fecha anterior.")

    etiquetas_str = ", ".join(tarea['etiquetas']) if tarea['etiquetas'] else ""
    nuevas_etiq = input(f"Etiquetas separadas por coma [{etiquetas_str}]: ")
    if nuevas_etiq.strip():
        # reutilizamos la logica de la funcion de utils directamente aca
        tarea['etiquetas'] = [e.strip().lower() for e in nuevas_etiq.split(',') if e.strip()]
        cambios_log.append("etiquetas")

    while True:
        nuevo_tiempo = input(f"Tiempo estimado min [{tarea['tiempo_estimado_min'] or 0}]: ").strip()
        if not nuevo_tiempo:
            break
        try:
            t_int = int(nuevo_tiempo)
            if t_int >= 0:
                tarea['tiempo_estimado_min'] = t_int
                cambios_log.append("tiempo_estimado")
                break
            print("Error: No puede ser negativo.")
        except ValueError:
            print("Error: Ingresa un número.")

    if cambios_log:
        registrar_log("EDITAR_TAREA", f"Editada tarea {tarea['id']}. Cambios en: {', '.join(cambios_log)}")
        print("Tarea actualizada.")
    else:
        print("No se hicieron cambios.")

def eliminar_tarea():
    if not memory_db.tareas:
        print("\nNo hay tareas registradas.")
        return

    id_buscar = pedir_entero_rango("\nID de la tarea a eliminar (0 para cancelar): ", 0, 999999)
    if id_buscar == 0:
        return

    tarea = next((t for t in memory_db.tareas if t["id"] == id_buscar), None)
    if not tarea:
        print("Error: Tarea no encontrada.")
        return

    print(f"\nResumen -> ID: {tarea['id']} | Título: {tarea['titulo']} | Estado: {tarea['estado']}")
    confirmacion = input("Escribe exactamente ELIMINAR para confirmar: ")
    
    if confirmacion == "ELIMINAR":
        memory_db.tareas.remove(tarea)
        registrar_log("ELIMINAR_TAREA", f"Eliminada tarea ID {tarea['id']}")
        print("Tarea borrada del sistema, que chevere.")
    else:
        print("Operación cancelada. No se eliminó nada.")

def plan_del_dia():
    if not memory_db.tareas:
        print("\nNo hay tareas en el sistema.")
        return

    hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # separamos las listas segun las reglas de negocio usando list comprehensions
    urgentes = [t for t in memory_db.tareas if t["estado"] in ["pendiente", "en_progreso"] 
                and t["fecha_vencimiento"] and t["fecha_vencimiento"] <= hoy]
    
    pendientes = [t for t in memory_db.tareas if t["estado"] == "pendiente" and t not in urgentes]
    en_progreso = [t for t in memory_db.tareas if t["estado"] == "en_progreso" and t not in urgentes]

    # ordenamos las pendientes por prioridad usando lambda (3 es mas alto, por eso reverse=True)
    pendientes.sort(key=lambda x: x["prioridad"], reverse=True)

    plan = urgentes + pendientes + en_progreso

    if not plan:
        print("\nNo hay tareas activas para mostrar en el plan del día.")
        return

    print("\n--- PLAN DEL DÍA ---")
    print("ID | Prioridad | Estado     | Vence      | Título")
    print("-" * 65)
    for t in plan:
        vence = t["fecha_vencimiento"] if t["fecha_vencimiento"] else "Sin fecha"
        print(f"{t['id']:<2} | {t['prioridad']:<9} | {t['estado']:<10} | {vence:<10} | {t['titulo']}")
    print("-" * 65)