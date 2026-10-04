# 📚 BIBLIOX - Sistema de Gestión de Biblioteca Digital Interconectada

## 1. Descripción No Técnica del Caso
**BIBLIOX** es una plataforma orientada a la administración inteligente de colecciones bibliográficas y la atención a usuarios. El sistema resuelve tres necesidades reales:
1.  **Inventario Central:** Almacena de manera segura libros digitales con su código ISBN único, título y autor.
2.  **Línea de Espera Justa:** Organiza de forma cronológica a las personas que esperan por un libro muy solicitado, garantizando que el primero en anotarse sea el primero en recibirlo.
3.  **Red de Recomendaciones:** Sugiere automáticamente títulos relacionados a los lectores basándose en patrones de préstamo (ej. *"Lectores que llevaron el libro A también leyeron el libro B"*).

---

## 2. Estructura del Sistema y Componentes Técnicos
El diseño respeta la Programación Orientada a Objetos (POO) mediante la clase `Libro`, cuyos atributos (`__isbn`, `__titulo`, `__autor`) están totalmente encapsulados y protegidos, accediendo a ellos exclusivamente mediante métodos *getters*.

El sistema integra cuatro componentes sobre los mismos datos:
*   **Componente A (Registro Principal):** Una **Lista Doblemente Enlazada** manual que gestiona el inventario de libros de manera secuencial.
*   **Componente B (Índice de Búsqueda):** Un **Árbol Balanceado AVL** con cálculo dinámico de alturas y rotaciones automáticas para localización inmediata de libros por ISBN.
*   **Componente C (Relaciones):** Un **Grafo Dirigido** basado en **Listas de Adyacencia** dinámicas para el sistema de recomendación interconectado.
*   **Componente D (Contrato Único):** Una interfaz (`IColaEspera`) con dos implementaciones intercambiables por polimorfismo: **Cola con Arreglo Circular** y **Cola con Lista Enlazada**.

---

## 3. Justificación Técnica de cada Estructura

### ¿Por qué una Lista Doblemente Enlazada para el Catálogo?
Se seleccionó la variante **doble** porque permite recorrer la biblioteca en ambos sentidos y facilita la eliminación de nodos intermedios (libros dados de baja) en un tiempo constante de \(O(1)\) una vez localizados, modificando únicamente los punteros adyacentes (`siguiente` y `anterior`) sin necesidad de desplazar elementos en memoria.

### ¿Por qué una Lista de Adyacencia para el Grafo de Recomendaciones?
Un libro solo se asocia directamente con unos pocos títulos relacionados, lo que genera un **grafo disperso**. Utilizar una *Matriz de Adyacencia* desperdiciaría memoria de forma cuadrática \(O(V^2)\) guardando celdas vacías. La *Lista de Adyacencia* optimiza el almacenamiento ocupando únicamente un espacio de \(O(V + E)\).

### Comparativa del Contrato de la Cola: Arreglo contra Lista (Componente D)

| Operación | Implementación con Arreglo Fijo | Implementación con Lista Enlazada |
| :--- | :---: | :---: |
| **Encolar (Insertar)** | \(O(1)\) | \(O(1)\) |
| **Desencolar (Sacar)** | \(O(1)\) | \(O(1)\) |
| **Casos Límite Controlados** | `OverflowError` si se llena la capacidad estática | Crecimiento dinámico ilimitado en memoria |

*   **Cuándo conviene cada una:** El *Arreglo Circular* es ideal si el servidor tiene memoria restringida y se conoce con certeza el número máximo de usuarios permitidos en espera. La *Lista Enlazada* conviene cuando la demanda de la fila es masiva e impredecible y no se desea rechazar a ningún usuario.

---

## 4. Experimento del Árbol (Evidencia de Autobalanceo AVL)

Para demostrar la efectividad del Componente B ante la degradación estructural de datos ordenados, el bloque de pruebas simula la inserción secuencial de los ISBNs (`111`, `222`, `333`). 

### Resultados del Experimento en Consola
Mientras que un árbol ordinario habría quedado desbalanceado en forma de línea recta con una altura de 3, el **Árbol AVL detectó un factor de balanceo de -2** tras el ingreso del nodo `333`, disparando de forma automática una **Rotación Simple a la Izquierda** sobre la raíz original.

El estado final del índice balanceado recolectado directamente de la terminal es:
*   `[ISBN: 111 -> Altura: 1, Balance: 0]`
*   `[ISBN: 222 -> Altura: 2, Balance: 0]`
*   `[ISBN: 333 -> Altura: 1, Balance: 0]`

**Conclusión:** La rotación promovió al nodo `222` como la nueva raíz central, reduciendo la altura máxima a **2** y restableciendo los factores de equilibrio a **0**. Esto garantiza que el costo de búsqueda se mantenga óptimo en tiempo logarítmico \(O(\log n)\) bajo cualquier escenario de inserción.

---

## 5. Casos de Prueba y Controles Especiales
El sistema controla de forma nativa las siguientes condiciones especiales exigidas por la rúbrica:
1.  **Clave Repetida (Caso Límite 1):** Si se intenta registrar un libro con un ISBN ya existente en el catálogo, el sistema arroja una excepción `ValueError` controlada.
2.  **Desborde de Cola (Caso Límite 2):** Al superar el límite estático en la `ColaArreglo`, se dispara un `OverflowError` controlado que protege la estabilidad del software.
3.  **Polimorfismo Efectivo:** Ambas implementaciones de la cola responden de manera idéntica al contrato unificado de `IColaEspera`, permitiendo el intercambio limpio de componentes en tiempo de ejecución.

---

## 6. Instrucciones de Ejecución
1.  Asegúrese de tener instalado **Python 3.10** o superior.
2.  Clone el repositorio e ingrese al directorio del proyecto.
3.  Ejecute el archivo principal para ver el despliegue automático de casos:
    ```bash
    python main.py
    ```

---
*   **Enlace al Video de Sustentación:** [Insertar enlace aquí]
