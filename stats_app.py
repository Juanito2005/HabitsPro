import datetime
from collections import Counter
import memory_db
from utils import pedir_entero_rango

def stats_estado():
    if not memory_db.tareas:
        print("\nNo hay tareas.")
        return
    
    # Counter hace todo el trabajo de agrupar y contar por nosotros
    conteo = Counter(t["estado"] for t in memory_db.tareas)
    print("\n--- TAREAS POR ESTADO ---")
    for estado, cantidad in conteo.items():
        print(f"{estado.capitalize()}: {cantidad}")

def stats_prioridad():
    if not memory_db.tareas:
        print("\nNo hay tareas.")
        return
        
    conteo = Counter(t["prioridad"] for t in memory_db.tareas)
    print("\n--- TAREAS POR PRIORIDAD ---")
    for prio in [3, 2, 1]:
        print(f"Prioridad {prio}: {conteo.get(prio, 0)}")

def stats_vencidas():
    hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    vencidas = [t for t in memory_db.tareas if t["estado"] not in ["hecha", "cancelada"] 
                and t["fecha_vencimiento"] and t["fecha_vencimiento"] < hoy]
    
    print(f"\n--- TAREAS VENCIDAS: {len(vencidas)} ---")
    for t in vencidas:
        print(f"ID: {t['id']} | Venció el: {t['fecha_vencimiento']} | Título: {t['titulo']}")

def stats_tiempos():
    hechas = [t for t in memory_db.tareas if t["estado"] == "hecha" 
              and t["tiempo_estimado_min"] is not None and t["tiempo_real_min"] is not None]
    
    if not hechas:
        print("\nNo hay tareas hechas con datos de tiempo para comparar.")
        return
        
    print("\n--- TIEMPO ESTIMADO VS REAL ---")
    # sum toma un generador y suma todo directo
    total_estimado = sum(t["tiempo_estimado_min"] for t in hechas)
    total_real = sum(t["tiempo_real_min"] for t in hechas)
    
    print(f"Total Estimado: {total_estimado} min")
    print(f"Total Real: {total_real} min")
    
    diferencia = total_real - total_estimado
    if diferencia > 0:
        print(f"Te pasaste por {diferencia} minutos en total.")
    elif diferencia < 0:
        print(f"Ahorraste {abs(diferencia)} minutos, buenísimo.")
    else:
        print("Calculaste el tiempo exacto.")

def stats_top_etiquetas():
    todas_etiquetas = []
    for t in memory_db.tareas:
        # extend añade los elementos de la lista, no la lista como tal
        todas_etiquetas.extend(t["etiquetas"])
        
    if not todas_etiquetas:
        print("\nNo hay etiquetas usadas todavía.")
        return
        
    conteo = Counter(todas_etiquetas)
    print("\n--- TOP 5 ETIQUETAS ---")
    for etiqueta, cantidad in conteo.most_common(5):
        print(f"{etiqueta}: {cantidad} usos")

def stats_habitos():
    if not memory_db.habitos:
        print("\nNo hay hábitos registrados.")
        return
        
    print("\n--- PROGRESO DE HÁBITOS ---")
    for h in memory_db.habitos:
        total_marcas = len(h["registros"])
        print(f"[{h['id']}] {h['nombre']} ({h['frecuencia']}): {total_marcas} veces marcado en total. Objetivo: {h['objetivo']}")

def menu_estadisticas():
    while True:
        print("\n--- ESTADÍSTICAS ---")
        print("1. Tareas por estado")
        print("2. Tareas por prioridad")
        print("3. Tareas vencidas")
        print("4. Tiempo estimado vs real")
        print("5. Top 5 etiquetas")
        print("6. Progreso de hábitos")
        print("7. Volver")
        
        opcion = pedir_entero_rango("\nElige una opción: ", 1, 7)
        
        if opcion == 1:
            stats_estado()
        elif opcion == 2:
            stats_prioridad()
        elif opcion == 3:
            stats_vencidas()
        elif opcion == 4:
            stats_tiempos()
        elif opcion == 5:
            stats_top_etiquetas()
        elif opcion == 6:
            stats_habitos()
        elif opcion == 7:
            break