from traffic_light import TrafficLight
from vehicle import Vehicle

class TrafficControlSystem:
    def __init__(self, lights):
        self.lights = lights
        self.current_green_light = lights[0]
        self.current_green_light.open_light()
        self.time_elapsed = 0
        self.default_green_time = 10
        self.max_green_time = 30
        self.yellow_time = 3
        self.priority_directions = ["north", "south"]

    def apply_rules(self):
        self.time_elapsed += 1

        if self.current_green_light:
            self.current_green_light.last_changed += 1
            if self.current_green_light.last_changed >= self.max_green_time:
                print(f"Semáforo {self.current_green_light.direction.upper()} ficou amarelo.")
                self.current_green_light.turn_yellow()
                self.current_green_light.last_changed = 0

            elif self.current_green_light.is_yellow and self.current_green_light.last_changed >= self.yellow_time:
                print(f"Semáforo {self.current_green_light.direction.upper()} fechou.")
                self.current_green_light.close_light()
                self.current_green_light.clear_vehicles()
                self.current_green_light = None

        if not self.current_green_light:
            self.choose_next_light()

    def choose_next_light(self):
        best_light = None
        max_waiting = 0
        for light in self.lights:
            waiting_count = light.get_waiting_vehicles_count()
            if light.direction in self.priority_directions:
                waiting_count += 2
            if waiting_count > max_waiting:
                max_waiting = waiting_count
                best_light = light

        if best_light:
            best_light.open_light()
            print(f"Semáforo {best_light.direction.upper()} abriu.")
            self.current_green_light = best_light

    def update_wait_times(self):
        for light in self.lights:
            if not light.is_green:
                for vehicle in light.waiting_vehicles:
                    vehicle.increment_wait_time()
