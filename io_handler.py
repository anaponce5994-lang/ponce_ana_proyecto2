"""Funciones de lectura y escritura de archivos (CSV y JSON)."""

import csv
import json
from datetime import datetime
from pathlib import Path

from grafo import Grafo

ENCABEZADOS: list[str] = ["Origen", "Destino", "Peso"]
CODIFICACION: str = "utf-8"


def normalizar_nodo(nombre: str) -> str:
    """Quita espacios sobrantes y pasa el nombre a mayúsculas."""
    return " ".join(nombre.split()).upper()


def convertir_peso(texto: str) -> float:
    """Convierte el texto a float; lanza ValueError con mensaje en español."""
    texto = texto.strip().replace(",", ".")
    if not texto:
        raise ValueError("el peso no puede quedar vacío")
    try:
        return float(texto)
    except ValueError:
        raise ValueError(f"'{texto}' no es un número válido") from None


def guardar_arista(ruta: Path, origen: str, destino: str, peso: float) -> None:
    """Agrega una arista al final del CSV (modo append 'a').

    Si el archivo no existe o está vacío, primero escribe los encabezados.
    """
    escribir_encabezados = not ruta.exists() or ruta.stat().st_size == 0
    with open(ruta, "a", newline="", encoding=CODIFICACION) as archivo:
        escritor = csv.writer(archivo)
        if escribir_encabezados:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([origen, destino, peso])


def cargar_grafo(ruta: Path) -> tuple[Grafo, list[str]]:
    """Lee el CSV fila por fila e instancia el grafo en memoria.

    Regresa el grafo y una lista de avisos. Las filas con datos corruptos
    se omiten sin detener el programa.
    """
    grafo = Grafo()
    avisos: list[str] = []
    try:
        with open(ruta, "r", newline="", encoding=CODIFICACION) as archivo:
            lector = csv.DictReader(archivo)
            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    origen = normalizar_nodo(fila["Origen"] or "")
                    destino = normalizar_nodo(fila["Destino"] or "")
                    peso = convertir_peso(fila["Peso"] or "")
                    grafo.agregar_arista(origen, destino, peso)
                except KeyError as error:
                    avisos.append(
                        f"Falta el encabezado {error} en {ruta.name}. "
                        f"Los encabezados deben ser: {','.join(ENCABEZADOS)}"
                    )
                    break
                except ValueError as error:
                    avisos.append(
                        f"Fila {numero_fila} omitida: {error}")
    except FileNotFoundError:
        avisos.append(
            f"No se encontró {ruta.name}; "
            "se creará al guardar la primera conexión."
        )
    except UnicodeDecodeError:
        avisos.append(
            f"{ruta.name} no está guardado en UTF-8 y no se pudo leer.")
    return grafo, avisos


def guardar_ruta_json(ruta: Path, inicio: str, destino: str,
                      peso_total: float, camino: list[str]) -> None:
    """Agrega el resultado de Dijkstra al historial en formato JSON."""
    historial: list[dict[str, object]] = []
    try:
        with open(ruta, "r", encoding=CODIFICACION) as archivo:
            datos = json.load(archivo)
        if isinstance(datos, list):
            historial = datos
    except FileNotFoundError:
        pass  # Primera consulta: el historial empieza vacío
    except json.JSONDecodeError:
        pass  # Historial dañado: se reemplaza por uno nuevo

    historial.append({
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "inicio": inicio,
        "destino": destino,
        "camino": camino,
        "peso_total": round(peso_total, 2),
    })
    with open(ruta, "w", encoding=CODIFICACION) as archivo:
        json.dump(historial, archivo, ensure_ascii=False, indent=2)
