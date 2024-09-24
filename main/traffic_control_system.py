from traffic_light import TrafficLight

class TrafficControlSystem:
    def __init__(self, lights):
        self.lights = lights
        self.current_green_light = lights[0]  # Começa com o primeiro semáforo
        self.current_green_light.open_light()  # Abre o semáforo inicial
        self.max_green_time = 15  # Tempo máximo para o sinal verde
        self.yellow_time = 1  # Tempo que o sinal ficará amarelo

    """Aplica as regras do semáforo e gerencia a mudança de sinal."""
    def apply_rules(self):
        if self.current_green_light:
            self.current_green_light.last_changed += 1

            # Se o tempo máximo de verde for atingido, muda para amarelo
            if self.current_green_light.last_changed >= self.max_green_time:
                print(f"Semáforo {self.current_green_light.direction.upper()} ficou amarelo.")
                self.current_green_light.turn_yellow()
                self.current_green_light.last_changed = 0  # Reinicia o contador

            # Se estiver amarelo por tempo suficiente, fecha o semáforo
            elif self.current_green_light.is_yellow and self.current_green_light.last_changed >= self.yellow_time:
                print(f"Semáforo {self.current_green_light.direction.upper()} fechou.")
                self.current_green_light.close_light()
                self.current_green_light.clear_vehicles()
                self.current_green_light = None

        # Se não há semáforo verde, escolhe o próximo
        if not self.current_green_light:
            self.choose_next_light()

    """Escolhe o próximo semáforo a abrir baseado em regras de prioridade."""
    def choose_next_light(self):
        best_light = None
        max_waiting = 0

        for light in self.lights:
            waiting_count = light.get_waiting_vehicles_count()
            if light.has_priority():
                waiting_count += 2  # Aumenta a contagem se a direção tem prioridade
            
            if waiting_count > max_waiting:
                max_waiting = waiting_count
                best_light = light

        # Abre o semáforo selecionado
        if best_light:
            best_light.open_light()
            print(f"Semáforo {best_light.direction.upper()} abriu.")
            self.current_green_light = best_light

    """Atualiza o tempo de espera de todos os veículos nos semáforos."""
    def update_wait_times(self):
        for light in self.lights:
            if not light.is_green:
                for vehicle in light.waiting_vehicles:
                    vehicle.increment_wait_time()
