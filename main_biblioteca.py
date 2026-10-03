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
# IMPLEMENTACION 1: COLA CON ARREGLO FIJO - CIRCULAR (COMPONENTE D)
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
            raise OverflowError("Error: La cola de espera esta llena.")
        self.__items[self.__final] = nombre_usuario
        self.__final = (self.__final + 1) % self.__capacidad
        self.__tamano += 1

    def desencolar(self) -> str:
        if self.esta_vacia():
            raise IndexError("Error: La lista de espera esta vacia.")
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
# IMPLEMENTACION 2: COLA CON LISTA ENLAZADA (COMPONENTE A Y D)
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
            raise IndexError("Error: La lista de espera esta vacia.")
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

    def get_isbn(self) -> str:
        return self.__isbn

    def get_titulo(self) -> str:
        return self.__titulo

    def get_autor(self) -> str:
        return self.__autor

    def __str__(self):
        return f"[ISBN: {self.__isbn} | '{self.__titulo}' - {self.__autor}]"


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


# =====================================================================
# INDICE DE BUSQUEDA: ARBOL BINARIO DE BUSQUEDA (COMPONENTE B)
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
        if nodo is None:
            return NodoArbol(libro)
        if libro.get_isbn() < nodo.libro.get_isbn():
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, libro)
        elif libro.get_isbn() > nodo.libro.get_isbn():
            nodo.derecho = self._insertar_recursivo(nodo.derecho, libro)
        return nodo

    def obtener_inorden_lista(self) -> list:
        lista = []
        self._inorden_rec(self.__raiz, lista)
        return lista

    def _inorden_rec(self, nodo, lista):
        if nodo:
            self._inorden_rec(nodo.izquierdo, lista)
            lista.append(nodo.libro.get_isbn())
            self._inorden_rec(nodo.derecho, lista)


# =====================================================================
# RELACIONES: GRAFO DE RECOMENDACIONES (COMPONENTE C)
# =====================================================================
class NodoVecino:
    def __init__(self, isbn_destino: str):
        self.isbn_destino = isbn_destino
        self.siguiente = None


class GrafoRecomendaciones:
    def __init__(self):
        self.__adyacencias = {}

    def agregar_libro(self, isbn: str) -> None:
        if isbn not in self.__adyacencias:
            self.__adyacencias[isbn] = None

    def agregar_recomendacion(self, isbn_origen: str, isbn_destino: str) -> None:
        self.agregar_libro(isbn_origen)
        self.agregar_libro(isbn_destino)

        nuevo_vecino = NodoVecino(isbn_destino)
        nuevo_vecino.siguiente = self.__adyacencias[isbn_origen]
        self.__adyacencias[isbn_origen] = nuevo_vecino

    def obtener_recomendaciones_lista(self, isbn: str) -> list:
        lista = []
        if isbn in self.__adyacencias:
            actual = self.__adyacencias[isbn]
            while actual is not None:
                lista.append(actual.isbn_destino)
                actual = actual.siguiente
        return lista


# =====================================================================
# PRUEBA DEL SISTEMA INTEGRADO (VERSION ULTRA-COMPATIBLE)
# =====================================================================
if __name__ == "__main__":
    # 1. Instanciar y cargar componentes de prueba internamente
    catalogo = CatalogoLibros()
    indice = IndiceLibros()
    grafo = GrafoRecomendaciones()
    cola_espera = ColaListaEnlazada()

    l1 = Libro("111", "El Quijote", "Cervantes")
    l2 = Libro("222", "Cien Anos de Soledad", "Gabriel Garcia Marquez")
    l3 = Libro("333", "Ficciones", "Jorge Luis Borges")

    catalogo.insertar(l1)
    catalogo.insertar(l2)
    catalogo.insertar(l3)

    indice.insertar(l1)
    indice.insertar(l2)
    indice.insertar(l3)

    grafo.agregar_recommendacion = grafo.agregar_recomendacion
    grafo.agregar_recomendacion("111", "222")
    grafo.agregar_recomendacion("111", "333")

    cola_espera.encolar("Andres")
    cola_espera.encolar("Beatriz")

    # 2. Recolectar datos de las estructuras sin usar prints intermedios
    lista_isbn = " ".join(indice.obtener_inorden_lista())
    lista_grafo = " ".join(grafo.obtener_recomendaciones_lista("111"))
    u1 = cola_espera.desencolar()
    u2 = cola_espera.desencolar()

    # 3. CONSTRUIR UNA UNICA CADENA PARA EVITAR EL BUG DEL COMPILADOR WEB
    resultado_final = (
        "--- Probando Sistema de Biblioteca ---\n"
        f"Recorrido Inorden del Indice (ISBNs): {lista_isbn}\n"
        f"Libros recomendados para 111: {lista_grafo}\n"
        "Probando Cola de Espera:\n"
        f"Siguiente en atender: {u1}\n"
        f"Siguiente en atender: {u2}"
    )

    # Un solo print limpia el buffer del simulador web por completo
    print(resultado_final)



