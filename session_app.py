import datetime
import math
import memory_db

def registrar_log(accion: str, detalle: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = {
        "timestamp": timestamp,
        "accion": accion,
        "detalle": detalle
    }
    memory_db.log_sesion.append(entrada)

def mostrar_log():
    if not memory_db.log_sesion:
        print("\nEl log está vacío, bro.")
        return

    total = len(memory_db.log_sesion)
    por_pagina = 15
    total_paginas = math.ceil(total / por_pagina)
    pagina_actual = 1

    while True:
        inicio = (pagina_actual - 1) * por_pagina
        fin = inicio + por_pagina
        
        print(f"\n--- LOG DE SESIÓN (Página {pagina_actual}/{total_paginas}) ---")
        print("Timestamp           | Acción         | Detalle")
        print("-" * 70)
        
        # sacamos el pedazo de la lista que toca mostrar con slicing, bien facil
        for entrada in memory_db.log_sesion[inicio:fin]:
            print(f"{entrada['timestamp']} | {entrada['accion']:<14} | {entrada['detalle']}")
        print("-" * 70)

        print("\nControles: [n] Siguiente | [p] Anterior | [0] Volver")
        comando = input("¿Qué hacemos?: ").strip().lower()

        if comando == '0':
            break
        elif comando == 'n' and pagina_actual < total_paginas:
            pagina_actual += 1
        elif comando == 'p' and pagina_actual > 1:
            pagina_actual -= 1
        else:
            print("Comando no válido o llegaste al tope.")

def limpiar_log():
    print("\nCuidado, vas a borrar todo el historial.")
    conf = input("Escribe exactamente LIMPIAR para confirmar: ")
    if conf == "LIMPIAR":
        memory_db.log_sesion.clear()
        registrar_log("LIMPIAR_LOG", "El log de sesión fue reseteado")
        print("Log limpio, que chevere.")
    else:
        print("Cancelado. Todo sigue igual.")