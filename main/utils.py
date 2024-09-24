import random
from vehicle import Vehicle

def generate_random_vehicle():
    directions = ["north", "south", "east", "west"]
    return Vehicle(random.choice(directions))

def generate_report(control_system):
    report = ""
    for light in control_system.lights:
        report += f"Semáforo {light.direction.upper()}: {'Aberto' if light.is_green else 'Fechado'}\n"
        report += f"Veículos esperando: {light.get_waiting_vehicles_count()}\n"
        for vehicle in light.waiting_vehicles:
            report += f"- Veículo esperando por {vehicle.waiting_time} segundos\n"
        report += "\n"
    return report
