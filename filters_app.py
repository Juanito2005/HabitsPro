import datetime
import math
import memory_db
from utils import pedir_entero_rango

# guardamos los filtros activos en un diccionario global a nivel de modulo
filtros_activos = {
    "estado": None,
    "prio_minima": None,
    "etiqueta": None,
    "palabra_titulo": None,
    "solo_vencidas": False,
    "vencen_hoy": False,
    "sin_vencimiento": False
}

def restablecer_filtros():
    for clave in filtros_activos:
        # si es booleano lo pasamos a false, si es texto/numero a None
        filtros_activos[clave] = False if isinstance(filtros_activos[clave], bool) else None
    print("\nFiltros limpiados, todo por defecto.")

def aplicar_filtros():
    hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    resultados = []

    for t in memory_db.tareas:
        cumple = True
        
        if filtros_activos["estado"] and t["estado"] != filtros_activos["estado"]:
            cumple = False
        if filtros_activos["prio_minima"] and t["prioridad"] < filtros_activos["prio_minima"]:
            cumple = False
        if filtros_activos["etiqueta"] and filtros_activos["etiqueta"] not in t["etiquetas"]:
            cumple = False
        if filtros_activos["palabra_titulo"] and filtros_activos["palabra_titulo"] not in t["titulo"].lower():
            cumple = False
            
        vence = t["fecha_vencimiento"]
        if filtros_activos["solo_vencidas"] and (not vence or vence >= hoy):
            cumple = False
        if filtros_activos["vencen_hoy"] and vence != hoy:
            cumple = False
        if filtros_activos["sin_vencimiento"] and vence is not None:
            cumple = False

        if cumple:
            resultados.append(t)
            
    return resultados

def mostrar_resultados_paginados(resultados):
    if not resultados:
        print("\nNinguna tarea cumple con los filtros actuales.")
        return

    total = len(resultados)
    por_pagina = 10
    total_paginas = math.ceil(total / por_pagina)
    pagina_actual = 1

    while True:
        inicio = (pagina_actual - 1) * por_pagina
        fin = inicio + por_pagina
        
        print(f"\n--- RESULTADOS: {total} (Página {pagina_actual}/{total_paginas}) ---")
        print("ID | Prio | Estado     | Vence      | Título")
        print("-" * 65)
        
        for t in resultados[inicio:fin]:
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
            print("Comando inválido o fin de resultados.")

def menu_filtros():
    while True:
        # mostramos el estado de los filtros para que el usuario no ande ciego
        print("\n--- BÚSQUEDA Y FILTROS ---")
        print(f"1. Estado: {filtros_activos['estado']}")
        print(f"2. Prio Mínima: {filtros_activos['prio_minima']}")
        print(f"3. Etiqueta (contiene): {filtros_activos['etiqueta']}")
        print(f"4. Palabra en título: {filtros_activos['palabra_titulo']}")
        print(f"5. Solo vencidas: {filtros_activos['solo_vencidas']}")
        print(f"6. Vencen hoy: {filtros_activos['vencen_hoy']}")
        print(f"7. Sin vencimiento: {filtros_activos['sin_vencimiento']}")
        print("8. Restablecer filtros")
        print("9. Aplicar filtros y ver resultados")
        print("10. Volver")

        opcion = pedir_entero_rango("\nElige una opción: ", 1, 10)

        if opcion == 1:
            estado = input("Estado (pendiente/en_progreso/hecha/cancelada): ").strip().lower()
            if estado in ["pendiente", "en_progreso", "hecha", "cancelada"]:
                filtros_activos["estado"] = estado
            else:
                print("Estado inválido.")
        elif opcion == 2:
            filtros_activos["prio_minima"] = pedir_entero_rango("Prioridad mínima (1-3): ", 1, 3)
        elif opcion == 3:
            filtros_activos["etiqueta"] = input("Etiqueta a buscar: ").strip().lower()
        elif opcion == 4:
            filtros_activos["palabra_titulo"] = input("Palabra a buscar: ").strip().lower()
        elif opcion == 5:
            filtros_activos["solo_vencidas"] = not filtros_activos["solo_vencidas"]
        elif opcion == 6:
            filtros_activos["vencen_hoy"] = not filtros_activos["vencen_hoy"]
        elif opcion == 7:
            filtros_activos["sin_vencimiento"] = not filtros_activos["sin_vencimiento"]
        elif opcion == 8:
            restablecer_filtros()
        elif opcion == 9:
            resultados = aplicar_filtros()
            mostrar_resultados_paginados(resultados)
        elif opcion == 10:
            break