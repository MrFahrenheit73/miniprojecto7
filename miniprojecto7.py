# ==============================================================================
# DICCIONARIO INTELIGENTE CON ÁRBOL BINARIO DE BÚSQUEDA (BST)
# Implementación en Python orientada a objetos conforme a PEP 8
# ==============================================================================

import os
from typing import List, Optional


class Palabra:
    """Representa una entrada léxica en el diccionario.

    Encapsula el término en minúsculas y su definición descriptiva,
    proporcionando sobrecarga de operadores para comparación alfabética.
    """

    def __init__(self, termino: str, definicion: str):
        self.termino: str = termino.strip().lower()
        self.definicion: str = definicion.strip()

    def __lt__(self, other: "Palabra") -> bool:
        return self.termino < other.termino

    def __gt__(self, other: "Palabra") -> bool:
        return self.termino > other.termino

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Palabra):
            return self.termino == other.termino
        if isinstance(other, str):
            return self.termino == other.strip().lower()
        return False

    def __str__(self) -> str:
        return f"{self.termino.capitalize()}: {self.definicion}"


class NodoBST:
    """Nodo individual de un árbol binario de búsqueda.

    Almacena una instancia del objeto Palabra y referencias a sus hijos.
    """

    def __init__(self, palabra: Palabra):
        self.palabra: Palabra = palabra
        self.izquierdo: Optional["NodoBST"] = None
        self.derecho: Optional["NodoBST"] = None


class DiccionarioBST:
    """Estructura de datos Árbol Binario de Búsqueda adaptada para objetos Palabra.

    Permite indexación alfabética, búsqueda exacta O(log n), autocompletado
    por prefijo con poda de subárboles y balanceo automático.
    """

    def __init__(self):
        self.raiz: Optional[NodoBST] = None
        self._total_palabras: int = 0

    @property
    def total_palabras(self) -> int:
        """Retorna la cantidad total de términos almacenados en el diccionario."""
        return self._total_palabras

    # --------------------------------------------------------------------------
    # 1. Inserción de palabras
    # --------------------------------------------------------------------------
    def insertar(self, termino: str, definicion: str) -> bool:
        """Inserta una nueva palabra en el diccionario respetando el orden alfabético.

        Si el término ya existe, actualiza su definición y retorna False.
        """
        termino_limpio = termino.strip().lower()
        if not termino_limpio:
            return False

        nueva_palabra = Palabra(termino_limpio, definicion)
        if self.raiz is None:
            self.raiz = NodoBST(nueva_palabra)
            self._total_palabras += 1
            return True

        fue_insertada = self._insertar_rec(self.raiz, nueva_palabra)
        if fue_insertada:
            self._total_palabras += 1
        return fue_insertada

    def _insertar_rec(self, nodo: NodoBST, nueva_palabra: Palabra) -> bool:
        if nueva_palabra < nodo.palabra:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(nueva_palabra)
                return True
            return self._insertar_rec(nodo.izquierdo, nueva_palabra)
        elif nueva_palabra > nodo.palabra:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(nueva_palabra)
                return True
            return self._insertar_rec(nodo.derecho, nueva_palabra)
        else:
            # Si el término coincide, se actualiza la definición
            nodo.palabra.definicion = nueva_palabra.definicion
            return False

    # --------------------------------------------------------------------------
    # 2. Búsqueda exacta O(h)
    # --------------------------------------------------------------------------
    def buscar_exacta(self, termino: str) -> Optional[Palabra]:
        """Busca una palabra exacta en el diccionario.

        Retorna el objeto Palabra si existe, o None si no se encuentra.
        """
        termino_norm = termino.strip().lower()
        if not termino_norm:
            return None
        return self._buscar_exacta_rec(self.raiz, termino_norm)

    def _buscar_exacta_rec(
        self, nodo: Optional[NodoBST], termino: str
    ) -> Optional[Palabra]:
        if nodo is None:
            return None

        if termino == nodo.palabra.termino:
            return nodo.palabra
        elif termino < nodo.palabra.termino:
            return self._buscar_exacta_rec(nodo.izquierdo, termino)
        else:
            return self._buscar_exacta_rec(nodo.derecho, termino)

    # --------------------------------------------------------------------------
    # 3. Autocompletado / Búsqueda por prefijo optimizada
    # --------------------------------------------------------------------------
    def buscar_por_prefijo(self, prefijo: str) -> List[Palabra]:
        """Retorna todas las palabras que comiencen con el prefijo especificado.

        Aplica poda de subárboles para no visitar ramas irrelevantes y
        devuelve los resultados ordenados alfabéticamente.
        """
        pref = prefijo.strip().lower()
        if not pref:
            return []

        resultados: List[Palabra] = []
        self._buscar_prefijo_rec(self.raiz, pref, resultados)
        return resultados

    def _buscar_prefijo_rec(
        self, nodo: Optional[NodoBST], pref: str, resultados: List[Palabra]
    ) -> None:
        if nodo is None:
            return

        termino_actual = nodo.palabra.termino

        # Caso 1: El término actual inicia con el prefijo
        if termino_actual.startswith(pref):
            # Recorrido inorden para garantizar orden alfabético
            self._buscar_prefijo_rec(nodo.izquierdo, pref, resultados)
            resultados.append(nodo.palabra)
            self._buscar_prefijo_rec(nodo.derecho, pref, resultados)

        # Caso 2: El término es alfabéticamente mayor que el prefijo y no empieza con él.
        # Las palabras con este prefijo solo pueden ubicarse en el subárbol izquierdo.
        elif termino_actual > pref:
            self._buscar_prefijo_rec(nodo.izquierdo, pref, resultados)

        # Caso 3: El término es alfabéticamente menor que el prefijo y no empieza con él.
        # Las palabras con este prefijo solo pueden ubicarse en el subárbol derecho.
        else:
            self._buscar_prefijo_rec(nodo.derecho, pref, resultados)

    # --------------------------------------------------------------------------
    # 4. Listado completo en orden alfabético (Recorrido Inorden)
    # --------------------------------------------------------------------------
    def listar_en_orden(self) -> List[Palabra]:
        """Retorna la lista de todas las palabras ordenadas alfabéticamente."""
        palabras: List[Palabra] = []
        self._inorden_rec(self.raiz, palabras)
        return palabras

    def _inorden_rec(self, nodo: Optional[NodoBST], lista: List[Palabra]) -> None:
        if nodo is not None:
            self._inorden_rec(nodo.izquierdo, lista)
            lista.append(nodo.palabra)
            self._inorden_rec(nodo.derecho, lista)

    # --------------------------------------------------------------------------
    # 5. Balanceo a altura mínima O(n)
    # --------------------------------------------------------------------------
    def balancear(self) -> None:
        """Reestructura el árbol in-place para lograr altura mínima garantizada."""
        elementos = self.listar_en_orden()
        self.raiz = self._construir_balanceado(elementos, 0, len(elementos) - 1)

    def _construir_balanceado(
        self, elementos: List[Palabra], inicio: int, fin: int
    ) -> Optional[NodoBST]:
        if inicio > fin:
            return None
        medio = (inicio + fin) // 2
        nodo = NodoBST(elementos[medio])
        nodo.izquierdo = self._construir_balanceado(elementos, inicio, medio - 1)
        nodo.derecho = self._construir_balanceado(elementos, medio + 1, fin)
        return nodo

    # --------------------------------------------------------------------------
    # 6. Estadísticas y Métricas del Árbol
    # --------------------------------------------------------------------------
    def calcular_altura(self) -> int:
        """Calcula la altura máxima del árbol (distancia de la raíz a la hoja más lejana)."""

        def _altura_rec(nodo: Optional[NodoBST]) -> int:
            if nodo is None:
                return -1
            return 1 + max(_altura_rec(nodo.izquierdo), _altura_rec(nodo.derecho))

        return _altura_rec(self.raiz)


# ==============================================================================
# BANCO DE DATOS INICIAL (60 TÉRMINOS INFORMÁTICOS Y CIENTÍFICOS)
# ==============================================================================

PALABRAS_INICIALES = [
    (
        "algoritmo",
        "Secuencia finita y no ambigua de pasos computables para resolver un"
        " problema.",
    ),
    (
        "almacenamiento",
        "Dispositivo o medio físico o virtual destinado a conservar datos e"
        " información.",
    ),
    (
        "amortizado",
        "Análisis del costo temporal promedio de una operación a lo largo de"
        " una secuencia.",
    ),
    (
        "ancho",
        "Dimensión transversal o número de nodos en el nivel más poblado de un"
        " árbol.",
    ),
    (
        "apilamiento",
        "Operación de inserción de un elemento en una estructura de pila.",
    ),
    (
        "arbol",
        "Estructura de datos jerárquica y no lineal compuesta de nodos"
        " enlazados.",
    ),
    (
        "arquitectura",
        "Diseño conceptual y estructura operacional fundamental de un sistema"
        " informático.",
    ),
    (
        "arreglo",
        "Colección contigua y homogénea de elementos accesibles mediante un"
        " índice.",
    ),
    (
        "asignacion",
        "Asociación o almacenamiento de un valor concreto en una variable.",
    ),
    (
        "autenticacion",
        "Verificación rigurosa de la identidad de un usuario, dispositivo o"
        " entidad.",
    ),
    (
        "automata",
        "Modelo matemático de un sistema que transita entre estados ante"
        " entradas.",
    ),
    (
        "autonomia",
        "Capacidad de un sistema o agente para operar sin intervención externa"
        " directa.",
    ),
    (
        "auto",
        "Vehículo automotor de transporte o prefijo que denota acción por sí"
        " mismo.",
    ),
    (
        "aurora",
        "Luz tenue o fenómeno luminoso que precede inmediatamente a la salida"
        " del sol.",
    ),
    (
        "balanceo",
        "Reorganización de un árbol de búsqueda para garantizar altura mínima"
        " logarítmica.",
    ),
    (
        "binario",
        "Sistema numérico o estructura lógica donde cada elemento tiene como"
        " máximo dos opciones.",
    ),
    (
        "bit",
        "Dígito binario elemental que representa la unidad atómica de"
        " información (0 o 1).",
    ),
    (
        "bloque",
        "Conjunto de instrucciones agrupadas y delimitadas sintácticamente.",
    ),
    (
        "booleano",
        "Tipo de dato primitivo que únicamente admite los valores verdadero o"
        " falso.",
    ),
    (
        "bucle",
        "Estructura de control iterativa que repite código mientras se cumpla"
        " una condición.",
    ),
    (
        "busqueda",
        "Algoritmo para determinar la existencia y ubicación de un dato en una"
        " colección.",
    ),
    (
        "byte",
        "Unidad básica de memoria direccionable compuesta por ocho bits.",
    ),
    (
        "cache",
        "Memoria de acceso ultrarrápido que almacena datos de lectura"
        " recurrente.",
    ),
    (
        "cadena",
        "Secuencia contigua e inmutable de caracteres alfanuméricos.",
    ),
    (
        "clase",
        "Plantilla en OOP que encapsula atributos y comportamientos de un tipo"
        " de objeto.",
    ),
    (
        "clave",
        "Identificador unívoco empleado para indexar o mapear un registro de"
        " información.",
    ),
    (
        "cliente",
        "Software o dispositivo que formula solicitudes de servicio a un"
        " servidor.",
    ),
    (
        "cola",
        "Estructura de datos lineal regida por el protocolo FIFO (primero en"
        " entrar, primero en salir).",
    ),
    (
        "compilador",
        "Traductor de software que convierte código fuente en lenguaje"
        " ejecutable de máquina.",
    ),
    (
        "concurrencia",
        "Capacidad de un entorno operativo para coordinar múltiples flujos de"
        " ejecución.",
    ),
    (
        "constante",
        "Identificador cuyo valor asignado permanece inalterable durante toda"
        " la ejecución.",
    ),
    (
        "constructor",
        "Subrutina especial de una clase encargada de inicializar nuevas"
        " instancias.",
    ),
    (
        "cursor",
        "Puntero indicador de la posición actual de lectura en un flujo o base"
        " de datos.",
    ),
    (
        "depuracion",
        "Metodología sistemática para encontrar y remediar fallas en el"
        " software.",
    ),
    (
        "diccionario",
        "Colección asociativa compuesta de pares de clave y valor.",
    ),
    (
        "direccion",
        "Identificador numérico de una celda específica en la memoria"
        " principal.",
    ),
    (
        "encapsulamiento",
        "Principio de diseño que oculta el estado interno y detalles de una"
        " clase.",
    ),
    (
        "encriptacion",
        "Cifrado criptográfico de información legible para volverla"
        " ininteligible.",
    ),
    (
        "enlace",
        "Apuntador que relaciona un nodo de una estructura con otro contiguo.",
    ),
    (
        "escaner",
        "Analizador que convierte un flujo de caracteres en una serie de fichas"
        " léxicas.",
    ),
    (
        "excepcion",
        "Condición anómala generada durante la ejecución que altera el flujo del"
        " programa.",
    ),
    (
        "funcion",
        "Bloque reutilizable de código parametrizado que ejecuta una tarea"
        " concreta.",
    ),
    (
        "grafo",
        "Conjunto no jerárquico de vértices interconectados mediante aristas.",
    ),
    (
        "hash",
        "Función algorítmica que proyecta datos arbitrarios en valores numéricos"
        " de tamaño fijo.",
    ),
    (
        "herencia",
        "Mecanismo OOP para derivar propiedades de una clase madre a clases"
        " hijas.",
    ),
    (
        "hilera",
        "Secuencia ordenada o hilo ligero de ejecución dentro de un proceso"
        " concurrente.",
    ),
    ("hoja", "Nodo terminal de un árbol que no posee descendientes."),
    (
        "indice",
        "Estructura auxiliar que acelera drásticamente la búsqueda de"
        " registros.",
    ),
    (
        "inorden",
        "Recorrido DFS que procesa el subárbol izquierdo, la raíz y el subárbol"
        " derecho.",
    ),
    (
        "insercion",
        "Acción de añadir un elemento nuevo en una estructura de datos.",
    ),
    (
        "instancia",
        "Manifestación física y viva en memoria de la estructura definida por"
        " una clase.",
    ),
    (
        "interfaz",
        "Contrato que define los métodos públicos que una clase concreta debe"
        " implementar.",
    ),
    (
        "iterador",
        "Objeto que facilita la navegación secuencial a través de los elementos"
        " de una colección.",
    ),
    (
        "memoria",
        "Subsistema del computador destinado a retener instrucciones y datos"
        " procesables.",
    ),
    (
        "metodo",
        "Función subordinada a una clase que opera sobre el estado de sus"
        " objetos.",
    ),
    (
        "nodo",
        "Elemento básico de una estructura enlazada que contiene datos y"
        " punteros.",
    ),
    (
        "objeto",
        "Entidad de software en OOP dotada de identidad, estado y"
        " comportamiento.",
    ),
    (
        "pila",
        "Estructura de datos lineal gobernada por la convención LIFO (último en"
        " entrar, primero en salir).",
    ),
    (
        "raiz",
        "Nodo primigenio y superior de un árbol jerárquico del cual descienden"
        " todos los demás.",
    ),
    (
        "recursividad",
        "Técnica de diseño algorítmico donde un método se autoinvoca con datos"
        " reducidos.",
    ),
]


def cargar_diccionario_inicial(
    ruta_archivo: str = "palabras_diccionario.txt",
) -> DiccionarioBST:
    """Carga los datos iniciales al árbol BST.

    Si existe el archivo de texto, lo lee línea por línea (formato:
    termino|definicion). En caso contrario, crea el archivo con la lista
    predeterminada y carga las 60 palabras, balanceando el árbol al final para
    asegurar O(log n).
    """
    diccionario = DiccionarioBST()

    # Creación automática del archivo si no existe
    if not os.path.exists(ruta_archivo):
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            for term, defin in PALABRAS_INICIALES:
                f.write(f"{term}|{defin}\n")

    # Lectura del archivo de texto
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if "|" in linea:
                partes = linea.split("|", 1)
                diccionario.insertar(partes[0], partes[1])

    # Balanceo para optimizar operaciones a O(log n)
    diccionario.balancear()
    return diccionario


# ==============================================================================
# INTERFAZ DE USUARIO POR CONSOLA (CLI INTERACTIVA)
# ==============================================================================


def mostrar_encabezado():
    print("\n" + "=" * 65)
    print("        SISTEMA DE DICCIONARIO INTELIGENTE CON BST")
    print("=" * 65)


def mostrar_menu():
    print("\n[ MENÚ DE OPCIONES ]")
    print("1. Buscar definición exacta")
    print("2. Autocompletar / Buscar por prefijo")
    print("3. Ver diccionario completo en orden alfabético")
    print("4. Agregar una nueva palabra")
    print("5. Ver estadísticas del árbol (altura y términos)")
    print("6. Salir")
    print("-" * 65)


def ejecutar_interfaz(diccionario: DiccionarioBST):
    """Bucle principal de interacción con el usuario en terminal."""
    mostrar_encabezado()
    print("-> Diccionario cargado y balanceado con éxito.")
    print(f"-> Total de términos activos: {diccionario.total_palabras}")
    print(f"-> Altura logarítmica del árbol: {diccionario.calcular_altura()}")

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- BÚSQUEDA EXACTA ---")
            termino = input("Ingresa la palabra a buscar: ").strip()
            if not termino:
                print("[!] Debes ingresar un término válido.")
                continue

            resultado = diccionario.buscar_exacta(termino)
            if resultado:
                print(f"\n[+] Término encontrado:")
                print(
                    f"    • {resultado.termino.upper()}: {resultado.definicion}"
                )
            else:
                print(
                    f"\n[-] La palabra '{termino}' no se encuentra en el"
                    " diccionario."
                )
                if len(termino) >= 2:
                    sugerencias = diccionario.buscar_por_prefijo(termino[:2])
                    if sugerencias:
                        print("    Quizás quisiste decir:")
                        for s in sugerencias[:4]:
                            print(f"    * {s.termino}")

        elif opcion == "2":
            print("\n--- AUTOCOMPLETADO POR PREFIJO ---")
            prefijo = input(
                "Ingresa el prefijo (ej. 'au', 'al', 'bi', 'co'): "
            ).strip()
            if not prefijo:
                print("[!] El prefijo no puede estar vacío.")
                continue

            coincidencias = diccionario.buscar_por_prefijo(prefijo)
            if coincidencias:
                print(
                    f"\n[+] Se encontraron {len(coincidencias)} coincidencias"
                    f" para '{prefijo}':"
                )
                for idx, pal in enumerate(coincidencias, start=1):
                    print(
                        f"    {idx:2d}. {pal.termino.capitalize():15s} ->"
                        f" {pal.definicion}"
                    )
            else:
                print(
                    "\n[-] No se registraron palabras que comiencen con"
                    f" '{prefijo}'."
                )

        elif opcion == "3":
            print("\n--- DICCIONARIO COMPLETO (ORDEN ALFABÉTICO) ---")
            palabras = diccionario.listar_en_orden()
            print(f"Total de registros: {len(palabras)}\n")
            for idx, pal in enumerate(palabras, start=1):
                print(
                    f"{idx:2d}. {pal.termino.capitalize():16s} :"
                    f" {pal.definicion}"
                )

        elif opcion == "4":
            print("\n--- AGREGAR O ACTUALIZAR PALABRA ---")
            nuevo_term = input("Palabra: ").strip()
            nueva_def = input("Definición: ").strip()
            if nuevo_term and nueva_def:
                insertada = diccionario.insertar(nuevo_term, nueva_def)
                if insertada:
                    print(f"[+] Palabra '{nuevo_term}' agregada exitosamente.")
                else:
                    print(f"[*] Definición de '{nuevo_term}' actualizada.")
            else:
                print("[!] Ninguno de los campos puede quedar vacío.")

        elif opcion == "5":
            print("\n--- ESTADÍSTICAS DEL BST ---")
            n = diccionario.total_palabras
            h = diccionario.calcular_altura()
            print(f"• Total de nodos (palabras): {n}")
            print(f"• Altura actual del árbol:   {h}")
            print(
                f"• Eficiencia teórica:       O(log2({n})) ≈ {h} niveles de"
                " búsqueda."
            )

        elif opcion == "6":
            print(
                "\n¡Gracias por utilizar el Diccionario Inteligente! Hasta"
                " pronto.\n"
            )
            break

        else:
            print(
                "[!] Opción inválida. Por favor, selecciona un número entre 1 y"
                " 6."
            )


if __name__ == "__main__":
    dicc = cargar_diccionario_inicial()
    ejecutar_interfaz(dicc)