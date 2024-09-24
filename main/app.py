import time
import tkinter as tk
from vehicle import Vehicle
from traffic_light import TrafficLight
from traffic_control_system import TrafficControlSystem
from traffic_simulation_app import TrafficSimulationApp
import utils
import random

def main():
    root = tk.Tk()
    root.title("Simulação de Trânsito Inteligente")

    lights = [TrafficLight("north"), TrafficLight("south"), TrafficLight("east"), TrafficLight("west")]
    control_system = TrafficControlSystem(lights)

    app = TrafficSimulationApp(root, control_system)

    root.mainloop()

if __name__ == "__main__":
    main()
