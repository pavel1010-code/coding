import random
import time
import json

print("--WELCOME TO THE GAME!--")

player_name = ""
player_hp = 100
max_hp = 100
player_damage_min = 10
player_damage_max = 20
potions = 3
gold = 0
victories = 0
armor = 0

enemies = [
    {"name": "Cave Rat", "hp": 30, "min_dmg": 3, "max_dmg": 8, "gold": 15},
    {"name": "Skeleton", "hp": 50, "min_dmg": 6, "max_dmg": 12, "gold": 30},
    {"name": "Ogre", "hp": 80, "min_dmg": 10, "max_dmg": 18, "gold": 60},
    {"name": "Dark knight", "hp": 120, "min_dmg": 15, "max_dmg": 25, "gold": 100}
]

materials = {
    "wood": 5,
    "iron": 3,
    "leather": 2,
    "magic_dust": 1
}

recipes = {
    "Iron Sword": {"wood": 2, "iron": 5, "gold": 50, "result_dmg": 10},
    "Heavy Armor": {"iron": 8, "leather": 5, "gold": 100, "result_armor": 5},
    "Super potion": {"magic_dust": 2, "gold": 30}
}

def craft_item():
    global gold, player_damage_min, player_damage_max, armor, potions

    print("\n--- CRAFTING WORKBENCH ---")
    print(f"Material -> Wood: {materials['wood']} | Iron: {materials['iron']} | Leather: {materials['leather']} | Magic Dust: {materials['magic_dust']}")
    print(f"Gold: {gold}")
    print("1) Craft Iron Sword (Requires: 2 wood, 5 iron, 50 gold) -> +10 Min/Max Damage")
    print("2) Craft Heavy Armor (Requires: 8 iron, 5 leather, 100 gold) -> +5 Armor")
    print("3) Craft Super Potion (Requires: 2 magic dust, 30 gold) -> Restores / +1 Potion")
    print("4) Leave workbench")

    choice = input("Select crafting option: ")

    if choice == "1":
        req = recipes["Iron Sword"]
        if materials["wood"] >= req["wood"] and materials["iron"] >= req["iron"] and gold >= req["gold"]:
            materials["wood"] -= req["wood"]
            materials["iron"] -= req["iron"]
            gold -= req["gold"]
            player_damage_min += req["result_dmg"]
            player_damage_max += req["result_dmg"]
            print("\n[SUCCESS] You forged a might Iron Sword!")
        else:
            print("\n[ERROR] Not enought materials or gold!")

    elif choice == "2":
        req = recipes["Heavy Armor"]
        if materials["iron"] >= req["iron"] and materials["leather"] >= req["leather"] and gold >= req["gold"]:
            materials["iron"] -= req["iron"]
            materials["leather"] -= req["leather"]
            gold -= req["gold"]
            armor += req["result_armor"]
            print("\n[SUCCESS] You crafted Heavy Armor! Defense increased.")
        else:
            print("\n[ERROR] Not enought materials or gold!")
    elif choice == "4":
        print("Leaving workbench...")

    elif choice == "3":
        req = recipes["Super potion"]
        if materials["magic_dust"] >= req["magic_dust"] and gold >= req["gold"]:
            materials["magic_dust"] -= req["magic_dust"]
            gold -= req["gold"]
            potions += 1
            print("\n[SUCCESS] You brewed a powerful Super potion!")
        else:
            print("\n[ERROR] Not enought materials or gold!")
    
    else:
        print("Invalid choice.")

def heal():
    global player_hp, potions

    if potions > 0:
        potions -= 1
        player_hp += 35
        if player_hp > max_hp:
            player_hp = max_hp
        print("\nYou drank a potion! HP restored.")
    else:
        print("\nNO potions left!")

def shop():
    global gold, potions, player_damage_min, player_damage_max

    print("\n-- SHOP --")
    print("Gold available:", gold)
    print("1) potion (25 gold)")
    print("2) Sword upgrade (+5 dmg) (50 gold)")
    print("3) Back")

    choice = input("Select option-- ")

    if choice == "1":
        if gold >= 25:
            gold -= 25
            potions += 1
            print("Bought 1 potion.")
        else:
            print("Not enough gold!")
    elif choice == "2":
        if gold >= 50:
            gold -= 50
            player_damage_min += 5
            player_damage_max += 5
            print("Sword upgrade!")
        else:
            print("Not enought gold!")
    elif choice == "3":
        print("Leaving shop ... ")
    else:
        print("this command is not funcional.")

def fight(enemy_data):
    global player_hp, max_hp, gold, victories, armor
    global heavy_strike_cd, shield_bash_cd, fireball_cd

    enemy_name = enemy_data["name"]
    enemy_hp = enemy_data["hp"]

    print(f"\nWatch out! A {enemy_name} appeared!")
    time.sleep(1)

    while enemy_hp > 0 and player_hp > 0:
        print(f"\n{enemy_name} HP : {enemy_hp}")
        print(f"Your HP: {player_hp}")
        print("1. Attack")
        print("2. Drink Potion")
        print("3. Run away")

        if heavy_strike_cd == 0:
            print("4. Heavy Strike (READY)")
        else:
            print(f"4. Heavy srtike (Cooldown: {heavy_strike_cd} turns)")

        if shield_bash_cd == 0:
            print("5. Shield Bash (READY)")
        else:
            print(f"5. Shield Bash (Cooldows: {shield_bash_cd} turns)")

        if fireball_cd == 0:
            print("6. Fireball (READY)")
        else:
            print(f"6. Fireball (Cooldown: {fireball_cd} turns)")

        action = input("Action: ")

        if action == "1":

            base_dmg = random.randint(player_damage_min, player_damage_max)
            is_crit = random.randint(1, 100) <= 15

            if is_crit:
                dmg = base_dmg * 2
                print(f"\n CRITICAL HIT! You struck {enemy_name} fiercely for {dmg} damage!")
            else:
                dmg = base_dmg
                print(f"\nYou hit {enemy_name} for {dmg} damage!")
            enemy_hp -= dmg

            if enemy_hp > 0:
                e_dmg = random.randint(enemy_data["min_dmg"], enemy_data["max_dmg"])
                actual_dmg = max(1, e_dmg - armor)
                player_hp -= actual_dmg
                print(f"{enemy_name} hit you back for {actual_dmg} HP!")

        elif action == "2":
            heal()

            e_dmg = random.randint(enemy_data["min_dmg"], enemy_data["max_dmg"])
            actual_dmg = max(1, e_dmg - armor)
            player_hp -= actual_dmg
            print(f"{enemy_name} attacked while you were healing for {actual_dmg} HP!")

        elif action == "3":
            if random.randint(1,100) > 50:
                print("\nYou escaped successfully!")

                if enemy_name in ["DJUNGLE DRAGON (BOSS), THE ANCIENT KING"]:
                    enemy_data["hp"] = enemy_hp


                return
            else:
                print("\nFailed to escape! Enemy gets a free hit.")
                e_dmg = random.randint(enemy_data["min_dmg"], enemy_data["max_dmg"])
                actual_dmg = max(1, e_dmg - armor)
                player_hp -= actual_dmg
                print(f"{enemy_name} hit you for {actual_dmg} HP!")
        elif action == "4":
            if heavy_strike_cd == 0:
                base_dmg = random.randint(player_damage_min, player_damage_max)
                is_crit = random.randint(1, 100) <= 30

                if is_crit:
                    dmg = int(base_dmg * 2.5)
                    print(f"\n BRUTAL CRITICAL HEAVY STRIKE! YOu smashed {enemy_name} for {dmg} damage!")
                else:
                    dmg = int(base_dmg * random.uniform(1.5, 2.0))
                    print(f"\n HEAVY STRIKE! You smashed {enemy_name} for {dmg} damage!")

                enemy_hp -= dmg
                heavy_strike_cd = 3

                if enemy_hp > 0:
                    e_dmg = random.randint(enemy_data["min_dmg"], enemy_data["max_dmg"])
                    actual_dmg = max(1, e_dmg - armor)
                    player_hp -= actual_dmg
                    print(f"{enemy_name} hit you back for {actual_dmg} HP!")
            else:
                print(f"\nHeavy Strike is on cooldown! ({heavy_strike_cd} turns left)")
                continue

        elif action == "5":
            if shield_bash_cd == 0:
                dmg = random.randint(player_damage_min // 2, player_damage_min)
                enemy_hp -= dmg
                shield_bash_cd = 4
                print(f"\nSHIELD BASH! You hit {enemy_name} for {dmg} damage and weakened their attack!")

                if enemy_hp > 0:
                    e_dmg = random.randint(enemy_data["min_dmg"], enemy_data["max_dmg"])
                    actual_dmg = max(1, e_dmg - armor)
                    player_hp -= actual_dmg
                    print(f"{enemy_name} dealt a wakened attack for only {actual_dmg} HP!")
            else:
                print(f"\nShieald Bash is on coolddown! ({shield_bash_cd} turns left)")
                continue
        elif action == "6":
            if fireball_cd == 0:
                dmg = random.randint(25, 45)
                enemy_hp -= dmg
                fireball_cd = 3
                print(f"\nFIREBALL! YOU hurlde a massive flame at {enemy_name} for {dmg} magic damage!")

                if enemy_hp > 0:
                    e_dmg = random.randint(enemy_data["min_dmg"], enemy_data["max_dmg"])
                    actual_dmg = max(1, e_dmg - armor)
                    player_hp -= actual_dmg
                    print(f"{enemy_name} hit you back for {actual_dmg} HP!")
            else:
                print(f"\nFireball is on cooldown! ({fireball_cd} turns left)")
                continue            

        else:
            print("Unknown action, skipped turn!")

        if action in ["1", "2", "4", "5", "6"]:
            if heavy_strike_cd > 0:
                heavy_strike_cd -= 1
            if shield_bash_cd > 0:
                shield_bash_cd -= 1
            if fireball_cd > 0:
                fireball_cd -= 1

        time.sleep(0.5)

    if player_hp < 0:
        player_hp = 0

    if enemy_name in ["DJUNGLE DRAGON (BOSS), THE ANCIENT KING"]:
        enemy_data["hp"] = enemy_hp

    if player_hp <= 0:
        print("\nYou died in combat...")
    else:
        print(f"\nYOu defeated {enemy_name}!")
        gold += enemy_data["gold"]
        victories += 1
        print(f"Earned {enemy_data['gold']} gold.")

        update_quests(enemy_name)
        check_achievements()

        if random.randint(1, 100) >= 25:
            max_hp += 10
            player_hp += 10
            print("RARE DROP! You found a Magic Amulet! Max HP permanently increased by 10!")


def print_stats():
    print(f"\nHero: {player_name}")
    print(f"HP: {player_hp}/{max_hp} | Potions: {potions} | Gold: {gold} | Victories: {victories}")


def main():
    global player_name

    print("=== DUNGAON GAME ===")
    player_name = input("Enter hero name: ").strip()
    if player_name == "":
        player_name = "Dragon Knight"

    running = True

    while running and player_hp > 0:
        print_stats()
        print("What do you want to do?")
        print("1. Hunt monsters")
        print("2. Go to shop")
        print("3. Drink potion")
        print("4. Exit game")

        choice = input("Choice: ")

        if choice == "1":

            if victories < 2:
                selected_enemy = enemies[0]
            elif victories < 4:
                selected_enemy = random.choice(enemies[:2])
            elif victories < 7:
                selected_enemy = random.choice(enemies[1:3])
            else:
                selected_enemy = random.choice(enemies)

            fight(selected_enemy)

        elif choice == "2":
            shop()
        elif choice == "3":
            heal()
        elif choice == "4":
            print("\nThanks for playing! Goodbye.")
            running = False
        else:
            print("Invalid input.")
    if player_hp <= 0:
        print(f"\nGame Over! Total victories: {victories}")

player_level = 1
player_xp = 0
xp_to_next_level = 50
armor = 0
heavy_strike_cd = 0
shield_bash_cd = 0
fireball_cd = 0

boss_monster = {
    "name": "DJUNGLE DRAGON (BOSS)",
    "hp": 250,
    "min_dmg": 20,
    "max_dmg": 35,
    "gold": 500,
    "xp": 200
}

game_completed = False
final_boss_unlocked = False

final_boss = {
    "name": "THE ANCIENT KING",
    "hp": 500,
    "min_dmg": 25,
    "max_dmg": 40,
    "gold": 1000,
    "xp": 500
}

def add_xp(amount):
    global player_xp, player_level, xp_to_next_level, max_hp, player_hp, player_damage_min, player_damage_max

    player_xp += amount
    print(f"\n[XP] Gained {amount} XP! ({player_xp}/{xp_to_next_level})")

    while player_xp >= xp_to_next_level:
        player_level += 1
        player_xp -= xp_to_next_level
        xp_to_next_level = int(xp_to_next_level * 1.5)

        max_hp += 20
        player_hp = max_hp
        player_damage_min += 3
        player_damage_max += 5

        print("\n" + "*" * 40)
        print(f"---LEVEL UP--- You are now level {player_level}!")
        print(f"---MAX HP--- INcreased to {max_hp} (Fully healed)")
        print(f"---Attack increased to {player_damage_min}-{player_damage_max}---")
        print("*" * 40)

def buy_armor():
    global gold, armor

    print("\n---Armor smith ---")
    print(f"Current armor: {armor}")
    print("1) Leather armor (+2 Defense) - 40 Gold")
    print("2) Iron Plate (+5 Defense) - 100 gold")
    print("3) Back")

    choice = input("Select aromor: ")
    if choice == "1":
        if gold >= 40:
            gold -= 40
            armor += 2
            print("Brought Leather Armor!")
        else:
            print("Not enought gold!")
    elif choice == "2":
        if gold >= 100:
            gold -= 100
            armor += 5
            print("Bought Iron Plate!")
        else:
            print("Not enought gold!")

def save_game():
    data = {
        "player_name": player_name,
        "player_hp": player_hp,
        "max_hp": max_hp,
        "player_damage_min": player_damage_min,
        "player_damage_max": player_damage_max,
        "potions": potions,
        "gold": gold,
        "victories": victories,
        "armor": armor,

        "player_level": player_level,
        "player_xp": player_xp,
        "xp_to_next_level": xp_to_next_level,

        "heavy_strike_cd": heavy_strike_cd,
        "shield_bash_cd": shield_bash_cd,
        "fireball_cd": fireball_cd,

        "boss_monster": boss_monster,
        "final_boss": final_boss,

        "quests": quests,
        "achievements": achievements,

        "treasures_found": treasures_found,
        "materials": materials,

        "game_completed": game_completed,
        "final_boss_unlocked": final_boss_unlocked
    }

    with open("savegame.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\n" + "=" * 45)
    print("[GAME SAVED SUCCEFULLY!]")
    print("=" * 45)

def load_game():
    global player_name, player_hp, max_hp
    global player_damage_min, player_damage_max
    global potions, gold, victories, armor
    global player_level, player_xp, xp_to_next_level
    global heavy_strike_cd, shield_bash_cd, fireball_cd
    global boss_monster, final_boss
    global quests, achievements
    global treasures_found, materials
    global game_completed, final_boss_unlocked

    try:
        with open("savegame.json", "r") as f:
            data = json.load(f)


        player_name = data["player_name"]
        player_hp = data["player_hp"]
        max_hp = data["max_hp"]
        player_damage_min = data["player_damage_min"]
        player_damage_max = data["player_damage_max"]
        potions = data["potions"]
        gold = data["gold"]
        victories = data["victories"]
        armor = data["armor"]

        player_level = data["player_level"]
        player_xp = data["player_xp"]
        xp_to_next_level = data["xp_to_next_level"]

        heavy_strike_cd = data["heavy_strike_cd"]
        shield_bash_cd = data["shield_bash_cd"]
        fireball_cd = data["fireball_cd"]

        boss_monster = data["boss_monster"]
        final_boss = data["final_boss"]

        quests = data["quests"]
        achievements = data["achievements"]

        treasures_found = data["treasures_found"]
        materials = data["materials"]

        game_completed = data["game_completed"]
        final_boss_unlocked = data["final_boss_unlocked"]

        print("\n" + "=" * 45)
        print("[GAME LOADED SUCCESSFULLY]")
        print(f"Welcome back, {player_name}!")
        print(f"Level: {player_level}")
        print(f"Gold: {gold}")
        print(f"Victories: {victories}")
        print("=" * 45)

        return True

    except FileNotFoundError:
        print("\n[NO SAVE FILE FOUND!]")
        return False

    except (KeyError, json.JSONDecodeError):
        print("\n[ERROR] Save file is corrupted or incompatible.")
        return False


def print_expanded_stats():
    print_stats()
    print(f"Level: {player_level} | XP: {player_xp}/{xp_to_next_level} | Armor Defense: {armor}")

def boss_fight():
    global boss_monster, gold, final_boss_unlocked

    if boss_monster["hp"] <= 0:
        print("\nThe dungeon Dragon has already been defeared!")
        return

    print("\n" + "!" * 55)
    print("              THE DRAGON'S LAIR")
    print("!" * 55)

    print("\nA massive roarr shakes the intire dungeon.")
    time.sleep(1)

    print("The dungeon Dragon emerges from the darkness.")
    time.sleep(1)

    print("\nDragon: \"You have come far, little warrior.\"")
    print("Dragon: \"But this dungeon will be your grave.\"")
    time.sleep(1)

    print("\nPrepare yourself...")
    time.sleep(1)

    fight(boss_monster)

    if player_hp <= 0:
        return

    if boss_monster["hp"] <= 0:

        print("\n" + "=" * 55)
        print("              THE DRAGON HAS FALLEN")
        print("=" * 55)

        print("\nthe dragon lets out one final roar.")
        time.sleep(1)

        print("Its enormous body crashes onto the dungeon floor.")
        time.sleep(1)

        print("the entire dungeon begins to shake.")
        time.sleep(1)

        print("\nYou have defeated the Dungeon Dragon.")
        print("But something feels wrong...")
        time.sleep(2)

        print("\nA strange red ight appears beneath teh dragon.")
        time.sleep(1)

        print("Ancient symbols being glowing across the walls.")
        time.sleep(1)

        print("\nYou hear a voice from deep beneath the dungeon:")
        print("\nThe dragon was never teh master...\"")
        time.sleep(2)

        print("\n\"It was quardian.\"")
        time.sleep(2)

        final_boss_unlocked = True
        save_game()


        print("\n" + "*" * 55)
        print("              NEW OBJECTIVE UNLOCKED")
        print("The true master of the dungeon has awakened.")
        print("Find the Ancient Chamber.")
        print("*" * 55)

        add_xp(boss_monster["xp"])

        if not achievements["Dragon Slayer"]:
            achievements["Dragon Slayer"] = True

            print("\n[ACHIEVEMENT UNLOCKED]")
            print("Dragon Slayer - Defeat the Dungeon Dragon!")
            print("Reward: +500 gold")

            gold += 500

def tavern():
    global gold
    print("\n --- THE LUCKY BOAR TAVERN ---")
    print(f"Your gold: {gold}")
    print("1) Play Dice Gamble (Double or nothing)")
    print("2) Leave tavern")

    choice = input("Choose: ")
    if choice == "1":
        if gold < 10:
            print("You need at least 10 gold to play!")
            return

        try:
            bet = int(input("Enter how much gold you want to bet: "))
            if 0 < bet <= gold:
                print("Rolling dice...")
                time.sleep(1)
                player_roll = random.randint(1, 6) + random.randint(1,6)
                dealer_roll = random.randint(1, 6) + random.randint(1, 6)

                print(f"Your roll: {player_roll} | Dealer's roll: {dealer_roll}")

                if player_roll > dealer_roll:
                    gold += bet
                    print(f"You won! Doubled your bet. Current gold: {gold}")
                elif player_roll < dealer_roll:
                    gold -= bet
                    print(f"You lost! Dealer wins. Current gold: {gold}")
                else:
                    print("It's a draw! Your gold is returned.")
            else:
                print("invalid bet amount!")
        except ValueError:
            print("PLease enter a valid number!")
    elif choice == "2":
        print("Leaving the tavern...")

def final_boss_fight():
    global final_boss, gold, game_completed

    if game_completed:
        print("\n" + "=" * 55)
        print("              THE GAME IS ALREADY COMPLETE")
        print("=" * 55)
        print("\nYou have already defeated the Ancient King.")
        print("The world is safe.")
        return

    if not final_boss_unlocked:
        print("\nThe Acient Chamber is sealed.")
        print("You must defeat the dungeon Dragon first.")
        return

    if final_boss["hp"] <= 0:
        print("\nThe Ancient King has already been defeated.")
        return

    print("\n" + "#" * 60)
    print("#" + " " * 58 + "#")
    print("#               THE ANCIENT CHAMBER")
    print("#" * 60)

    time.sleep(1)

    print("\nYou enter a gigantic underground chamber.")
    time.sleep(1)

    print("Thousands of ancient statues surround you.")
    time.sleep(1)

    print("At the center stands an enormous black throne.")
    time.sleep(2)

    print("\nSomeone is sitting on it.")
    time.sleep(2)

    print("\nAncient King: \"So... the dragon has fallen.\"")
    time.sleep(2)

    print("Ancient king: \"I have waited centuries for someone strong enough.\"")
    time.sleep(2)

    print("\nThe Ancient King slowly rises form his throne.")
    time.sleep(1)

    print("Ancient King: \"Show me what you are capable of.\"")
    time.sleep(2)

    fight(final_boss)

    if player_hp <= 0:
        return

    if final_boss["hp"] <= 0:

        print("\n" + "#" * 60)
        print("#" + " " * 58 + "#")
        print("#             THE FINAL BATTLE IS OVER")
        print("#" + " " * 58 + "#")
        print("#" * 60)

        time.sleep(2)

        print("The darkness surrounding the chamber begins to disappear.")
        time.sleep(1)

        print("The ancient statues crumble.")
        time.sleep(1)

        print("Light enters the dungeon for the first time in centuries.")
        time.sleep(2)

        print("\nAncient King:")
        print("\"You have done what no warrior before you could do.\"")
        time.sleep(2)

        print("\"You are the new guardian of this world.\"")
        time.sleep(2)

        print("\nThe Ancient King disappears into the light.")
        time.sleep(2)

        add_xp(final_boss["xp"])

        game_completed = True
        save_game()

        print("\n" + "=" * 60)
        print("                 GAME COMPLETED")
        print("=" * 60)

        print("\nYou defeated the Dungeon Dragon.")
        print("You defeated the Ancient King.")
        print("You survived the dungeon.")
        print("\nThe world is finally safe.")

        print("\n" + "*" * 60)
        print("                  CONGRATULATIONS!")
        print("*" * 60)

        print(f"\nFinal Hero: {player_name}")
        print(f"Final Level: {player_level}")
        print(f"Final Victories: {victories}")
        print(f"Final Gold: {gold}")
        print(f"Final Treasures: {treasures_found}")

        print("\nYour adventure is complete.")
        print("=" * 60)

    else:
        print("\nThe Ancient King survives.")
        print("You will have to return and finish the battle.")
        print(f"His remaining HP: {final_boss['hp']}")


quests = [
    {
        "name": "Rat Extermination",
        "description": "Defeat 3 Cave Rats.",
        "target": 3,
        "progress": 0,
        "reward_gold": 50,
        "reward_xp": 40,
        "completed": False
    },
    {
        "name": "Skeleton Hunter",
        "description": "Defeat 3 Sheletons.",
        "target": 3,
        "progress": 0,
        "reward_gold": 100,
        "reward_xp": 75,
        "completed": False
    },
    {
        "name": "Ogre Slayer",
        "description": "defeat 2 Orges.",
        "target": 2,
        "progress": 0,
        "reward_gold": 150,
        "reward_xp": 100,
        "completed": False
    }
]

achievements = {
    "First Blood": False,
    "Rich Hero": False,
    "Monster Hunter": False,
    "Treasure Hunter": False,
    "Survivor": False,
    "Dragon Slayer": False
}

treasures_found = 0

def show_quest():
    print("\n" + "=" * 45)
    print("              QUEST LOG")
    print("=" * 45)

    for current_quest in quests:
        if current_quest["completed"]:
            status = "[COMPLETED]"
        else:
            status = f"[{current_quest['progress']}/{current_quest['target']}]"

        print(f"\n{current_quest['name']} {status}")
        print(f"  {current_quest['description']}")
        print(f"  Reward: {current_quest['reward_gold']} gold + {current_quest['reward_xp']} XP")

    print("\n" + "=" * 45)
    
def check_achievements():
    global gold, victories, treasures_found

    if victories >= 1 and not achievements["First Blood"]:
        achievements["First Blood"] = True
        print("\n[ACHIEVEMENT UNLOCKED]")
        print("First blood - Defeat your first monster!")
        print("Reward: +25 gold")
        gold += 25

    if gold >= 500 and not achievements["Rich Hero"]:
        achievements["Rich Hero"] = True
        print("\n[ACHIEVEMENT UNLOCKED]")
        print("Rich Hero - collect 500 gold!")
        print("Reward: +100 gold")
        gold += 100

    if victories >= 10 and not achievements["Monster Hunter"]:
        achievements["Monster Hunter"] = True
        print("\n[ACHIEVEMENT UNLOCKED]")
        print("Monster Hunter - defeat 10 monsters!")
        print("Reward: +150 XP")
        add_xp(150)

    if treasures_found >= 3 and not achievements["Treasure Hunter"]:
        achievements["Treasure Hunter"] = True
        print("\n[ACHIEVEMENT UNLOCKED]")
        print("Treasure Hunter - Find 3 treasures!")
        print("Reward: +200 gold")
        gold += 200

    if player_hp <= 20 and victories >= 5 and not achievements["Survivor"]:
        achievements["Survivor"] = True
        print("\n[ACHIEVEMENT UNLOCKED]")
        print("Survivor - Survive after reaching critical health!")
        print("Reward: +50 gold")
        gold += 50

def update_quests(enemy_name):
    global gold

    for current_quest in quests:
        if current_quest["completed"]:
            continue

        if "Cave Rat" in enemy_name and current_quest["name"] == "Rat Extermination":
            current_quest["progress"] += 1

        elif "Skeleton" in enemy_name and current_quest["name"] == "Skeleton Hunter":
            current_quest["progress"] += 1

        elif "Ogre" in enemy_name and current_quest["name"] == "Ogre Slayer":
            current_quest["progress"] += 1

        if current_quest["progress"] >= current_quest["target"]:
            current_quest["progress"] = current_quest["target"]
            current_quest["completed"] = True

            print("\n" + "*" * 45)
            print("QUEST COMPLETED!")
            print(f"{current_quest['name']}")
            print(f"Reward: {current_quest['reward_gold']} gold")
            print(f"Reward: {current_quest['reward_xp']} XP")
            print("*" * 45)

            gold += current_quest["reward_gold"]
            add_xp(current_quest["reward_xp"])

def treasure_hunt():
    global gold, potions, treasures_found, player_hp

    print("\n" + "=" * 45)
    print("              Treasure Hunt")
    print("=" * 45)

    print("YOu entered an ancient abandoned area...")
    time.sleep(1)

    event = random.randint(1, 6)

    if event == 1:
        print("\nYou found nothing but old bones.")
        time.sleep(1)

    elif event == 2:
        found_gold = random.randint(30, 80)
        gold += found_gold
        treasures_found += 1

        print("\nTREAASURE FOUND!")
        print(f"YOu discovered {found_gold} gold!")
        time.sleep(1)

    elif event == 3:
        potions += 2
        treasures_found += 1

        print("\nYou found a hidden chest!")
        print("Inside were 2 healing potions!")
        time.sleep(1)

    elif event == 4:
        bonus_hp = random.randint(10, 30)
        player_hp += bonus_hp

        if player_hp > max_hp:
            player_hp = max_hp

        print("\nA magical fountain was hidden underground!")
        print(f"You restored {bonus_hp} HP.")
        time.sleep(1)

    elif event == 5:
        found_gold = random.randint(80, 100)
        gold += found_gold
        treasures_found += 1

        print("\nRARE TREASURE!")
        print(f"You opened a golden chest containing {found_gold} gold!")
        time.sleep(1)

    elif event == 6:
        print("\nYou discovered a cursed chest!")
        print("You try to open it anyway...")

        time.sleep(1)

        curse_damage = random.randint(10,30)
        player_hp -= curse_damage

        if player_hp < 0:
            player_hp = 0

        print(f"The curse dealt {curse_damage} damage!")

    check_achievements()

def show_achievements():
    print("\n" + "=" * 45)
    print("               ACHIEVEMENTS")
    print("=" * 45)

    unlocked = 0

    for name, completed in achievements.items():
        if completed:
            print(f"[UNLOCKED] {name}")
            unlocked += 1
        else:
            print(f"[locked]   {name}")

    print("-" * 45)
    print(f"Achievements unlocked: {unlocked}/{len(achievements)}")
    print("=" * 45)

def character_info():
    print("\n" + "=" * 45)
    print("               CHARACTER INFO")
    print("=" * 45)

    print(f"Name:         {player_name}")
    print(f"Level:        {player_level}")
    print(f"XP:           {player_xp}/{xp_to_next_level}")
    print(f"HP:           {player_hp}/{max_hp}")
    print(f"Damage:       {player_damage_min}-{player_damage_max}")
    print(f"Armor:        {armor}")
    print(f"Potions:      {potions}")
    print(f"Gold:         {gold}")
    print(f"Victories:    {victories}")
    print(f"Treasures:    {treasures_found}")

    print("=" * 45)

def random_world_event():
    global gold,potions, player_hp

    print("\nYou continue exploring the dangerous wordld...")
    time.sleep(1)

    event = random.randint(1, 5)

    if event == 1:
        print("\nA traveling merchant approaches you.")
        print("He gives you a free potion.")

        potions += 1

    elif event == 2:
        bonus_gold = random.randint(10, 50)
        gold += bonus_gold

        print("\nYou found some gold lying on the road!")
        print(f"You collected {bonus_gold} gold.")

    elif event == 3:
        damage = random.randint(5, 15)
        player_hp -= damage

        print("\nA group of bats attacked you!")
        print(f"You lost {damage} HP.")

        if player_hp < 0:
            player_hp = 0
        
    elif event == 4:
        heal_amount = random.randint(10, 25)
        player_hp += heal_amount

        if player_hp > max_hp:
            player_hp = max_hp

        print("\nYou discoevered a peaceful healing spring.")
        print(f"You recovered {heal_amount} HP.")

    else:
        print("\nThe area is strangely quiet...")
        print("You hear something moving in the darkness.")

    time.sleep(1)

def training_ground():
    global player_damage_min, player_damage_max, armor, gold

    print("\n" + "=" * 45)
    print("              TRAINING GROUND")
    print("=" * 45)

    print("You an train your combat skills here.")
    print(f"Gold: {gold}")
    print()
    print("1) Strength training - 75 gold")
    print("2) Defense training - 75 gold")
    print("3) Leave")

    choice = input("Choose training: ")

    if choice == "1":
        if gold >= 75:
            gold -= 75
            player_damage_min += 2
            player_damage_max += 2

            print("\nYou trained your swordsmaship!")
            print("Damage increased by +2")
        else:
            print("\nNot enough gold!")

    elif choice == "2":
        if gold >= 75:
            gold -= 75
            armor += 1

            print("\nYou trained your defensive skills!")
            print("Armor increased by +1.")
        else:
            print("\nNot enough gold!")

    elif choice == "3":
        print("Leaving training ground...")

    else:
        print("Invalid choice.")

def adventure_menu():
    while True:
        print("\n" + "=" * 45)
        print("               ADVENTURES")
        print("=" * 45)

        print("1. Search for treasure")
        print("2. Explore the wilderness")
        print("3. Visit training groud")
        print("4. View quests")
        print("5. View achievements")
        print("6. Character information")
        print("7. Leave")

        choice = input("Adventure choice: ")

        if choice == "1":
            treasure_hunt()

        elif choice == "2":
            random_world_event()

        elif choice == "3":
            training_ground()

        elif choice == "4":
            show_quest()

        elif choice == "5":
            show_achievements()

        elif choice == "6":
            character_info()

        elif choice == "7":
            print("Leaving the adventure manu...")
            break
            
        else:
            print("Invalid choice.")


def expanded_main():
    global player_name, gold, potions, player_hp
    global game_completed

    print("\n" + "=" * 55)
    print("           DUNGAON GAME")
    print("            FINAL EDITION")
    print("=" * 55)

    print("\n1. New Game")
    print("2. Load Game")
    print("3. Exit")

    start_choice = input("\nChoose: ")

    if start_choice == "1":
        player_name = input("\nEnter hero name: ").strip()

        if player_name == "":
            player_name = "Dragon Knight"

        print(f"\nWelcome, {player_name}!")
        print("Your adventure begins...")
        time.sleep(1)

    elif start_choice == "2":
        if not load_game():
            print("\nStarting a new game instead...")
            time.sleep(1)

            player_name = input("\nEnter hero name: ").strip()

            if player_name == "":
                player_name = "Dragon Knight"

    elif start_choice == "3":
        print("\nThanks for playing!")
        return

    else:
        print("\nInvalid choice.")
        return

    if game_completed:
        print("\n" + "=" * 55)
        print("              GAME COMPLETED")
        print("=" * 55)
        print("\nWelcome back, legendary hero.")
        print("You have already completed the main story.")
        print("You can continue exploring the world.")
        print("=" * 55)

    game_running = True

    while game_running and player_hp > 0:

        print_expanded_stats()

        print("\nWhat do you want to do?")
        print("1. Hunt Monsters")
        print("2. Go to Shop")
        print("3. Visit Armor Smith")
        print("4. Visit Tavern")
        print("5. Drink Potion")
        print("6. Fight the Dungeon Dragon")
        print("7. Enter the Ancient Chamber")
        print("8. Adventures")
        print("9. Save Game")
        print("10. Load Game")
        print("11. Exit Game")

        choice = input("\nChoice: ")

        if choice == "1":

            event_roll = random.choices(
                [0, 1, 2, 3],
                weights=[60, 15, 15, 10],
                k=1
            )[0]

            if event_roll == 0:

                old_victories = victories

                if victories < 2:
                    selected_enemy = enemies[0]

                elif victories < 4:
                    selected_enemy = random.choice(enemies[:2])

                elif victories < 7:
                    selected_enemy = random.choice(enemies[1:3])

                else:
                    selected_enemy = random.choice(enemies)

                fight(selected_enemy)

                if victories > old_victories:
                    add_xp(25)

            elif event_roll == 1:

                found_gold = random.randint(20, 70)
                gold += found_gold

                print("\n" + "~" * 35)
                print(f"Lucky Find!")
                print(f"You discovered {found_gold} gold!")
                print("~" * 35)

                time.sleep(1)

            elif event_roll == 2:

                potions += 1

                print("\n" + "~" * 35)
                print("Discovery!")
                print("You found a healing potion!")
                print("~" * 35)

                time.sleep(1)

            elif event_roll == 3:

                trap_dmg = random.randint(10, 25)
                player_hp -= trap_dmg

                if player_hp < 0:
                    player_hp = 0

                print("\n" + "!" * 35)
                print("TRAP!")
                print(f"You took {trap_dmg} damage!")
                print("!" * 35)

                time.sleep(1)

        elif choice == "2":
            shop()

        elif choice == "3":
            buy_armor()

        elif choice == "4":
            tavern()

        elif choice == "5":
            heal()

        elif choice == "6":
            boss_fight()

        elif choice == "7":
            final_boss_fight()

            if game_completed:
                print("\nThe main story has been completed.")
                print("You may continue exploring the world.")
                print("The game will remain open.")

        elif choice == "8":
            adventure_menu()

        elif choice == "9":
            save_game()

        elif choice == "10":
            load_game()

        elif choice == "11":
            print("\nThanks for playing!")
            print("Your adventure will be waiting for you.")
            game_running = False

        else:
            print("\nInvalid input.")

    if player_hp <= 0:
        print("\n" + "=" * 50)
        print("                 GAME OVER")
        print("=" * 50)
        print(f"\nHero: {player_name}")
        print(f"Victories: {victories}")
        print(f"Level: {player_level}")
        print("\nYour journey has ended...")
        print("=" * 50)

if __name__ == "__main__":
    expanded_main()