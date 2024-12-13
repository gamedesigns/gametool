import gradio as gr
from enemy import Enemy, load_enemies_from_json, save_enemies_to_json
from player import Player, Equipment, load_equipment_from_json, load_exp_curve_from_json
from combat import simulate_combat

# Load data from JSON files
enemies = load_enemies_from_json('enemies.json')
equipment_list = load_equipment_from_json('equipment.json')
exp_curve = load_exp_curve_from_json('exp_curve.json')

# Function to apply equipment to player
def apply_equipment(player, equipment):
    for eq in equipment:
        player.attack_damage += eq.bonus_attack_damage
        player.attack_speed += eq.bonus_attack_speed
        player.defense += eq.bonus_defense
    return player

# Function to simulate combat and return result
def fight(player_health, player_attack_damage, player_attack_speed, player_defense, *args):
    num_enemies = len(enemies)
    enemy_counts = args[:num_enemies]
    equipment_names = args[num_enemies]
    
    enemy_counts_dict = dict(zip([enemy.name for enemy in enemies], enemy_counts))
    
    # Create player with base stats
    player = Player(player_health, player_attack_damage, player_attack_speed, player_defense)
    
    # Apply selected equipment
    selected_equipment = [eq for eq in equipment_list if eq.name in equipment_names]
    player = apply_equipment(player, selected_equipment)
    
    # Choose enemies based on counts
    selected_enemies = []
    for enemy, count in enemy_counts_dict.items():
        for _ in range(count):
            selected_enemy = next((e for e in enemies if e.name == enemy), None)
            if selected_enemy:
                selected_enemies.append(selected_enemy)
    if not selected_enemies:
        raise ValueError("One or more enemies not found")
    
    # Simulate combat
    result, damage_to_player, damage_to_enemies, enemies_defeated, exp_gained = simulate_combat(player, selected_enemies)
    
    # If player wins, grant EXP
    if result == "Player wins":
        player.exp += exp_gained
        player.level_up(exp_curve)
        return f"{result}. Gained {exp_gained} EXP. Current EXP: {player.exp}. Level: {player.level}. Damage dealt: {damage_to_enemies}. Damage received: {damage_to_player}. Enemies defeated: {enemies_defeated}"
    else:
        return f"{result}. Damage received: {damage_to_player}"

# Function to add a new enemy
def add_enemy(name, health, attack_damage, attack_speed, defense, exp=0):
    new_enemy = Enemy(name, health, attack_damage, attack_speed, defense, exp)
    enemies.append(new_enemy)
    save_enemies_to_json('enemies.json', enemies)
    return "Enemy added successfully."

# Function to remove an enemy
def remove_enemy(name):
    global enemies
    enemies = [e for e in enemies if e.name != name]
    save_enemies_to_json('enemies.json', enemies)
    return f"Enemy {name} removed."

# Function to edit an enemy
def edit_enemy(name, new_name, health, attack_damage, attack_speed, defense, exp=0):
    global enemies
    for i, enemy in enumerate(enemies):
        if enemy.name == name:
            enemies[i].name = new_name
            enemies[i].health = health
            enemies[i].attack_damage = attack_damage
            enemies[i].attack_speed = attack_speed
            enemies[i].defense = defense
            enemies[i].exp = exp
            break
    save_enemies_to_json('enemies.json', enemies)
    return f"Enemy {name} edited."

# Gradio interface
with gr.Blocks() as iface:
    # Combat simulation interface
    enemy_count_sliders = []
    for enemy in enemies:
        slider = gr.Slider(0, 10, step=1, label=f"Number of {enemy.name}")
        enemy_count_sliders.append(slider)
    
    combat_interface = gr.Interface(
        fn=fight,
        inputs=[
            gr.Slider(1, 200, step=1, label="Player Health"),
            gr.Slider(1, 20, step=1, label="Player Attack Damage"),
            gr.Slider(0.5, 2, step=0.1, label="Player Attack Speed"),
            gr.Slider(1, 10, step=1, label="Player Defense"),
        ] + enemy_count_sliders + [
            gr.CheckboxGroup([eq.name for eq in equipment_list], label="Equipment")
        ],
        outputs="text",
        title="GameTool - Combat Simulator",
        description="Simulate combat between player and enemies with different equipment."
    )
    
    # Enemy management interface
    with gr.Tab("Manage Enemies"):
        with gr.Row():
            with gr.Column():
                name_input = gr.Textbox(label="Name")
                health_input = gr.Number(label="Health")
                attack_damage_input = gr.Number(label="Attack Damage")
                attack_speed_input = gr.Number(label="Attack Speed")
                defense_input = gr.Number(label="Defense")
                exp_input = gr.Number(label="EXP")
                add_btn = gr.Button("Add Enemy")
                add_btn.click(add_enemy, inputs=[name_input, health_input, attack_damage_input, attack_speed_input, defense_input, exp_input], outputs=gr.Label())
                
                name_remove_input = gr.Textbox(label="Name")
                remove_btn = gr.Button("Remove Enemy")
                remove_btn.click(remove_enemy, inputs=name_remove_input, outputs=gr.Label())
                
                name_edit_input = gr.Textbox(label="Current Name")
                new_name_input = gr.Textbox(label="New Name")
                health_edit_input = gr.Number(label="Health")
                attack_damage_edit_input = gr.Number(label="Attack Damage")
                attack_speed_edit_input = gr.Number(label="Attack Speed")
                defense_edit_input = gr.Number(label="Defense")
                exp_edit_input = gr.Number(label="EXP")
                edit_btn = gr.Button("Edit Enemy")
                edit_btn.click(edit_enemy, inputs=[name_edit_input, new_name_input, health_edit_input, attack_damage_edit_input, attack_speed_edit_input, defense_edit_input, exp_edit_input], outputs=gr.Label())

iface.launch()