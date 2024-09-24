class Vehicle:
    def __init__(self, direction):
        self.direction = direction
        self.waiting_time = 0
        
    def increment_wait_time(self):
        self.waiting_time += 1
