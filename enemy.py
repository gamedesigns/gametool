import json

class Enemy:
    def __init__(self, name, health, attack_damage, attack_speed, defense, exp=0):
        self.name = name
        self.health = health
        self.attack_damage = attack_damage
        self.attack_speed = attack_speed
        self.defense = defense
        self.exp = exp

def load_enemies_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [Enemy(**enemy) for enemy in data['enemies']]

def save_enemies_to_json(file_path, enemies):
    data = {'enemies': [enemy.__dict__ for enemy in enemies]}
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)