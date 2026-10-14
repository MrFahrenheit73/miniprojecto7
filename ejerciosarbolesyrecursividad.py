
"""
Unidad 9: Árboles - Árbol Binario de Búsqueda (BST)
Implementación profesional con tipado estático y resolución de la Tarea 6.
"""
from collections import deque
from typing import Optional, List, Any

class NodoArbol:
    """Clase que representa un nodo en un árbol binario."""
    def __init__(self, valor: Any):
        self.valor = valor
        self.izquierdo: Optional['NodoArbol'] = None
        self.derecho: Optional['NodoArbol'] = None


class ArbolBinarioBusqueda:
    """Clase que representa un Árbol Binario de Búsqueda (BST)."""
    
    def __init__(self):
        self.raiz: Optional[NodoArbol] = None

    # ==========================================
    # OPERACIONES BÁSICAS (Sección 3)
    # ==========================================
    def insertar(self, valor: Any) -> None:
        """Inserta un nuevo valor en el árbol de forma ordenada."""
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual: NodoArbol, valor: Any) -> None:
        if valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecho, valor)
        # Si el valor es igual, se ignora (no se permiten duplicados en este BST)

    def buscar(self, valor: Any) -> bool:
        """Busca un valor en el árbol. Retorna True si existe, False si no."""
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual: Optional[NodoArbol], valor: Any) -> bool:
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor:
            return True
        if valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierdo, valor)
        return self._buscar_recursivo(nodo_actual.derecho, valor)

    # ==========================================
    # RECORRIDOS (Sección 3)
    # ==========================================
    def inorden(self) -> List[Any]:
        """Recorrido Inorden: Izquierda -> Raíz -> Derecha."""
        resultado: List[Any] = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo: Optional[NodoArbol], resultado: List[Any]) -> None:
        if nodo is not None:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_rec(nodo.derecho, resultado)

    # ==========================================
    # RESOLUCIÓN DE LA TAREA (Sección 6)
    # ==========================================
    
    # =======================================================
    # 1. ELIMINACIÓN (3 CASOS: HOJA, 1 HIJO, 2 HIJOS)
    # =======================================================
    def eliminar(self, valor: Any) -> None:
        """Elimina un nodo del árbol manteniendo la propiedad del BST."""
        self.raiz = self._eliminar_rec(self.raiz, valor)

    def _eliminar_rec(self, nodo: Optional[NodoArbol], valor: Any) -> Optional[NodoArbol]:
        if nodo is None:
            return None
            
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_rec(nodo.derecho, valor)
        else:
            # Nodo encontrado
            # Caso 1 y 2: El nodo tiene un hijo o es hoja
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
                
            # Caso 3: El nodo tiene dos hijos
            # Encontramos el sucesor inorden (el mínimo del lado derecho)
            sucesor = self._min_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.valor)
            
        return nodo

    def _min_nodo(self, nodo: NodoArbol) -> NodoArbol:
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    # =======================================================
    # 2. RECORRIDOS BFS (EN ANCHURA / NIVELES CON COLA)
    # =======================================================
    def por_niveles(self) -> List[Any]:
        """Recorrido en Anchura (BFS). Visita nivel por nivel usando una Cola."""
        if self.raiz is None:
            return []
            
        resultado = []
        cola = deque([self.raiz])
        
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            
            if nodo.izquierdo is not None:
                cola.append(nodo.izquierdo)
            if nodo.derecho is not None:
                cola.append(nodo.derecho)
                
        return resultado
    # =======================================================
    # 3. SUMA DE ELEMENTOS (RECURSIVA INMUTABLE)
    # =======================================================
    def suma_elementos(self) -> int:
        """Suma de todos los elementos sin modificar el árbol."""
        return self._suma_rec(self.raiz)

    def _suma_rec(self, nodo: Optional[NodoArbol]) -> int:
        if nodo is None:
            return 0
        return nodo.valor + self._suma_rec(nodo.izquierdo) + self._suma_rec(nodo.derecho)
    # =======================================================
    # 4. VALIDACIÓN DE COMPLETITUD (0 O 2 HIJOS POR NODO)
    # =======================================================
    def es_completo(self) -> bool:
        """Verifica si todos los nodos internos tienen exactamente dos hijos."""
        return self._es_completo_rec(self.raiz)

    def _es_completo_rec(self, nodo: Optional[NodoArbol]) -> bool:
        # Un árbol vacío o una hoja (0 hijos) se consideran completos
        if nodo is None:
            return True
        if nodo.izquierdo is None and nodo.derecho is None:
            return True
            
        # Si tiene ambos hijos, verificamos hacia abajo
        if nodo.izquierdo is not None and nodo.derecho is not None:
            return self._es_completo_rec(nodo.izquierdo) and self._es_completo_rec(nodo.derecho)
            
        # Si tiene un solo hijo, no es completo
        return False

    # ==========================================
    # UTILIDADES DE VISUALIZACIÓN
    # ==========================================
    def mostrar_arbol(self) -> None:
        """Muestra el árbol rotado 90 grados en consola."""
        self._imprimir_nodo(self.raiz, "", True)

    def _imprimir_nodo(self, nodo: Optional[NodoArbol], prefijo: str, es_izquierdo: bool) -> None:
        if nodo is not None:
            self._imprimir_nodo(nodo.derecho, prefijo + ("|   " if es_izquierdo else "    "), False)
            print(prefijo + ("\\-- " if es_izquierdo else "/-- ") + str(nodo.valor))
            self._imprimir_nodo(nodo.izquierdo, prefijo + ("    " if es_izquierdo else "|   "), True)

    # =======================================================
    # 5. BALANCEO A ALTURA MÍNIMA (DIVISIÓN Y CONQUISTA)
    # =======================================================
def construir_arbol_balanceado(valores: List[Any]) -> Optional[NodoArbol]:
    """Construye un BST balanceado de altura mínima a partir de una lista ordenada."""
    if not valores:
        return None
        
    medio = len(valores) // 2
    nodo = NodoArbol(valores[medio])
    nodo.izquierdo = construir_arbol_balanceado(valores[:medio])
    nodo.derecho = construir_arbol_balanceado(valores[medio + 1:])
    return nodo

def balancear_arbol(bst_original: ArbolBinarioBusqueda) -> ArbolBinarioBusqueda:
    """
    Toma un BST (posiblemente degenerado), extrae sus elementos
    y retorna un NUEVO BST balanceado de altura mínima.
    """
    # En un BST el recorrido inorden devuelve los elementos ordenados automáticamente
    valores_ordenados = bst_original.inorden() 
    
    nuevo_bst = ArbolBinarioBusqueda()
    nuevo_bst.raiz = construir_arbol_balanceado(valores_ordenados)
    return nuevo_bst


# ==========================================
# BLOQUE DE PRUEBAS
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DEL BST ---")
    
    # Crear un árbol potencialmente degenerado
    arbol = ArbolBinarioBusqueda()
    for val in [10, 20, 30, 40, 50, 60, 70]:  # Al insertarse ordenados, crea una "lista enlazada"
        arbol.insertar(val)
        
    print("\n1. Árbol Degenerado Original:")
    arbol.mostrar_arbol()
    
    print("\n2. Balanceando el árbol (Tarea 5):")
    arbol_balanceado = balancear_arbol(arbol)
    arbol_balanceado.mostrar_arbol()
    
    print(f"\n3. Recorrido por niveles / BFS (Tarea 2): {arbol_balanceado.por_niveles()}")
    print(f"4. Suma de elementos (Tarea 3): {arbol_balanceado.suma_elementos()}")
    print(f"5. ¿Es completo? (Tarea 4): {arbol_balanceado.es_completo()}")
    
    print("\n6. Eliminando la raíz (40) (Tarea 1):")
    arbol_balanceado.eliminar(40)
    arbol_balanceado.mostrar_arbol()