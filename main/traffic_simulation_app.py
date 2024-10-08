import tkinter as tk
import utils
import random

class TrafficSimulationApp:
    def __init__(self, root, control_system):
        self.root = root
        self.control_system = control_system
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        self.traffic_lights = {}
        self.vehicle_queues = {}
        self.setup_interface()

        self.quit_button = tk.Button(root, text="Encerrar Simulação", command=self.quit_simulation)
        self.quit_button.pack()

        self.update_simulation()

    """Configura a interface gráfica dos semáforos e suas posições."""
    def setup_interface(self):
        positions = {
            "north": (250, 200),
            "south": (250, 300),
            "east": (300, 250),
            "west": (200, 250)
        }
        for light in self.control_system.lights:
            x, y = positions[light.direction]
            color = "red" if not light.is_green else "green"
            self.traffic_lights[light.direction] = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
            self.vehicle_queues[light.direction] = []

    """Atualiza a simulação, aplicando regras e gerenciando veículos."""
    def update_simulation(self):
        self.control_system.apply_rules()
        self.control_system.update_wait_times()
        self.update_traffic_lights()
        self.update_vehicle_queues()

        # Gera novos veículos aleatoriamente
        if random.random() < 0.5: #50% de chance de gerar um veículo
            new_vehicle = utils.generate_random_vehicle()
            print(f"Veículo chegou na direção {new_vehicle.direction.upper()}.")
            for light in self.control_system.lights:
                if light.direction == new_vehicle.direction:
                    light.add_vehicle(new_vehicle)

        self.root.after(1000, self.update_simulation)

    """Atualiza a cor dos semáforos na interface gráfica."""
    def update_traffic_lights(self):
        for light in self.control_system.lights:
            color = "green" if light.is_green else "yellow" if light.is_yellow else "red"
            self.canvas.itemconfig(self.traffic_lights[light.direction], fill=color)

    """Atualiza a visualização das filas de veículos esperando no semáforo."""
    def update_vehicle_queues(self):
        queue_positions = {
            "north": (245, 165),
            "south": (245, 325),
            "east": (325, 245),
            "west": (165, 245)
        }
        offsets = {
            "north": (0, -20),
            "south": (0, 20),
            "east": (20, 0),
            "west": (-20, 0)
        }

        # Limpa as filas antigas de veículos
        for vehicles in self.vehicle_queues.values():
            for vehicle_id in vehicles:
                self.canvas.delete(vehicle_id)
        self.vehicle_queues = {key: [] for key in self.vehicle_queues}

        # Desenha as filas de veículos atualizadas
        for light in self.control_system.lights:
            pos_x, pos_y = queue_positions[light.direction]
            offset_x, offset_y = offsets[light.direction]

            # Se o semáforo estiver verde, remove todos os veículos da fila
            if light.is_green:
              for _ in range(len(light.waiting_vehicles)):
                vehicle_id = self.canvas.create_rectangle(
                  pos_x, pos_y,
                  pos_x + 10, pos_y + 10,
                  fill="blue"
                )
                self.root.after(50, lambda v_id=vehicle_id: self.canvas.delete(v_id))  # Remove rapidamente o veículo

              light.clear_vehicles()

            # Desenha os veículos restantes
            for i, vehicle in enumerate(light.waiting_vehicles):
                vehicle_id = self.canvas.create_rectangle(
                    pos_x + i * offset_x, pos_y + i * offset_y,
                    pos_x + i * offset_x + 10, pos_y + i * offset_y + 10,
                    fill="blue"
                )
                self.vehicle_queues[light.direction].append(vehicle_id)

    """Encerra a simulação."""
    def quit_simulation(self):
        self.root.destroy()