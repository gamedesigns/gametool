import gradio as gr
from enemy import load_enemies_from_json, Enemy
from player import Player, Equipment, load_equipment_from_json
from combat import simulate_combat

# Load data from JSON files
enemies = load_enemies_from_json('enemies.json')
equipment_list = load_equipment_from_json('equipment.json')

# Function to apply equipment to player
def apply_equipment(player, equipment):
    for eq in equipment:
        player.health += eq.bonus_health
        player.attack_damage += eq.bonus_attack_damage
        player.attack_speed += eq.bonus_attack_speed
        player.defense += eq.bonus_defense
    return player

# Function to simulate combat and return result
def fight(player_health, player_attack_damage, player_attack_speed, player_defense,
          enemy_name, equipment_names):
    # Create player with base stats
    player = Player(player_health, player_attack_damage, player_attack_speed, player_defense)
    
    # Apply selected equipment
    selected_equipment = [eq for eq in equipment_list if eq.name in equipment_names]
    player = apply_equipment(player, selected_equipment)
    
    # Choose enemy
    enemy = next((e for e in enemies if e.name == enemy_name), None)
    if not enemy:
        raise ValueError("Unknown enemy")
    
    # Simulate combat
    result = simulate_combat(player, enemy)
    return result

# Gradio interface
iface = gr.Interface(
    fn=fight,
    inputs=[
        gr.Slider(1, 200, step=1, label="Player Health"),
        gr.Slider(1, 20, step=1, label="Player Attack Damage"),
        gr.Slider(0.5, 2, step=0.1, label="Player Attack Speed"),
        gr.Slider(1, 10, step=1, label="Player Defense"),
        gr.Radio([e.name for e in enemies], label="Enemy"),
        gr.CheckboxGroup([eq.name for eq in equipment_list], label="Equipment")
    ],
    outputs="text",
    title="GameTool - Combat Simulator",
    description="Simulate combat between player and enemies with different equipment."
)

iface.launch()