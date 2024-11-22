import enums
import random
import string

STAT_BASE = 20
WOLF_BASE_STRENGTH = 40
WOLF_BASE_AGILITY = 20
RABBIT_BASE_STRENGTH = 20
RABBIT_BASE_AGILITY = 30

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Animal:
    def __init__(self,  strength=STAT_BASE, agility=STAT_BASE):
        self.energy = 50
        self.sex = enums.randomize()
        self.age = 0
        self.strength = strength
        self.agility = agility
        self.fatigue = 0
        self.breeding = 5
        self.name = id_generator()

    def is_dead(self):
        return True if self.energy <= 0 else False
    
    def increase_age(self, amount=1):
        self.age += amount
        self.breeding = max(0, self.breeding - amount)

    def __str__(self):
        return "Energy: {0}\nSex: {1}\nAge: {2}\nStrength: {3}\nAgility: {4}\nFatigue: {5}".format(self.energy, self.sex, self.age, self.strength, self.agility, self.fatigue)

class Rabbit(Animal):
    def __init__(self, strength=RABBIT_BASE_STRENGTH, agility=RABBIT_BASE_AGILITY):
        super().__init__(strength, agility)

    def eat_grass(self, grass, amount=10):
        self.energy += grass.eaten(amount)

    def tire(self, amount=5):
        self.energy -= amount

    def __str__(self):
        return f"Name: {self.name}, Sex: {self.sex}, Strength: {self.strength}, Agility: {self.agility}, Energy: {self.energy}"

class Wolf(Animal):
    def __init__(self, strength=WOLF_BASE_STRENGTH, agility=WOLF_BASE_AGILITY):
        super().__init__(strength, agility)
