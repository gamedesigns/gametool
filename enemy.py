import json

class Enemy:
    def __init__(self, name, health, attack_damage, attack_speed, defense):
        self.name = name
        self.health = health
        self.attack_damage = attack_damage
        self.attack_speed = attack_speed
        self.defense = defense  # Added defense attribute

def load_enemies_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [Enemy(**enemy) for enemy in data['enemies']]