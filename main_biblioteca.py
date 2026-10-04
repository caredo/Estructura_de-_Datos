class IColaEspera:
    def encolar(self, nombre_usuario: str) -> None:
        pass

    def desencolar(self) -> str:
        pass

    def esta_vacia(self) -> bool:
        pass

    def tamano(self) -> int:
        pass


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


class NodoUsuario:
    def __init__(self, nombre_usuario: str):
        self.nombre_usuario = nombre_usuario
        self.siguiente = None


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
            raise ValueError(f"Error: El ISBN {libro.get_isbn()} ya existe.")
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


class NodoArbol:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


class IndiceLibros:
    def __init__(self):
        self.__raiz = None

    def _obtener_altura(self, nodo: NodoArbol) -> int:
        if nodo:
            return nodo.altura
        return 0

    def _obtener_balance(self, nodo: NodoArbol) -> int:
        if not nodo:
            return 0
        alt_izq = self._obtener_altura(nodo.izquierdo)
        alt_der = self._obtener_altura(nodo.derecho)
        return alt_izq - alt_der

    def _rotar_derecha(self, y: NodoArbol) -> NodoArbol:
        x = y.izquierdo
        T2 = x.derecho
        x.derecho = y
        y.izquierdo = T2
        y.altura = 1 + max(self._obtener_altura(y.izquierdo), self._obtener_altura(y.derecho))
        x.altura = 1 + max(self._obtener_altura(x.izquierdo), self._obtener_altura(x.derecho))
        return x

    def _rotar_izquierda(self, x: NodoArbol) -> NodoArbol:
        y = x.derecho
        T2 = y.izquierdo
        y.izquierdo = x
        x.derecho = T2
        x.altura = 1 + max(self._obtener_altura(x.izquierdo), self._obtener_altura(x.derecho))
        y.altura = 1 + max(self._obtener_altura(y.izquierdo), self._obtener_altura(y.derecho))
        return y

    def insertar(self, libro: Libro) -> None:
        self.__raiz = self._insertar_recursivo(self.__raiz, libro)

    def _insertar_recursivo(self, nodo: NodoArbol, libro: Libro) -> NodoArbol:
        if nodo is None:
            return NodoArbol(libro)
        if libro.get_isbn() < nodo.libro.get_isbn():
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, libro)
        elif libro.get_isbn() > nodo.libro.get_isbn():
            nodo.derecho = self._insertar_recursivo(nodo.derecho, libro)
        else:
            return nodo

        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierdo), self._obtener_altura(nodo.derecho))
        balance = self._obtener_balance(nodo)

        if balance > 1 and libro.get_isbn() < nodo.izquierdo.libro.get_isbn():
            return self._rotar_derecha(nodo)
        if balance < -1 and libro.get_isbn() > nodo.derecho.libro.get_isbn():
            return self._rotar_izquierda(nodo)
        if balance > 1 and libro.get_isbn() > nodo.izquierdo.libro.get_isbn():
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        if balance < -1 and libro.get_isbn() < nodo.derecho.libro.get_isbn():
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
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

    def imprimir_tabla_alturas(self) -> None:
        self._imprimir_alturas_rec(self.__raiz)

    def _imprimir_alturas_rec(self, nodo):
        if nodo:
            self._imprimir_alturas_rec(nodo.izquierdo)
            balance = self._obtener_balance(nodo)
            print(f"  [ISBN: {nodo.libro.get_isbn()} -> Altura: {nodo.altura}, Balance: {balance}]")
            self._imprimir_alturas_rec(nodo.derecho)


class NodoVecino:
    def __init__(self, isbn_destino: str):
        self.isbn_destino = isbn_destino
        self.siguiente = None


class GrafoRecomendaciones:
    def __init__(self):
        self.adyacencias = {}

    def agregar_libro(self, isbn: str) -> None:
        if isbn not in self.adyacencias:
            self.adyacencias[isbn] = None

    def agregar_recomendacion(self, isbn_origen: str, isbn_destino: str) -> None:
        self.agregar_libro(isbn_origen)
        self.agregar_libro(isbn_destino)
        nuevo_vecino = NodoVecino(isbn_destino)
        nuevo_vecino.siguiente = self.adyacencias[isbn_origen]
        self.adyacencias[isbn_origen] = nuevo_vecino


print("--- PUNTO 4: DEMOSTRACION DE CASOS ---")
catalogo = CatalogoLibros()
indice = IndiceLibros()
grafo = GrafoRecomendaciones()
l1 = Libro("111", "El Quijote", "Cervantes")
l2 = Libro("222", "Cien Anos de Soledad", "Gabo")
l3 = Libro("333", "Ficciones", "Borges")

catalogo.insertar(l1)
catalogo.insertar(l2)
catalogo.insertar(l3)
indice.insertar(l1)
indice.insertar(l2)
indice.insertar(l3)
grafo.agregar_recomendacion("111", "222")
grafo.agregar_recomendacion("111", "333")

print("[OK] Caso Normal cargado.")
lista_isbns = " ".join(indice.obtener_inorden_lista())
print(f"  ISBNs en Indice AVL: {lista_isbns}")

print("\n[TEST] Caso Limite 1: Duplicado")
try:
    catalogo.insertar(Libro("111", "Duplicado", "Autor"))
except ValueError as e:
    print(f"  Capturado -> {str(e)}")

print("\n[TEST] Caso Limite 2: Overflow Cola")
cola_limite = ColaArreglo(capacidad=2)
try:
    cola_limite.encolar("U1")
    cola_limite.encolar("U2")
    cola_limite.encolar("U3")
except OverflowError as e:
    print(f"  Capturado -> {str(e)}")

print("\n[TEST] Intercambio de Colas")
c_arr = ColaArreglo(capacidad=5)
c_arr.encolar("Andres")
c_arr.encolar("Beatriz")
c_lis = ColaListaEnlazada()
c_lis.encolar("Andres")
c_lis.encolar("Beatriz")
print(f"  ColaArreglo: {c_arr.desencolar()} y {c_arr.desencolar()}")
print(f"  ColaListaEnlazada: {c_lis.desencolar()} y {c_lis.desencolar()}")

print("\n--- PUNTO 5: TABLA DE ALTURAS AVL ---")
indice.imprimir_tabla_alturas()
