import json

class Player:
    def __init__(self, health, attack_damage, attack_speed, defense):
        self.health = health
        self.attack_damage = attack_damage
        self.attack_speed = attack_speed
        self.defense = defense

class Equipment:
    def __init__(self, name, type, bonus_health=0, bonus_attack_damage=0, bonus_attack_speed=0, bonus_defense=0):
        self.name = name
        self.type = type
        self.bonus_health = bonus_health
        self.bonus_attack_damage = bonus_attack_damage
        self.bonus_attack_speed = bonus_attack_speed
        self.bonus_defense = bonus_defense

def load_equipment_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [Equipment(**eq) for eq in data['equipment']]