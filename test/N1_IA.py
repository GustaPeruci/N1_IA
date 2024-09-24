import time
import random
import tkinter as tk

class Vehicle:
    def __init__(self, direction):
        self.direction = direction
        self.waiting_time = 0  
        
    def increment_wait_time(self):
        self.waiting_time += 1

# Classe para os semáforos
class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.is_green = False
        self.is_yellow = False  # Adiciona estado amarelo
        self.waiting_vehicles = []  
        self.last_changed = 0  

    def open_light(self):
        self.is_green = True
        self.is_yellow = False  # Reseta o estado amarelo
        self.last_changed = 0

    def turn_yellow(self):
        self.is_green = False
        self.is_yellow = True  # Ativa o estado amarelo

    def close_light(self):
        self.is_green = False
        self.is_yellow = False  # Reseta o estado amarelo

    def add_vehicle(self, vehicle):
        self.waiting_vehicles.append(vehicle)

    def clear_vehicles(self):
        self.waiting_vehicles.clear()

    def get_waiting_vehicles_count(self):
        return len(self.waiting_vehicles)

# Sistema de Controle de Tráfego
class TrafficControlSystem:
    def __init__(self, lights):
        self.lights = lights
        self.current_green_light = lights[0]  
        self.current_green_light.open_light()
        self.time_elapsed = 0
        self.default_green_time = 10  
        self.max_green_time = 30  
        self.yellow_time = 3  # Tempo que o sinal ficará amarelo
        self.priority_directions = ["north", "south"]  

    def apply_rules(self):
        self.time_elapsed += 1

        if self.current_green_light:
            self.current_green_light.last_changed += 1

            # Fecha o semáforo se o tempo máximo foi atingido
            if self.current_green_light.last_changed >= self.max_green_time:
                print(f"Semáforo {self.current_green_light.direction.upper()} ficou amarelo.")
                self.current_green_light.turn_yellow()
                self.current_green_light.last_changed = 0  # Reinicia o contador

            # Fecha o semáforo amarelo após o tempo especificado
            elif self.current_green_light.is_yellow and self.current_green_light.last_changed >= self.yellow_time:
                print(f"Semáforo {self.current_green_light.direction.upper()} fechou.")
                self.current_green_light.close_light()
                self.current_green_light.clear_vehicles()
                self.current_green_light = None

        if not self.current_green_light:
            self.choose_next_light()

    def choose_next_light(self):
        # Prioridade para direções com maior número de veículos ou maior tempo de espera
        best_light = None
        max_waiting = 0

        for light in self.lights:
            waiting_count = light.get_waiting_vehicles_count()

            # Regras de prioridade: se a direção está entre as prioritárias, favorece essa direção
            if light.direction in self.priority_directions:
                waiting_count += 2  # Adiciona peso para direções prioritárias

            # Seleciona o semáforo com mais veículos ou com maior tempo de espera
            if waiting_count > max_waiting:
                max_waiting = waiting_count
                best_light = light

        # Abre o semáforo selecionado
        if best_light:
            best_light.open_light()
            print(f"Semáforo {best_light.direction.upper()} abriu.")

            self.current_green_light = best_light

    def update_wait_times(self):
        # Aumenta o tempo de espera dos veículos
        for light in self.lights:
            if not light.is_green:
                for vehicle in light.waiting_vehicles:
                    vehicle.increment_wait_time()

# Função para simular novos veículos chegando
def generate_random_vehicle():
    directions = ["north", "south", "east", "west"]
    return Vehicle(random.choice(directions))

# Interface gráfica com Tkinter
class TrafficSimulationApp:
    def __init__(self, root, control_system):
        self.root = root
        self.control_system = control_system
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        self.traffic_lights = {}
        self.vehicle_queues = {}
        self.setup_interface()

        # Botão para encerrar a simulação
        self.quit_button = tk.Button(root, text="Encerrar Simulação", command=self.quit_simulation)
        self.quit_button.pack()

        # Timer para atualizar a simulação
        self.update_simulation()

    def setup_interface(self):
        # Configura semáforos na interface
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

    def update_simulation(self):
        # Aplica as regras do sistema de controle e atualiza os tempos de espera
        self.control_system.apply_rules()
        self.control_system.update_wait_times()
        self.update_traffic_lights()
        self.update_vehicle_queues()

        # Simula novos veículos chegando de forma aleatória
        if random.random() < 0.5:  # 50% de chance de um novo veículo aparecer
            new_vehicle = generate_random_vehicle()
            print(f"Veículo chegou na direção {new_vehicle.direction.upper()}.")
            for light in self.control_system.lights:
                if light.direction == new_vehicle.direction:
                    light.add_vehicle(new_vehicle)

        self.root.after(1000, self.update_simulation)  # Atualiza a cada 1 segundo

    def update_traffic_lights(self):
        # Atualiza a cor dos semáforos na interface
        for light in self.control_system.lights:
            if light.is_green:
                color = "green"
            elif light.is_yellow:
                color = "yellow"  # Define a cor amarela
            else:
                color = "red"
            self.canvas.itemconfig(self.traffic_lights[light.direction], fill=color)

    def update_vehicle_queues(self):
      # Atualiza a fila de veículos na interface
      queue_positions = {
          "north": (245, 165),  # Posição inicial dos veículos
          "south": (245, 325),
          "east": (325, 245),
          "west": (165, 245)
      }
      offsets = {
          "north": (0, -20),  # Aumenta y para veículos do norte
          "south": (0, 20),  # Diminui y para veículos do sul
          "east": (20, 0),  # Diminui x para veículos do east
          "west": (-20, 0)    # Aumenta x para veículos do oeste
      }

      # Limpa as filas antigas
      for vehicles in self.vehicle_queues.values():
          for vehicle_id in vehicles:
              self.canvas.delete(vehicle_id)
      self.vehicle_queues = {key: [] for key in self.vehicle_queues}

      # Desenha as filas de veículos atualizadas
      for light in self.control_system.lights:
          pos_x, pos_y = queue_positions[light.direction]
          offset_x, offset_y = offsets[light.direction]

          # Se o semáforo estiver verde, remove todos os carros
          if light.is_green:
              light.clear_vehicles()

          # Desenha os veículos restantes
          for i, vehicle in enumerate(light.waiting_vehicles):
              # Corrige a posição dos veículos acumulando corretamente
              vehicle_id = self.canvas.create_rectangle(
                  pos_x + i * offset_x, pos_y + i * offset_y,
                  pos_x + i * offset_x + 10, pos_y + i * offset_y + 10,
                  fill="blue"
              )
              self.vehicle_queues[light.direction].append(vehicle_id)

    def quit_simulation(self):
        # Encerra a simulação e gera o relatório
        report = generate_report(self.control_system)
        print(report)
        self.root.destroy()

# Função para gerar o relatório de estado dos semáforos e veículos
def generate_report(control_system):
    report = ""
    for light in control_system.lights:
        report += f"Semáforo {light.direction.upper()}: {'Aberto' if light.is_green else 'Fechado'}\n"
        report += f"Veículos esperando: {light.get_waiting_vehicles_count()}\n"
        for vehicle in light.waiting_vehicles:
            report += f"- Veículo esperando por {vehicle.waiting_time} segundos\n"
        report += "\n"
    return report

# Função principal para rodar a simulação
def main():
    root = tk.Tk()
    root.title("Simulação de Trânsito Inteligente")

    # Cria os semáforos
    lights = [TrafficLight("north"), TrafficLight("south"), TrafficLight("east"), TrafficLight("west")]

    # Sistema de controle
    control_system = TrafficControlSystem(lights)

    # Interface gráfica
    app = TrafficSimulationApp(root, control_system)

    # Inicia a interface Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()