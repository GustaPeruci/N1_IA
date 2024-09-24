class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.is_green = False
        self.is_yellow = False
        self.waiting_vehicles = []
        self.last_changed = 0

    def open_light(self):
        self.is_green = True
        self.is_yellow = False
        self.last_changed = 0

    def turn_yellow(self):
        self.is_green = False
        self.is_yellow = True

    def close_light(self):
        self.is_green = False
        self.is_yellow = False

    def add_vehicle(self, vehicle):
        self.waiting_vehicles.append(vehicle)

    def clear_vehicles(self):
        self.waiting_vehicles.clear()

    def get_waiting_vehicles_count(self):
        return len(self.waiting_vehicles)
