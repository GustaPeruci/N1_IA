import random

class Vehicle:
    def __init__(self, direction):
        self.direction = direction
        self.waiting_time = 0
        
    def increment_wait_time(self):
        """Incrementa o tempo de espera do veículo em 1 segundo."""
        self.waiting_time += 1

class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.is_green = False
        self.is_yellow = False
        self.waiting_vehicles = []
        self.last_changed = 0

    def open_light(self):
        """Abre o semáforo para a direção atual."""
        self.is_green = True
        self.is_yellow = False
        self.last_changed = 0

    def turn_yellow(self):
        """Muda o semáforo para amarelo."""
        self.is_green = False
        self.is_yellow = True

    def close_light(self):
        """Fecha o semáforo."""
        self.is_green = False
        self.is_yellow = False

    def add_vehicle(self, vehicle):
        """Adiciona um veículo à fila de espera do semáforo."""
        self.waiting_vehicles.append(vehicle)

    def clear_vehicles(self):
        """Remove todos os veículos da fila."""
        self.waiting_vehicles.clear()

    def get_waiting_vehicles_count(self):
        """Retorna a contagem de veículos esperando no semáforo."""
        return len(self.waiting_vehicles)

    def has_priority(self):
        """Verifica se a direção tem prioridade para abrir o semáforo."""
        return self.get_waiting_vehicles_count() > 3 and any(vehicle.waiting_time > 30 for vehicle in self.waiting_vehicles)
