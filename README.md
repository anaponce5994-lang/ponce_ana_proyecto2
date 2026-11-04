# Proyecto 2: Persistencia, Archivos y Excepciones

**Programación III · Unidad 2**
Ponce Santero Ana Patricia — 214459944

Programa modular en Python para ingresar conexiones de una red de transporte
entre universidades de Guadalajara (CUGDL, UNIVA, UAG, UNE, UNIVER, UTEG),
guardarlas en `nodos.csv`, construir el grafo en memoria y calcular la ruta más
corta con el algoritmo de Dijkstra de la Unidad 1.

## Estructura

```
ponce_ana_proyecto2/
├── nodos.csv          # Conexiones de la red (Origen,Destino,Peso)
├── main.py            # Script principal interactivo (menú)
├── grafo.py           # Clases POO: Nodo, Grafo y método dijkstra
├── io_handler.py      # Lectura/escritura del CSV y del historial JSON
├── requirements.txt   # Dependencia: flake8
└── README.md
```

Al calcular una ruta se crea `historial_rutas.json` con los resultados.

## Cómo ejecutarlo

Requiere Python 3.10 o superior.

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Menú:

1. **Ingresar nueva conexión:** pide nodo origen, nodo destino y peso. Se
   guarda en `nodos.csv` en modo append (`'a'`).
2. **Ver nodos y conexiones.**
3. **Calcular ruta más corta:** ejecuta Dijkstra y muestra la ruta y el peso
   total.
4. **Salir.**

## Manejo de errores

| Situación | Qué hace el programa |
| --- | --- |
| Peso con texto (`cinco`), negativo o vacío | Muestra el error y vuelve a pedir el peso |
| `nodos.csv` no existe (`FileNotFoundError`) | Inicia con la red vacía y crea el archivo al guardar |
| Faltan encabezados (`KeyError`) | Avisa cuáles deben ser y no se detiene |
| Fila con datos corruptos (`ValueError`) | Omite esa fila, avisa el número de fila y sigue |
| Nodo que no existe al calcular la ruta (`KeyError`) | Avisa y regresa al menú |
| No hay camino entre los nodos (`ValueError`) | Avisa y regresa al menú |

No se usa `except:` a secas ni `except Exception:`; todas las lecturas y
escrituras usan `with open(...)`.

## Revisión con Flake8

```bash
python3 -m flake8 .
```

Si no muestra nada, el código no tiene errores de estilo.
