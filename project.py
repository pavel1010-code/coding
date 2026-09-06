import random
import time

print("--WELCOME TO THE GAME!--")

player_name = ""
layer_hp = 100
max_hp = 100
player_damage_min = 10
player_damage_max = 20
potions = 3
gold = 0
victories = 0

enemies = [
    {"name": "Cave Rat", "hp": 30, "min_dmg": 3, "max_dmg": 8, "gold": 15},
    {"name": "Skeleton", "hp": 50, "min_dmg": 6, "max_dmg": 12, "gold": 30},
    {"name": "Ogre", "hp": 80, "min_dmg": 10, "max_dmg": 18, "gold": 60},
    {"name": "Dark knight", "hp": 120, "min_dmg": 15, "max_dmg": 25, "gold": 100}
]

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

    print("n-- SHOP --")
    print("Gold available:", gold)
    print("1) potion (25 gold)")
    print("2) Sword upgrade (+5 dmg) (50 gold)")
    print("3) Back")

    choice = input("Select option-- ")

    if choice == "1":
        if gold >= 25:
            gold -= 25:
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
        ("this command is not funcional.")