import random
from vehicle import Vehicle

def generate_random_vehicle():
    directions = ["north", "south", "east", "west"]
    return Vehicle(random.choice(directions))