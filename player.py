class Player:
    def __init__(self, health, attack_damage, attack_speed, defense, exp=0, level=1):
        self.health = health
        self.attack_damage = attack_damage
        self.attack_speed = attack_speed
        self.defense = defense
        self.exp = exp
        self.level = level

    def level_up(self, exp_curve):
        levels = sorted(map(int, exp_curve.keys()))
        for level in levels:
            required_exp = exp_curve[str(level)]
            if self.exp < required_exp:
                self.level = level - 1
                break
        else:
            self.level = levels[-1]
        
        # Ensure level is at least 1
        if self.level < 1:
            self.level = 1
        
        # Adjust stats based on level
        base_health = 100
        base_attack_damage = 10
        base_defense = 5
        self.health = base_health + (self.level - 1) * 10
        self.attack_damage = base_attack_damage + (self.level - 1) * 5
        self.defense = base_defense + (self.level - 1) * 2

class Equipment:
    def __init__(self, name, type, bonus_attack_damage=0, bonus_defense=0, bonus_attack_speed=0):
        self.name = name
        self.type = type
        self.bonus_attack_damage = bonus_attack_damage
        self.bonus_defense = bonus_defense
        self.bonus_attack_speed = bonus_attack_speed

import json

def load_equipment_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Equipment(**eq) for eq in data['equipment']]

def load_exp_curve_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)