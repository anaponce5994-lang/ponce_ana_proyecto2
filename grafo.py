"""Clases POO de la red de transporte: Nodo, Grafo y el algoritmo de Dijkstra.

El algoritmo de Dijkstra es el desarrollado en la Unidad 1 (Proyecto 1),
ahora como método de la clase Grafo y con anotaciones de tipo.
"""

import math

INFINITO: float = math.inf


class Nodo:
    """Representa un punto de la red (una universidad) y sus vecinos."""

    def __init__(self, nombre: str) -> None:
        """Crea un nodo sin vecinos."""
        self.nombre: str = nombre
        self.vecinos: dict[str, float] = {}

    def agregar_vecino(self, vecino: str, peso: float) -> None:
        """Agrega o actualiza un vecino con el peso de la conexión."""
        self.vecinos[vecino] = peso

    def __repr__(self) -> str:
        """Texto para mostrar el nodo al depurar."""
        return f"Nodo({self.nombre!r}, vecinos={self.vecinos})"


class Grafo:
    """Grafo no dirigido y ponderado: cada arista es de ida y vuelta."""

    def __init__(self) -> None:
        """Crea un grafo vacío; self.nodos guarda {nombre: Nodo}."""
        self.nodos: dict[str, Nodo] = {}

    def obtener_nodo(self, nombre: str) -> Nodo:
        """Regresa el nodo con ese nombre; si no existe, lo crea."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)
        return self.nodos[nombre]

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        """Agrega una arista en ambos sentidos.

        Lanza ValueError si un nodo está vacío, si el origen y el destino
        son iguales o si el peso no es un número positivo.
        """
        if not origen or not destino:
            raise ValueError("el nombre del nodo no puede estar vacío")
        if origen == destino:
            raise ValueError("un nodo no puede conectarse consigo mismo")
        if not math.isfinite(peso) or peso <= 0:
            raise ValueError("el peso debe ser un número mayor que cero")
        self.obtener_nodo(origen).agregar_vecino(destino, peso)
        self.obtener_nodo(destino).agregar_vecino(origen, peso)

    def existe_arista(self, origen: str, destino: str) -> bool:
        """Indica si ya hay una conexión directa entre dos nodos."""
        return origen in self.nodos and destino in self.nodos[origen].vecinos

    def nombres(self) -> list[str]:
        """Lista ordenada con los nombres de todos los nodos."""
        return sorted(self.nodos)

    def aristas(self) -> list[tuple[str, str, float]]:
        """Lista de aristas sin repetir el sentido inverso."""
        resultado: list[tuple[str, str, float]] = []
        for nombre in self.nombres():
            for vecino, peso in sorted(self.nodos[nombre].vecinos.items()):
                if nombre < vecino:
                    resultado.append((nombre, vecino, peso))
        return resultado

    def dijkstra(self, inicio: str, destino: str) -> tuple[float, list[str]]:
        """Calcula la ruta más corta entre dos nodos (Unidad 1).

        En cada vuelta elige el nodo no visitado con la menor distancia y
        actualiza la distancia de sus vecinos. Regresa (peso_total, camino).
        Lanza KeyError si algún nodo no existe y ValueError si no hay ruta.
        """
        for nombre in (inicio, destino):
            if nombre not in self.nodos:
                raise KeyError(nombre)

        distancias: dict[str, float] = {}
        anteriores: dict[str, str | None] = {}
        visitados: set[str] = set()

        for nombre in self.nodos:
            distancias[nombre] = INFINITO
            anteriores[nombre] = None

        distancias[inicio] = 0.0

        while len(visitados) < len(self.nodos):
            # Buscar el nodo más cercano que no se haya visitado
            nodo_actual: str | None = None
            menor_distancia = INFINITO
            for nombre in self.nodos:
                if nombre in visitados:
                    continue
                if distancias[nombre] < menor_distancia:
                    menor_distancia = distancias[nombre]
                    nodo_actual = nombre

            # Los nodos que faltan no se pueden alcanzar
            if nodo_actual is None:
                break

            # Si llegamos al destino, terminamos
            if nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            # Revisar vecinos
            for vecino, peso in self.nodos[nodo_actual].vecinos.items():
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

        if distancias[destino] == INFINITO:
            raise ValueError(f"no hay ruta entre {inicio} y {destino}")

        # Construir el camino desde el destino hacia el inicio
        camino: list[str] = []
        actual: str | None = destino
        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]
        camino.reverse()
        return distancias[destino], camino
