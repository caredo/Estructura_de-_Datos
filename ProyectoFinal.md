# 📚 BIBLIOX - Sistema de Gestión de Biblioteca Digital Interconectada

## 1. Descripción No Técnica del Caso
**BIBLIOX** es una plataforma orientada a la administración inteligente de colecciones bibliográficas y la atención a usuarios. El sistema resuelve tres necesidades reales:
1.  **Inventario Central:** Almacena de manera segura libros digitales con su código ISBN único, título y autor.
2.  **Línea de Espera Justa:** Organiza de forma cronológica a las personas que esperan por un libro muy solicitado, garantizando que el primero en anotarse sea el primero en recibirlo.
3.  **Red de Recomendaciones:** Sugiere automáticamente títulos relacionados a los lectores basándose en patrones de co-prestamo (ej. *"Lectores que llevaron el libro A también leyeron el libro B"*).

---

## 2. Estructura del Sistema y Componentes Técnicos
El diseño respeta la Programación Orientada a Objetos (POO) mediante la clase `Libro`, cuyos atributos (`__isbn`, `__titulo`, `__autor`) están totalmente encapsulados y protegidos, accediendo a ellos exclusivamente mediante métodos *getters*.

El sistema integra cuatro componentes sobre los mismos datos:
*   **Componente A (Registro Principal):** Una **Lista Doblemente Enlazada** manual que gestiona el inventario de libros.
*   **Componente B (Índice de Búsqueda):** Un **Árbol Binario de Búsqueda (ABB)** recursivo para localización inmediata de libros por ISBN.
*   **Componente C (Relaciones):** Un **Grafo No Dirigido** basado en **Listas de Adyacencia** puras para el sistema de recomendación.
*   **Componente D (Contrato Único):** Una interfaz (`IColaEspera`) con dos implementaciones intercambiables: **Cola con Arreglo Circular** y **Cola con Lista Enlazada**.

---

## 3. Justificación Técnica de cada Estructura

### ¿Por qué una Lista Doblemente Enlazada para el Catálogo?
Se seleccionó la variante **doble** porque permite recorrer la biblioteca en ambos sentidos y facilita la eliminación de nodos intermedios (libros dados de baja) en un tiempo constante de \(O(1)\) una vez localizados, modificando únicamente los punteros de los nodos adyacentes sin necesidad de desplazar elementos en memoria.

### ¿Por qué una Lista de Adyacencia para el Grafo de Recomendaciones?
Un libro solo se asocia directamente con unos pocos títulos del mismo género, lo que genera un **grafo disperso**. Utilizar una *Matriz de Adyacencia* desperdiciaría memoria de forma cuadrática \(O(V^2)\) guardando celdas vacías. La *Lista de Adyacencia* optimiza el almacenamiento ocupando únicamente un espacio de \(O(V + E)\).

### Comparativa del Contrato de la Cola: Arreglo contra Lista (Componente D)

| Operación | Implementación con Arreglo Fijo | Implementación con Lista Enlazada |
| :--- | :---: | :---: |
| **Encolar (Insertar)** | \(O(1)\) | \(O(1)\) |
| **Desencolar (Sacar)** | \(O(1)\) | \(O(1)\) |
| **Casos Límite Controlados** | `OverflowError` si se llena la capacidad estática | Crecimiento dinámico ilimitado en memoria |

*   **Cuándo conviene cada una:** El *Arreglo Circular* es ideal si el servidor tiene memoria restringida y se conoce con certeza el número máximo de usuarios en espera. La *Lista Enlazada* conviene cuando la demanda de la fila es masiva e impredecible y no se quiere rechazar a ningún usuario.

---

## 4. Experimento del Árbol (Medición de Alturas)

Para demostrar el impacto del orden de los datos en un Árbol Binario de Búsqueda convencional, se insertaron los mismos 15 libros bajo dos condiciones diferentes:

### Tabla de Resultados del Experimento

| Condición de Inserción | Claves ISBN en Orden de Ingreso | Altura del Árbol |
| :--- | :--- | :---: |
| **Árbol A (Desordenado)** | `978-08, 978-04, 978-12, 978-02, 978-06, 978-10, 978-14, 978-01, 978-03, 978-05, 978-07, 978-09, 978-11, 978-13, 978-15` | **4** |
| **Árbol B (Ordenado)** | `978-01, 978-02, 978-03, 978-04, 978-05, 978-06, 978-07, 978-08, 978-09, 978-10, 978-11, 978-12, 978-13, 978-14, 978-15` | **15** |

### Explicación de la Degradación Estructural
*   **Análisis:** Al ingresar datos de forma estrictamente ordenada (Árbol B), el árbol pierde su ramificación bilateral y se convierte estructuralmente en una **línea recta (lista enlazada espigada)**.
*   **Efecto en la búsqueda:** El Árbol A mantiene un costo de búsqueda eficiente de \(O(\log n)\), requiriendo máximo 4 comparaciones. El Árbol B se degrada a un costo lineal de \(O(n)\), obligando al sistema a realizar hasta 15 operaciones para encontrar el último libro, destruyendo la ventaja de la estrategia *Divide y Vencerás*.
*   **Solución AVL:** Un árbol AVL evita esta degradación mediante **rotaciones automáticas** cada vez que detecta un desbalance en los factores de altura, asegurando un balance óptimo constante.

*(Nota: La imagen de los dibujos paso a paso de las rotaciones AVL requeridas por el punto 3.5 debe ser anexada aquí por el estudiante)*.

---

## 5. Casos de Prueba y Controles Especiales
El sistema controla de forma nativa las siguientes condiciones especiales exigidas por la rúbrica:
1.  **Clave Repetida:** Si se intenta insertar un libro con un ISBN ya registrado en el catálogo, el sistema detiene la operación y emite una advertencia.
2.  **Clave que no existe:** Al buscar un ISBN inexistente en el árbol, la recursividad retorna `None` de forma segura en lugar de romper el flujo.
3.  **Eliminación del único elemento:** Al remover el último libro disponible en la lista doble, los punteros de `cabeza` y `cola` se limpian simultáneamente a `None`, dejando la estructura vacía y estable.

---

## 6. Instrucciones de Ejecución
1.  Asegúrese de tener instalado **Python 3.10** o superior.
2.  Clone el repositorio: `git clone https://github.com`
3.  Ejecute el archivo principal: `python main.py`

---
*   **Enlace al Video de Sustentación:** [Insertar enlace aquí]
