def simulate_combat(player, enemy):
    player_turns_per_second = player.attack_speed
    enemy_turns_per_second = enemy.attack_speed

    while player.health > 0 and enemy.health > 0:
        # Player attacks enemy
        damage_to_enemy = max(player.attack_damage - enemy.defense, 0)
        enemy.health -= damage_to_enemy

        # Enemy attacks player
        damage_to_player = max(enemy.attack_damage - player.defense, 0)
        player.health -= damage_to_player

    if player.health <= 0:
        return "Enemy wins"
    else:
        return "Player wins"