class IColaEspera:
    def encolar(self, nombre_usuario: str) -> None: pass
    def desencolar(self) -> str: pass
    def esta_vacia(self) -> bool: pass
    def tamano(self) -> int: pass

class ColaArreglo(IColaEspera):
    def __init__(self, capacidad: int = 10):
        self.__capacidad = capacidad
        self.__items = [None] * capacidad
        self.__frente = 0
        self.__final = 0
        self.__tamano = 0
    def encolar(self, nombre_usuario: str) -> None:
        if self.__tamano == self.__capacidad: raise OverflowError("🚨 Cola llena.")
        self.__items[self.__final] = nombre_usuario
        self.__final = (self.__final + 1) % self.__capacidad
        self.__tamano += 1
    def desencolar(self) -> str:
        if self.esta_vacia(): raise IndexError("🚨 Cola vacia.")
        usuario = self.__items[self.__frente]
        self.__items[self.__frente] = None
        self.__frente = (self.__frente + 1) % self.__capacidad
        self.__tamano -= 1
        return usuario
    def esta_vacia(self) -> bool: return self.__tamano == 0
    def tamano(self) -> int: return self.__tamano

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
        nuevo = NodoUsuario(nombre_usuario)
        if self.esta_vacia(): self.__frente = nuevo
        else: self.__final.siguiente = nuevo
        self.__final = nuevo
        self.__tamano += 1
    def desencolar(self) -> str:
        if self.esta_vacia(): raise IndexError("🚨 Cola vacia.")
        usuario = self.__frente.nombre_usuario
        self.__frente = self.__frente.siguiente
        if self.__frente is None: self.__final = None
        self.__tamano -= 1
        return usuario
    def esta_vacia(self) -> bool: return self.__frente is None
    def tamano(self) -> int: return self.__tamano

class Libro:
    def __init__(self, isbn: str, titulo: str, autor: str):
        self.__isbn = isbn
        self.__titulo = titulo
        self.__autor = autor
    def get_isbn(self) -> str: return self.__isbn
    def get_titulo(self) -> str: return self.__titulo
    def get_autor(self) -> str: return self.__autor
    def __str__(self): return f"[ISBN: {self.__isbn} | '{self.__titulo}' - {self.__autor}]"

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
        if self.buscar(libro.get_isbn()) is not None: return
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
            if actual.libro.get_isbn() == isbn: return actual.libro
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
        actual = self.__cabeza
        while actual is not None:
            print(f"  -> {actual.libro}")
            actual = actual.siguiente

class NodoArbol:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.izquierdo = None
        self.derecho = None

class IndiceLibros:
    def __init__(self): self.__raiz = None
    def insertar(self, libro: Libro) -> None: self.__raiz = self._ins(self.__raiz, libro)
    def _ins(self, nodo: NodoArbol, libro: Libro) -> NodoArbol:
        if nodo is None: return NodoArbol(libro)
        if libro.get_isbn() < nodo.libro.get_isbn(): nodo.izquierdo = self._ins(nodo.izquierdo, libro)
        elif libro.get_isbn() > nodo.libro.get_isbn(): nodo.derecho = self._ins(nodo.derecho, libro)
        return nodo
    def buscar(self, isbn: str) -> Libro: return self._bus(self.__raiz, isbn)
    def _bus(self, nodo: NodoArbol, isbn: str) -> Libro:
        if nodo is None or nodo.libro.get_isbn() == isbn: return nodo.libro if nodo else None
        if isbn < nodo.libro.get_isbn(): return self._bus(nodo.izquierdo, isbn)
        return self._bus(nodo.derecho, isbn)

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
            self.__total_vertices += 1
    def enlazar_libros(self, isbn_a: str, isbn_b: str) -> None:
        self.registrar_libro(isbn_a)
        self.registrar_libro(isbn_b)
        idx_a = self._idx(isbn_a)
        nuevo_b = NodoVecino(isbn_b)
        nuevo_b.siguiente = self.__listas_adyacencia[idx_a]
        self.__listas_adyacencia[idx_a] = nuevo_b
        idx_b = self._idx(isbn_b)
        nuevo_a = NodoVecino(isbn_a)
        nuevo_a.siguiente = self.__listas_adyacencia[idx_b]
        self.__listas_adyacencia[idx_b] = nuevo_a
    def _idx(self, isbn: str) -> int:
        for i in range(self.__total_vertices):
            if self.__vertices_isbn[i] == isbn: return i
        return -1
    def consultar_recomendaciones(self, isbn: str) -> None:
        idx = self._idx(isbn)
        if idx == -1: return
        print(f"📚 Libros recomendados para {isbn}:", end=" ")
        actual = self.__listas_adyacencia[idx]
        while actual:
            print(actual.isbn_destino, end=" | ")
            actual = actual.siguiente
        print()

if __name__ == "__main__":
    print("=== INICIALIZANDO SISTEMA DE BIBLIOTECA BIBLIOX ===\n")
    catalogo = CatalogoLibros()
    indice_busqueda = IndiceLibros()
    red_recomendaciones = GrafoRecomendaciones()
    cola_espera = ColaListaEnlazada()
    
    print(f"⚙️ Motor de cola activo: {type(cola_espera).__name__}\n")
    
    l1 = Libro("978-01", "Cien anos de soledad", "Gabriel Garcia Marquez")
    l2 = Libro("978-02", "Don Quijote de la Mancha", "Miguel de Cervantes")
    l3 = Libro("978-03", "El Aleph", "Jorge Luis Borges")
    
    for libro in [l1, l2, l3]:
        catalogo.insertar(libro)
        indice_busqueda.insertar(libro)
        
    red_recomendaciones.enlazar_libros("978-01", "978-03")
    
    print("--- 1. Recorrido del catalogo ---")
    catalogo.recorrer()
    print("\n--- 2. Busqueda en Indice ABB ---")
    print(f"Resultado: {indice_busqueda.buscar('978-02')}")
    print("\n--- 3. Consultas al Grafo ---")
    red_recomendaciones.consultar_recomendaciones("978-01")
    print("\n--- 4. Gestion de Fila de Espera ---")
    cola_espera.encolar("Carlos Gomez")
    cola_espera.encolar("Ana Martinez")
    print(f"Atendiendo a: {cola_espera.desencolar()}")
