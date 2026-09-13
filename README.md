# HelpDesk-QueueManager 🛠️👨‍💻

**Actividad Evaluativa:** Una estructura de datos en acción  
**Curso:** Estructura de Datos  
**Estudiante:** Carlos Eduardo Rojas Ayala
**Entorno de Desarrollo:** Python 3.x  

---

## 1. Descripción No Técnica del Problema 🏢
En el departamento de sistemas e infraestructura tecnológica de la Fundacion Universitaria Maria Cano, los empleados experimentan incidentes técnicos diariamente (fallas de conectividad a la VPN, bloqueos de contraseñas, pantallas azules o problemas con impresoras). 

Cuando muchos usuarios reportan fallas al mismo tiempo, el equipo de soporte técnico (Mesa de Ayuda) puede verse saturado. Si las solicitudes se gestionan de manera informal (por mensajes de chat, correos dispersos o llamadas), los casos se atienden en desorden, se pierden requerimientos y se genera frustración. 

### La Solución
**HelpDesk-QueueManager** es una aplicación diseñada para organizar la atención de soporte técnico de forma justa y eficiente. El sistema actúa como una "sala de espera virtual" con un límite máximo de almacenamiento diario (capacidad fija para 10 tickets). Los incidentes se registran estrictamente en el orden en que ocurren, garantizando que el primer empleado en reportar un problema sea el primero en recibir atención de un técnico. El sistema impide que se pierdan datos y avisa de manera clara cuando el equipo de soporte ha alcanzado su límite de atención diaria.

---

## 2. Estructura de Datos Seleccionada 📊
La estructura de datos central de esta solución es una **Cola implementada mediante un Vector (Arreglo Estático) de tamaño fijo**, utilizando una lógica de **Cola Circular**.

### Justificación Técnica de la Elección
*   **Principio FIFO (First In, First Out):** Una cola es la única estructura lineal que garantiza que el primer elemento en entrar sea el primero en salir, lo cual es el requerimiento operativo y ético fundamental de una mesa de ayuda.
*   **Eficiencia en el Acceso y Modificación:** Al implementar la cola de manera **circular** utilizando aritmética modular (operador `%`), las operaciones de inserción (`registrar_ticket`) y eliminación (`atender_ticket`) se realizan en un tiempo constante **O(1)**. 
*   **Optimización de Memoria:** No necesitamos desplazar los elementos del vector hacia adelante cada vez que se atiende un ticket (lo cual costaría un tiempo *O(n)*). En su lugar, los punteros `frente` y `final` se mueven cíclicamente a lo largo de las 10 posiciones del vector, reutilizando los espacios liberados de forma inmediata.

### Limitaciones de la Solución
*   **Capacidad Rígida:** Al estar basada en un arreglo estático, la capacidad máxima está fija en 10 tickets. Si llega el ticket número 11 y la cola está llena, ocurre un desbordamiento (*Queue Overflow*) y el ticket es rechazado, obligando al usuario a esperar que un técnico libere espacio.

---

## 3. Análisis Comparativo: ¿Qué pasaría si usáramos una Pila? 🔄

Para validar la elección, se comparó el diseño de la **Cola** frente a una **Pila (Stack)** implementada también sobre un vector:

| Criterio de Comparación | Estructura Elegida: **Cola** | Estructura Alternativa: **Pila** |
| :--- | :--- | :--- |
| **Organización de Datos** | Secuencial, tipo **FIFO** (Primero en entrar, primero en salir). | Secuencial, tipo **LIFO** (Último en entrar, primero en salir). |
| **Acceso a Elementos** | Restringido. Solo se opera el elemento en el `frente`. | Restringido. Solo se opera el elemento en el tope (`top`). |
| **Operaciones Principales** | Inserción al `final`, eliminación por el `frente`. | Inserción y eliminación ocurren exclusivamente en el tope. |
| **Facilidad de Implementación** | **Moderada:** Requiere controlar punteros con lógica circular (`%`). | **Alta:** Solo requiere incrementar o decrementar un único índice de tope. |
| **Impacto en el Problema** | **Ideal y Justo:** Respeta rigurosamente el orden de llegada de los usuarios. | **Inviable:** El último empleado en reportar un fallo sería el primero en ser atendido. El primer usuario en reportar podría quedar esperando indefinidamente (*hambruna de procesos*). |

---

## 4. Instrucciones para Ejecutar el Programa 🚀

### Requisitos Previos
*   Tener instalado **Python 3.7** o superior.

### Pasos para la Ejecución
1. Descargue o clone este repositorio en su máquina local.
2. Navegue al directorio del proyecto donde se encuentra el archivo `main.py`.
3. Ejecute el script principal desde la terminal o consola de comandos:
   ```bash
   python main.py
   ```

---

## 5. Casos de Prueba Utilizados 🧪
El programa ejecuta un flujo continuo automatizado para demostrar los siguientes escenarios:

1.  **Caso Límite 1 (Control de Vacío / Underflow):** El sistema inicia vacío e intenta ejecutar la acción de atender un ticket. El programa controla la condición especial mostrando un mensaje informativo: `⚠️ AVISO [Cola Vacía]`.
2.  **Caso Normal (Llenado progresivo):** Se insertan de forma secuencial 10 tickets representativos con datos reales (ID, Nombre de usuario y descripción del fallo). Los punteros avanzan correctamente del índice 0 al 9.
3.  **Caso Límite 2 (Control de Desbordamiento / Overflow):** Con la cola llena (10/10), se intenta registrar un ticket número 11. El sistema bloquea la inserción de manera segura mostrando el mensaje: `❌ ERROR [Cola Llena]`.
4.  **Demostración de Circularidad:** Se atienden 2 tickets (liberando las posiciones físicas 0 y 1). Posteriormente, se ingresan 2 nuevos tickets. El programa demuestra el comportamiento circular al alojar estos nuevos registros en las posiciones iniciales liberadas, reutilizando la memoria de forma exacta.

---

## 6. Limitaciones Actuales y Posibles Mejoras 📈
*   **Limitación:** La capacidad fija de 10 elementos restringe el escalado en empresas grandes.
    *   *Mejora:* Implementar la cola utilizando **Nodos Enlazados (Listas Enlazadas)** para permitir un crecimiento dinámico de la memoria según la demanda.
*   **Limitación:** No existe un orden de criticidad; se atiende igual un olvido de contraseña que la caída del servidor principal.
    *   *Mejora:* Evolucionar la estructura hacia una **Cola de Prioridad (Priority Queue)** o un *Heap*, donde fallas críticas se ubiquen automáticamente al inicio de la fila.

---

## 7. Enlace al Video Explicativo 🎥
Puedes ver la sustentación completa de la actividad, la explicación del código y la demostración de los casos de prueba en el siguiente enlace:
👉 **[https://fumcc-my.sharepoint.com/:v:/g/personal/carloseduardorojasayala_fumc_edu_co/IQABYaUciRN2T7jxoScgjpPQAYjuLW5LzrSLBi9LDvnCs1o?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=vVzVLv]**
