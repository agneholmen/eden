import enums
import random

STAT_BASE = 20
WOLF_BASE_STRENGTH = 40
WOLF_BASE_AGILITY = 20
RABBIT_BASE_STRENGTH = 20
RABBIT_BASE_AGILITY = 30

class Animal:
    def __init__(self,  strength=STAT_BASE, agility=STAT_BASE):
        self.energy = 50
        self.sex = enums.randomize()
        self.age = 0
        self.strength = strength
        self.agility = agility
        self.fatigue = 0

    def __str__(self):
        return "Energy: {0}\nSex: {1}\nAge: {2}\nStrength: {3}\nAgility: {4}\nFatigue: {5}".format(self.energy, self.sex, self.age, self.strength, self.agility, self.fatigue)

class Rabbit(Animal):
    def __init__(self, strength=RABBIT_BASE_STRENGTH, agility=RABBIT_BASE_AGILITY):
        super().__init__(strength, agility)

class Wolf(Animal):
    def __init__(self, strength=WOLF_BASE_STRENGTH, agility=WOLF_BASE_AGILITY):
        super().__init__(strength, agility)
