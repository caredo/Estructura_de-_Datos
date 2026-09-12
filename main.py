class Ticket:
    def __init__(self, id_ticket: int, usuario: str, falla: str):
        self.id_ticket = id_ticket
        self.usuario = usuario
        self.falla = falla

    def __str__(self):
        return f"[Ticket #{self.id_ticket}] {self.usuario}: '{self.falla}'"


class ColaMesaAyuda:
    def __init__(self, capacidad: int):
        self.capacidad = capacidad
        self.vector = [None] * capacidad  # Arreglo estático inicializado con tamaño fijo
        self.frente = 0
        self.final = -1
        self.tamano_actual = 0

    def esta_llena(self) -> bool:
        return self.tamano_actual == self.capacidad

    def esta_vacia(self) -> bool:
        return self.tamano_actual == 0

    def registrar_ticket(self, ticket: Ticket) -> bool:
        """Operación Enqueue (Insertar en la cola)"""
        if self.esta_llena():
            print(f"❌ ERROR [Cola Llena]: No se pudo registrar el ticket de {ticket.usuario}. Capacidad máxima alcanzada.")
            return False
        
        # Aritmética modular para lograr el movimiento circular del puntero 'final'
        self.final = (self.final + 1) % self.capacidad
        self.vector[self.final] = ticket
        self.tamano_actual += 1
        print(f"✅ Ticket #{ticket.id_ticket} encolado para {ticket.usuario} (Posición física vector: {self.final}).")
        return True

    def atender_ticket(self) -> Ticket:
        """Operación Dequeue (Retirar de la cola)"""
        if self.esta_vacia():
            print("⚠️ AVISO [Cola Vacía]: No hay tickets pendientes en la mesa de ayuda.")
            return None
        
        ticket_atendido = self.vector[self.frente]
        self.vector[self.frente] = None  # Liberamos explícitamente la celda en memoria
        
        print(f"🔧 [Atendiendo] Ticket #{ticket_atendido.id_ticket} de {ticket_atendido.usuario} removido del frente (Posición: {self.frente}).")
        
        # Aritmética modular para avanzar el puntero 'frente' de forma circular
        self.frente = (self.frente + 1) % self.capacidad
        self.tamano_actual -= 1
        return ticket_atendido

    def mostrar_cola(self):
        """Imprime el estado actual del vector y el orden lógico de los tickets"""
        if self.esta_vacia():
            print("📭 La cola de la mesa de ayuda está vacía.")
            return
        print(f"\n--- ESTADO DE LA COLA ({self.tamano_actual}/{self.capacidad} ocupados) ---")
        indice = self.frente
        for i in range(self.tamano_actual):
            print(f" -> Posición en fila {i+1}: {self.vector[indice]}")
            indice = (indice + 1) % self.capacidad
        print("--------------------------------------------------\n")


# === EJECUCIÓN CONTINUA DE LOS CASOS DE PRUEBA (Para demostración en el video) ===
if __name__ == "__main__":
    # Inicialización de la mesa de ayuda con capacidad fija para 10 tickets
    soporte = ColaMesaAyuda(capacidad=10)

    print("=== CASO LÍMITE 1: CONTROL DE VACÍO (UNDERFLOW) ===")
    soporte.atender_ticket()

    print("\n=== CASO NORMAL: LLENADO DE LA COLA ===")
    usuarios_ejemplo = [
        ("Carlos Pérez", "Pantalla azul"), 
        ("Ana Gómez", "Fallo de conexión VPN"), 
        ("Luis Martínez", "Impresora atascada en contabilidad"), 
        ("Marta Ruiz", "Clave de red bloqueada"),
        ("Jorge Torres", "Equipo sin acceso a internet"), 
        ("Lucía Villamil", "Instalar software de desarrollo"),
        ("Andrés Quintana", "Teclado dañado"), 
        ("Elena Mendoza", "El audio no funciona en Teams"),
        ("Pedro Suárez", "Correo institucional bloqueado"), 
        ("Sofía Borja", "Lentitud extrema en el sistema ERP")
    ]
    
    id_actual = 101
    for usuario, falla in usuarios_ejemplo:
        soporte.registrar_ticket(Ticket(id_actual, usuario, falla))
        id_actual += 1

    soporte.mostrar_cola()

    print("=== CASO LÍMITE 2: CONTROL DE DESBORDAMIENTO (OVERFLOW) ===")
    # Intentamos registrar el ticket número 11 con la estructura al límite
    soporte.registrar_ticket(Ticket(111, "Ramón Valdés", "El computador de escritorio no enciende"))

    print("\n=== LIBERACIÓN Y DEMOSTRACIÓN DE CIRCULARIDAD ===")
    # El técnico atiende y procesa los 2 primeros tickets de la fila (libera índices físicos 0 y 1)
    soporte.atender_ticket()
    soporte.atender_ticket()
    
    soporte.mostrar_cola()

    print("=== REUTILIZACIÓN DE MEMORIA EN ACCIÓN ===")
    # Al quedar 2 espacios disponibles, la cola aloja los nuevos tickets al principio del vector
    soporte.registrar_ticket(Ticket(111, "Ramón Valdés", "El computador de escritorio no enciende"))
    soporte.registrar_ticket(Ticket(112, "Inés Jaramillo", "Monitor parpadea constantemente"))
    
    soporte.mostrar_cola()
