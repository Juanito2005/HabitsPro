from datetime import datetime, date

def pedir_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:
    while True:
        entrada = input(mensaje)
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"Error: El número debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("Error: Debes introducir un número entero válido.")

def pedir_texto_obligatorio(mensaje: str, max_longitud: int = None) -> str:
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Error: El texto no puede estar vacío.")
            continue
        if max_longitud and len(texto) > max_longitud:
            print(f"Error: El texto excede el máximo de {max_longitud} caracteres.")
            continue
        return texto

def pedir_fecha_opcional(mensaje: str) -> str:
    # pedimos la fecha validando que no pongan años loquisimos ni viajen al futuro
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            return ""
        try:
            fecha_validada = datetime.strptime(entrada, "%Y-%m-%d").date()
            hoy = date.today()
            
            # bloqueamos registros que no tienen sentido para la app
            if fecha_validada.year < 2023:
                print("Error: La fecha es demasiado antigua, bro.")
                continue
            if fecha_validada > hoy:
                print("Error: No puedes registrar fechas en el futuro.")
                continue
                
            return fecha_validada.strftime("%Y-%m-%d")
        except ValueError:
            print("Error: Formato incorrecto. Usa YYYY-MM-DD.")

def pedir_etiquetas(mensaje: str) -> list:
    entrada = input(mensaje)
    etiquetas = [etiqueta.strip().lower() for etiqueta in entrada.split(',') if etiqueta.strip()]
    return etiquetas