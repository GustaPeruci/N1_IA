import random

class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.is_green = False
        self.is_yellow = False
        self.waiting_vehicles = []
        self.last_changed = 0

    """Abre o semáforo para a direção atual."""
    def open_light(self):
        self.is_green = True
        self.is_yellow = False
        self.last_changed = 0

    """Muda o semáforo para amarelo."""
    def turn_yellow(self):
        self.is_green = False
        self.is_yellow = True

    """Fecha o semáforo."""
    def close_light(self):
        self.is_green = False
        self.is_yellow = False

    """Adiciona um veículo à fila de espera do semáforo."""
    def add_vehicle(self, vehicle):
        self.waiting_vehicles.append(vehicle)

    """Remove todos os veículos da fila."""
    def clear_vehicles(self):
        self.waiting_vehicles.clear()

    """Retorna a contagem de veículos esperando no semáforo."""
    def get_waiting_vehicles_count(self):
        return len(self.waiting_vehicles)

    """Verifica se a direção tem prioridade para abrir o semáforo."""
    def has_priority(self):
        return self.get_waiting_vehicles_count() > 3 and any(vehicle.waiting_time > 30 for vehicle in self.waiting_vehicles)
