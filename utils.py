from datetime import datetime

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

    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            return ""
        try:
            fecha_validada = datetime.strptime(entrada, "%Y-%m-%d").date()
            return fecha_validada.strftime("%Y-%m-%d")
        except ValueError:
            print("Error: Formato de fecha incorrecto. Usa YYYY-MM-DD.")

def pedir_etiquetas(mensaje: str) -> list:
    entrada = input(mensaje)
    etiquetas = [etiqueta.strip().lower() for etiqueta in entrada.split(',') if etiqueta.strip()]
    return etiquetas