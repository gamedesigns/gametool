def simulate_combat(player, enemies_list, max_rounds=1000):
    total_damage_to_enemies = 0
    total_damage_to_player = 0
    enemies_defeated = 0
    
    for _ in range(max_rounds):
        # Player attacks one enemy (for simplicity, attacks the first alive enemy)
        target_enemy = next((e for e in enemies_list if e.health > 0), None)
        if target_enemy:
            damage_to_enemy = max(player.attack_damage - target_enemy.defense, 0)
            target_enemy.health -= damage_to_enemy
            total_damage_to_enemies += damage_to_enemy
        else:
            break  # All enemies defeated
        
        # Enemies attack player
        for enemy in enemies_list:
            if enemy.health > 0:
                damage_to_player = max(enemy.attack_damage - player.defense, 0)
                player.health -= damage_to_player
                total_damage_to_player += damage_to_player
                if player.health <= 0:
                    break  # Player defeated
        if player.health <= 0:
            break  # Exit the loop if player is defeated
    
    enemies_defeated = sum(1 for enemy in enemies_list if enemy.health <= 0)
    if player.health <= 0:
        exp_gained = 0  # Set exp_gained to 0 when player loses
    else:
        exp_gained = sum(enemy.exp for enemy in enemies_list if enemy.health <= 0)
    
    return ("Player wins" if player.health > 0 else "Enemies win"), total_damage_to_player, total_damage_to_enemies, enemies_defeated, exp_gained