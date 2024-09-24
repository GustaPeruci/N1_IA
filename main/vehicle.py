class Vehicle:
    def __init__(self, direction):
        self.direction = direction
        self.waiting_time = 0
        
    def increment_wait_time(self):
        """Incrementa o tempo de espera do veículo em 1 segundo."""
        self.waiting_time += 1