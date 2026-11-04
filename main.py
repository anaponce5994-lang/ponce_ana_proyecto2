"""Script principal interactivo de la red de transporte.

Ejecutar con:  python3 main.py
"""

import math
from pathlib import Path

from grafo import Grafo
from io_handler import (
    cargar_grafo,
    convertir_peso,
    guardar_arista,
    guardar_ruta_json,
    normalizar_nodo,
)

CARPETA: Path = Path(__file__).parent
RUTA_CSV: Path = CARPETA / "nodos.csv"
RUTA_JSON: Path = CARPETA / "historial_rutas.json"

MENU: str = """
=========== RED DE TRANSPORTE ===========
 1. Ingresar nueva conexión
 2. Ver nodos y conexiones
 3. Calcular ruta más corta (Dijkstra)
 4. Salir
========================================="""


def pedir_nodo(mensaje: str) -> str:
    """Pide el nombre de un nodo hasta que no esté vacío."""
    while True:
        nombre = normalizar_nodo(input(mensaje))
        if nombre:
            return nombre
        print("  ✗ El nombre del nodo no puede estar vacío. Intenta de nuevo.")


def pedir_peso(mensaje: str) -> float:
    """Pide el peso de la arista hasta que sea un número positivo.

    Usa try-except para que un texto como "cinco", un número negativo
    o un campo vacío no detengan el programa.
    """
    while True:
        try:
            peso = convertir_peso(input(mensaje))
            if not math.isfinite(peso):
                raise ValueError("el peso debe ser un número finito")
            if peso <= 0:
                raise ValueError("el peso debe ser mayor que cero")
            return peso
        except ValueError as error:
            print(f"  ✗ Error: {error}. Intenta de nuevo (ejemplo: 4.5).")


def ingresar_conexion(grafo: Grafo) -> Grafo:
    """Captura una conexión, la guarda en el CSV y recarga el grafo."""
    print("\n--- Nueva conexión ---")
    origen = pedir_nodo("  Nodo origen: ")
    destino = pedir_nodo("  Nodo destino: ")
    if origen == destino:
        print("  ✗ El origen y el destino deben ser distintos.")
        return grafo
    if grafo.existe_arista(origen, destino):
        print(f"  ✗ La conexión {origen} - {destino} ya existe.")
        return grafo
    peso = pedir_peso("  Peso (km): ")

    try:
        guardar_arista(RUTA_CSV, origen, destino, peso)
    except PermissionError:
        print(f"  ✗ No hay permiso para escribir en {RUTA_CSV.name}.")
        return grafo
    print(f"  ✓ Conexión {origen} - {destino} ({peso:g}) "
          f"guardada en {RUTA_CSV.name}.")
    return cargar_red()


def mostrar_red(grafo: Grafo) -> None:
    """Imprime los nodos y las conexiones del grafo."""
    if not grafo.nodos:
        print("  La red está vacía. Ingresa conexiones con la opción 1.")
        return
    print(f"\nNodos ({len(grafo.nodos)}): {', '.join(grafo.nombres())}")
    print("Conexiones:")
    for origen, destino, peso in grafo.aristas():
        print(f"  {origen:<10} <-> {destino:<10} {peso:>6g}")


def calcular_ruta(grafo: Grafo) -> None:
    """Pide inicio y destino, ejecuta Dijkstra y muestra el resultado."""
    if len(grafo.nodos) < 2:
        print("  Se necesitan al menos dos nodos para calcular una ruta.")
        return
    print(f"\nNodos disponibles: {', '.join(grafo.nombres())}")
    inicio = pedir_nodo("  Nodo de inicio: ")
    destino = pedir_nodo("  Nodo de destino: ")
    try:
        peso_total, camino = grafo.dijkstra(inicio, destino)
    except KeyError as error:
        print(f"  ✗ El nodo {error} no existe en la red.")
        return
    except ValueError as error:
        print(f"  ✗ {error}.")
        return

    print(f"\n  Ruta más corta: {' -> '.join(camino)}")
    print(f"  Peso total: {peso_total:.2f}")
    try:
        guardar_ruta_json(RUTA_JSON, inicio, destino, peso_total, camino)
    except PermissionError:
        print(f"  ⚠ No se pudo guardar el historial en {RUTA_JSON.name}.")


def cargar_red() -> Grafo:
    """Carga nodos.csv, muestra los avisos y regresa el grafo en memoria."""
    grafo, avisos = cargar_grafo(RUTA_CSV)
    for aviso in avisos:
        print(f"  ⚠ {aviso}")
    print(f"  ✓ Grafo cargado: {len(grafo.nodos)} nodos, "
          f"{len(grafo.aristas())} conexiones.")
    return grafo


def main() -> None:
    """Ciclo principal del menú."""
    print("Cargando la red de transporte desde nodos.csv...")
    grafo = cargar_red()
    while True:
        print(MENU)
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            grafo = ingresar_conexion(grafo)
        elif opcion == "2":
            mostrar_red(grafo)
        elif opcion == "3":
            calcular_ruta(grafo)
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("  ✗ Opción no válida. Elige 1, 2, 3 o 4.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido. "
              "Las conexiones guardadas se conservan.")
