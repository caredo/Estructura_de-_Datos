# =====================================================================
# CONTRATO (INTERFAZ) PARA LA COLA DE ESPERA (COMPONENTE D)
# =====================================================================
class IColaEspera:
    def encolar(self, nombre_usuario: str) -> None:
        pass
    def desencolar(self) -> str:
        pass
    def esta_vacia(self) -> bool:
        pass
    def tamano(self) -> int:
        pass

# =====================================================================
# IMPLEMENTACIÓN 1: COLA CON ARREGLO FIJO - CIRCULAR (COMPONENTE D)
# =====================================================================
class ColaArreglo(IColaEspera):
    def __init__(self, capacidad: int = 10):
        self.__capacidad = capacidad
        self.__items = [None] * capacidad
        self.__frente = 0
        self.__final = 0
        self.__tamano = 0

    def encolar(self, nombre_usuario: str) -> None:
        if self.__tamano == self.__capacidad:
            raise OverflowError("🚨 Error: La cola de espera está llena.")
        self.__items[self.__final] = nombre_usuario
        self.__final = (self.__final + 1) % self.__capacidad
        self.__tamano += 1

    def desencolar(self) -> str:
        if self.esta_vacia():
            raise IndexError("🚨 Error: La lista de espera está vacía.")
        usuario = self.__items[self.__frente]
        self.__items[self.__frente] = None
        self.__frente = (self.__frente + 1) % self.__capacidad
        self.__tamano -= 1
        return usuario

    def esta_vacia(self) -> bool:
        return self.__tamano == 0

    def tamano(self) -> int:
        return self.__tamano

# =====================================================================
# IMPLEMENTACIÓN 2: COLA CON LISTA ENLAZADA (COMPONENTE A Y D)
# =====================================================================
class NodoUsuario:
    def __init__(self, nombre_usuario: str):
        self.nombre_usuario = nombre_usuario
        self.siguiente = None

class ColaListaEnlazada(IColaEspera):
    def __init__(self):
        self.__frente = None
        self.__final = None
        self.__tamano = 0

    def encolar(self, nombre_usuario: str) -> None:
        nuevo_nodo = NodoUsuario(nombre_usuario)
        if self.esta_vacia():
            self.__frente = nuevo_nodo
        else:
            self.__final.siguiente = nuevo_nodo
        self.__final = nuevo_nodo
        self.__tamano += 1

    def desencolar(self) -> str:
        if self.esta_vacia():
            raise IndexError("🚨 Error: La lista de espera está vacía.")
        usuario = self.__frente.nombre_usuario
        self.__frente = self.__frente.siguiente
        if self.__frente is None:
            self.__final = None
        self.__tamano -= 1
        return usuario

    def esta_vacia(self) -> bool:
        return self.__frente is None

    def tamano(self) -> int:
        return self.__tamano

# =====================================================================
# ENTIDAD PRINCIPAL ENCAPSULADA
# =====================================================================
class Libro:
    def __init__(self, isbn: str, titulo: str, autor: str):
        self.__isbn = isbn
        self.__titulo = titulo
        self.__autor = autor

    def get_isbn(self) -> str: return self.__isbn
    def get_titulo(self) -> str: return self.__titulo
    def get_autor(self) -> str: return self.__autor
    def __str__(self): return f"[ISBN: {self.__isbn} | '{self.__titulo}' - {self.__autor}]"

# =====================================================================
# REGISTRO PRINCIPAL: LISTA DOBLEMENTE ENLAZADA (COMPONENTE A)
# =====================================================================
class NodoDoble:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.siguiente = None
        self.anterior = None

class CatalogoLibros:
    def __init__(self):
        self.__cabeza = None
        self.__cola = None

    def insertar(self, libro: Libro) -> None:
        if self.buscar(libro.get_isbn()) is not None:
            print(f"⚠️ Advertencia: El libro {libro.get_isbn()} ya existe.")
            return
        nuevo = NodoDoble(libro)
        if self.__cabeza is None:
            self.__cabeza = nuevo
            self.__cola = nuevo
        else:
            self.__cola.siguiente = nuevo
            nuevo.anterior = self.__cola
            self.__cola = nuevo

    def buscar(self, isbn: str) -> Libro:
        actual = self.__cabeza
        while actual is not None:
            if actual.libro.get_isbn() == isbn:
                return actual.libro
            actual = actual.siguiente
        return None

    def eliminar(self, isbn: str) -> bool:
        actual = self.__cabeza
        while actual is not None:
            if actual.libro.get_isbn() == isbn:
                if actual.anterior is None and actual.siguiente is None:
                    self.__cabeza = None
                    self.__cola = None
                elif actual.anterior is None:
                    self.__cabeza = actual.siguiente
                    self.__cabeza.anterior = None
                elif actual.siguiente is None:
                    self.__cola = actual.anterior
                    self.__cola.siguiente = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                return True
            actual = actual.siguiente
        return False

    def recorrer(self) -> None:
        if self.__cabeza is None:
            print("El catálogo está vacío.")
            return
        actual = self.__cabeza
        while actual is not None:
            print(f"  -> {actual.libro}")
            actual = actual.siguiente

# =====================================================================
# ÍNDICE DE BÚSQUEDA: ÁRBOL BINARIO DE BÚSQUEDA (COMPONENTE B)
# =====================================================================
class NodoArbol:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.izquierdo = None
        self.derecho = None

class IndiceLibros:
    def __init__(self):
        self.__raiz = None

    def insertar(self, libro: Libro) -> None:
        self.__raiz = self._insertar_recursivo(self.__raiz, libro)

    def _insertar_recursivo(self, nodo: NodoArbol, libro: Libro) -> NodoArbol:
        if nodo is None: return NodoArbol(libro)
        if libro.get_isbn() < nodo.libro.get_isbn():
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, libro)
        elif libro.get_isbn() > nodo.libro.get_isbn():
            nodo.derecho = self._insertar_recursivo(nodo.derecho, libro)
        return nodo

    def buscar(self, isbn: str) -> Libro:
        return self._buscar_recursivo(self.__raiz, isbn)

    def _buscar_recursivo(self, nodo: NodoArbol, isbn: str) -> Libro:
        if nodo is None or nodo.libro.get_isbn() == isbn:
            return nodo.libro if nodo else None
        if isbn < nodo.libro.get_isbn():
            return self._buscar_recursivo(nodo.izquierdo, isbn)
        return self._buscar_recursivo(nodo.derecho, isbn)

    def inorden(self) -> None: self._inorden_rec(self.__raiz); print()
    def _inorden_rec(self, nodo):
        if nodo:
            self._inorden_rec(nodo.izquierdo)
            print(nodo.libro.get_isbn(), end=" ")
            self._inorden_rec(nodo.derecho)

    def preorden(self) -> None: self._preorden_rec(self.__raiz); print()
    def _preorden_rec(self, nodo):
        if nodo:
            print(nodo.libro.get_isbn(), end=" ")
            self._preorden_rec(nodo.izquierdo)
            self._preorden_rec(nodo.derecho)

    def postorden(self) -> None: self._postorden_rec(self.__raiz); print()
    def _postorden_rec(self, nodo):
        if nodo:
            self._postorden_rec(nodo.izquierdo)
            self._postorden_rec(nodo.derecho)
            print(nodo.libro.get_isbn(), end=" ")

# =====================================================================
# RELACIONES: GRAFO DE RECOMENDACIONES (COMPONENTE C)
# =====================================================================
class NodoVecino:
    def __init__(self, isbn_destino: str):
        self.isbn_destino = isbn_destino
        self.siguiente = None

class GrafoRecomendaciones:
    def __init__(self, max_libros: int = 20):
        self.__max_libros = max_libros
        self.__vertices_isbn = [None] * max_libros
        self.__listas_adyacencia = [None] * max_libros
        self.__total_vertices = 0

    def registrar_libro(self, isbn: str) -> None:
        for i in range(self.__total_vertices):
            if self.__vertices_isbn[i] == isbn: return
        if self.__total_vertices < self.__max_libros:
            self.__vertices_isbn[self.__total_vertices] = isbn
            self.__listas_adyacencia[self.__total_vertices] = None
            self.__total_vertices += 1

    def enlazar_libros(self, isbn_a: str, isbn_b: str) -> None:
        self.registrar_libro(isbn_a)
        self.registrar_libro(isbn_b)
        idx_a = self._buscar_indice(isbn_a)
        nuevo_b = NodoVecino(isbn_b)
        nuevo_b.siguiente = self.__listas_adyacencia[idx_a]
        self.__listas_adyacencia[idx_a] = nuevo_b

        idx_b = self._buscar_indice(isbn_b)
        nuevo_a = NodoVecino(isbn_a)
        nuevo_a.siguiente = self.__listas_adyacencia[idx_b]
        self.__listas_adyacencia[idx_b] = nuevo_a

    def _buscar_indice(self, isbn: str) -> int:
        for i in range(self.__total_vertices):
            if self.__vertices_isbn[i] == isbn: return i
        return -1

    def consultar_recomendaciones(self, isbn: str) -> None:
        idx = self._buscar_indice(isbn)
        if idx == -1: return
        print(f"📚 Libros recomendados para {isbn}:", end=" ")
        actual = self.__listas_adyacencia[idx]
        while actual:
            print(actual.isbn_destino, end=" | ")
            actual = actual.siguiente
        print()

