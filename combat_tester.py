# Code for the entire simulation:

import random
import pprint
import math

# Define Attributes, Skills, Armor Types, Weapon Types, Wound Stages
ATTRIBUTES = ["Physique", "Fighting", "Precision", "Instincts", "Resolve", "Empathy", "Intellect"]

SKILLS = {
    "Physique": {
        "Advanced": ["Acrobatics"],
        "Simple": ["Athletics", "Strength"]
    },
    "Fighting": {
        "Advanced": [],
        "Simple": ["Heavy", "Fencing"]
    },
    "Precision": {
        "Advanced": ["Lockpicking"],
        "Simple": ["Shooting", "Throwing"]
    },
    "Instincts": {
        "Advanced": ["Picking pockets"],
        "Simple": ["Stealth", "Survival"]
    },
    "Intellect": {
        "Advanced": ["Arcane Theory", "Medicine"],
        "Simple": ["Learning", "Investigation"]
    },
    "Empathy": {
        "Advanced": [],
        "Simple": ["Deception", "Persuasion", "Handle animals"]
    }
}
ARMOR_TYPES = {
    "Leather Jacket": {"Armor": 3, "Hindrance": 1, "Load": 0},
    "Padded Jacket": {"Armor": 4, "Hindrance": 1, "Load": 0},
    "Hardened Leather": {"Armor": 3, "Hindrance": 0, "Load": 1},
    "Chain Mail": {"Armor": 4, "Hindrance": 0, "Load": 1},
    "Scale Mail": {"Armor": 5, "Hindrance": 1, "Load": 1},
    "Breastplate": {"Armor": 6, "Hindrance": 1, "Load": 2},
    "Splint Mail": {"Armor": 7, "Hindrance": 1, "Load": 2},
    "Full Plate": {"Armor": 8, "Hindrance": 1, "Load": 2},
}

WEAPON_TYPES = {
    "Small": {"Damage": 3, "Load": 0},
    "Simple": {"Damage": 3, "Load": 1},
    "Fencing": {"Damage": 4, "Load": 1},
    "Heavy": {"Damage": 4, "Load": 1},
    "2-handed": {"Damage": 6, "Load": 3},
    "Versatile": {"Damage": 5, "Load": 2},
}

WOUND_STAGES = ["Healthy", "Bleeding", "Battered", "Mauled", "Broken"]

# Define the Character and Combat classes

class Monster:
    def __init__(self, name, stamina, damage, attack_attributes, physical_difficulty=0, armor=0):
        self.name = name
        self.stamina = stamina
        self.damage = damage
        self.attack_attributes = attack_attributes
        self.physical_difficulty = physical_difficulty
        self.armor = armor

    def take_damage(self, damage, attacker):
        print(f"{self.name} takes {damage} damage from {attacker.name}!")
        damage -= self.armor
        self.stamina -= damage
        if self.stamina <= 0:
            print(f"{self.name} has been defeated!")
    
    def __str__(self):
        return f"{self.name}: Stamina: {self.stamina} | Armor: {self.armor} | Damage: {self.damage}"


class Character:
    def __init__(self, name, randomize=False, attributes=None, skills=None, armor=None, weapon=None):
        self.name = name
        if randomize:
            while True:
                self.attributes = {attr: random.randint(2, 7) for attr in ATTRIBUTES}
                if sum(self.attributes.values()) == 32:
                    break
            self.skills = {}
            for attr in SKILLS:
                for skill_type in SKILLS[attr]:
                    for skill in SKILLS[attr][skill_type]:
                        self.skills[skill] = 1 if random.choice([True, False]) else 0
            self.armor = random.choice(list(ARMOR_TYPES.keys()))
            self.weapon = random.choice(list(WEAPON_TYPES.keys()))
        else:
            self.attributes = attributes
            self.skills = skills
            self.armor = armor
            self.weapon = weapon
        
        self.wound_stage = 0
        self.stamina = self.attributes["Physique"] + self.attributes["Resolve"]

    def roll_test(self, attribute, help_count=0, hindrance_count=0):
        base_dice = [random.randint(1, 12), random.randint(1, 12)]
        
        # Replace dice based on help and hindrance counts
        for i in range(help_count):
            if base_dice:
                base_dice.pop()
                base_dice.append(random.randint(1, 10))
        for i in range(hindrance_count):
            if base_dice:
                base_dice.pop()
                base_dice.append(random.randint(1, 20))
        
        hits = sum([1 for die in base_dice if die <= self.attributes[attribute]])
        criticals = base_dice.count(1)
        complications = sum([1 for die in base_dice if die >= 12])
        
        return hits, criticals, complications, base_dice
    
    def take_damage(self, damage, attacker):
        print(f"{self.name} takes {damage} damage from {attacker.name}!")
        
        # Armor roll
        armor_roll = random.randint(1, 12)
        if armor_roll <= ARMOR_TYPES[self.armor]["Armor"]:
            damage -= armor_roll

            print(f"{self.name} soaks {ARMOR_TYPES[self.armor]['Armor']} damage with {self.armor}!")

        # Determine the amount of stamina to spend to minimize wound stages
        excess_damage = damage % 5  # Find out how much above the last multiple of 5 the damage is
        if excess_damage != 0:
            stamina_needed = excess_damage +1  # add one to the excess damage, to make sure damage is less than a multiple of 5, so the wound stage doesn't increase
        else:
            stamina_needed = 0

        # Spend the stamina, but ensure we don't spend more stamina than we have or need
        stamina_spent = min(self.stamina, stamina_needed, damage)
        self.stamina -= stamina_spent
        damage -= stamina_spent
        print(f"{self.name} soaks {stamina_spent} damage with stamina!")

        # Calculate wound stages
        if damage > 0:
            self.wound_stage += 1
            if damage >= 5:
                self.wound_stage += math.floor(damage/5)
            if self.wound_stage > 4:
                self.wound_stage = 4
            print(f"{self.name} took {damage} damage, advances wound stage, now {WOUND_STAGES[self.wound_stage]}!")

        if self.wound_stage >= 4:
            print(f"{self.name} was Broken by {attacker.name}!")

    
    def __str__(self):
        attr_str = ', '.join([f"{attr[:3]}: {self.attributes[attr]}" for attr in ATTRIBUTES])
        return f"{self.name}: {attr_str} | Armor: {self.armor} | Weapon: {self.weapon} | Wound: {WOUND_STAGES[self.wound_stage]} | Stamina: {self.stamina}"


class CombatWithSides:
    def __init__(self, characters, monsters):
        self.characters = characters
        self.monsters = monsters

    def check_combat_over(self):
        monsters_alive = [monster for monster in self.monsters if monster.stamina > 0]
        characters_alive = [character for character in self.characters if character.wound_stage < 4]
        return len(monsters_alive) == 0 or len(characters_alive) == 0
    
    def left_alive(self):
        monsters_alive = [monster for monster in self.monsters if monster.stamina > 0]
        characters_alive = [character for character in self.characters if character.wound_stage < 4]
        return monsters_alive + characters_alive

    def monsters_alive(self):
        return [monster for monster in self.monsters if monster.stamina > 0]
    
    def characters_alive(self):
        return [character for character in self.characters if character.wound_stage < 4]

    def start_round(self):
        turn_order = self.left_alive()
        random.shuffle(turn_order)
        for entity in turn_order:
            if isinstance(entity, Character):
                self.take_turn(entity, self.monsters_alive())
            else:
                self.take_turn(entity, self.characters_alive())
    
    def take_turn(self, attacker, defenders):
        if defenders:
            target = random.choice(defenders)
            if isinstance(attacker, Character):
                for i in range(0,2):
                    hits, criticals, complications, dice = attacker.roll_test(
                        "Fighting", hindrance_count=target.physical_difficulty if target.physical_difficulty>=0 else 0, help_count=target.physical_difficulty if target.physical_difficulty<0 else 0)
                    print(f"{attacker.name} attacks {target.name} with dice: {dice}")
                    if hits:
                        damage = WEAPON_TYPES[attacker.weapon]["Damage"]
                        if criticals:
                            edge_points = 2 * criticals + hits - criticals
                            damage += edge_points
                        target.take_damage(damage, attacker)
            else:
                # Monster attacking, character defending
                chosen_attribute = random.choice(attacker.attack_attributes)
                hits, criticals, complications, dice = target.roll_test(
                    chosen_attribute, hindrance_count=attacker.physical_difficulty if attacker.physical_difficulty>=0 else 0, help_count=attacker.physical_difficulty if attacker.physical_difficulty<0 else 0)
                print(f"{target.name} defends against {attacker.name} using {chosen_attribute} with dice: {dice}")
                edge_points = 0
                if complications:
                    edge_points = 2 * complications
                if not hits:
                    target.take_damage(attacker.damage+edge_points, attacker)
    
    def get_combat_status(self):
        return [str(entity) for entity in self.characters + self.monsters]


attributes = {
    "Physique": 5,
    "Fighting": 6,
    "Precision": 4,
    "Instincts": 5,
    "Resolve": 5,
    "Empathy": 4,
    "Intellect": 4
}

{"Physique": 5, "Fighting": 5, "Precision": 4, "Instincts": 5, "Resolve": 5, "Empathy": 4, "Intellect": 4}

skills = []

armor = "Padded Jacket"

weapon = "Fencing"

# Running the simulation with 3 characters

# Characters for testing system
opthero = Character("OptimizedHero", attributes={"Physique": 6, "Fighting": 8, "Precision": 2, "Instincts": 6, "Resolve": 6, "Empathy": 3, "Intellect": 2}, skills=skills, armor="Chain Mail", weapon="Versatile")
char1 = Character("Hero", attributes=attributes, skills=skills, armor=armor, weapon=weapon)
char2 = Character("Sidekick", attributes=attributes, skills=skills, armor=armor, weapon=weapon)
char3 = Character("Sidepunch", attributes=attributes, skills=skills, armor=armor, weapon=weapon)
monster1 = Monster("Armored Knight", 15, 7, ["Fighting", "Instincts"], 1, 2)
monster2 = Monster("Bandit", 5, 5, ["Physique", "Instincts"], 0, 1)
monster3 = Monster("Bandit2", 5, 5, ["Physique", "Instincts"], 0, 1)
monster4 = Monster("Dragon", 30, 13, ["Physique", "Instincts"], 2, 3)
monster5 = Monster("Demon Prince", 30, 13, ["Physique", "Instincts"], 2, 3)

# Testing combat system

test_res = []

for i in range(0, 100):
    # Create new instances of Character and Monster for each combat
    #opthero = Character("OptimizedHero", attributes={"Physique": 6, "Fighting": 8, "Precision": 2, "Instincts": 6, "Resolve": 6, "Empathy": 3, "Intellect": 2}, skills=skills, armor="Chain Mail", weapon="Versatile")
    #opthero2 = Character("OptimizedHero", attributes={"Physique": 6, "Fighting": 8, "Precision": 2, "Instincts": 6, "Resolve": 6, "Empathy": 3, "Intellect": 2}, skills=skills, armor="Chain Mail", weapon="Versatile")
    #opthero3 = Character("OptimizedHero", attributes={"Physique": 6, "Fighting": 8, "Precision": 2, "Instincts": 6, "Resolve": 6, "Empathy": 3, "Intellect": 2}, skills=skills, armor="Chain Mail", weapon="Versatile")
    opthero = Character("AvgHero", attributes=attributes, skills=skills, armor=armor, weapon=weapon)
    opthero2 = Character("AvgHero", attributes=attributes, skills=skills, armor=armor, weapon=weapon)
    opthero3 = Character("AvgHero", attributes=attributes, skills=skills, armor=armor, weapon=weapon)
    #opthero = Character("BadHero", attributes={"Physique": 3, "Fighting": 3, "Precision": 6, "Instincts": 4, "Resolve": 3, "Empathy": 7, "Intellect": 7}, skills=skills, armor="Padded Jacket", weapon="Versatile")
    #opthero2 = Character("BadHero", attributes={"Physique": 3, "Fighting": 3, "Precision": 6, "Instincts": 4, "Resolve": 3, "Empathy": 7, "Intellect": 7}, skills=skills, armor="Padded Jacket", weapon="Versatile")
    #opthero3 = Character("BadHero", attributes={"Physique": 3, "Fighting": 3, "Precision": 6, "Instincts": 4, "Resolve": 3, "Empathy": 7, "Intellect": 7}, skills=skills, armor="Padded Jacket", weapon="Versatile")
    monster1 = Monster("Armored Knight", 15, 7, ["Fighting", "Instincts"], 1, 2)
    monster2 = Monster("Armored Knight", 15, 7, ["Fighting", "Instincts"], 1, 2)
    monster3 = Monster("Bandit", 5, 5, ["Physique", "Instincts"], 0, 1)
    combat = CombatWithSides([opthero], [monster1])
    rounds = 0
    while combat.check_combat_over() == False:
        combat.start_round()
        pprint.pprint("Round ended!")
        rounds += 1

    pprint.pprint(f"Combat ended after {rounds} rounds!")
    pprint.pprint("Left alive were:")
    for entity in combat.left_alive():
        #pprint.pprint(str(entity))
        test_res.append(entity.name)

from collections import Counter

# Count the occurrences of each entity in the test_res list
counts = Counter(test_res)

# Calculate the percentage of each entity
total_tests = len(test_res)
percentages = {entity: count/total_tests*100 for entity, count in counts.items()}

# Print the percentages
for entity, percentage in percentages.items():
    print(f"{entity}: {percentage:.2f}%")

