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
    max_age = 10
    def __init__(self,  strength=STAT_BASE, agility=STAT_BASE):
        self.energy = 50
        self.sex = enums.randomize()
        self.age = 0
        self.strength = strength
        self.agility = agility
        self.fatigue = 0
        self.breeding = 5
        self.name = id_generator()
        self.iteration = 0

    def is_dead(self):
        if self.energy <= 0 or self.age > self.max_age:
            return True
        else:
            return False
    
    def increase_age(self, amount=1):
        self.age += amount
        self.breeding = max(0, self.breeding - amount)

    def __str__(self):
        return "Energy: {0}\nSex: {1}\nAge: {2}\nStrength: {3}\nAgility: {4}\nFatigue: {5}".format(self.energy, self.sex, self.age, self.strength, self.agility, self.fatigue)

class Rabbit(Animal):
    max_age = 15
    breeding_age = 2
    def __init__(self, strength=RABBIT_BASE_STRENGTH + random.randint(-5, 5), agility=RABBIT_BASE_AGILITY + random.randint(-5, 5)):
        super().__init__(strength, agility)
        self.breeding = Rabbit.breeding_age

    def eat_grass(self, grass, amount=10):
        self.energy += grass.eaten(amount)

    def tire(self, amount=5):
        self.energy -= amount

    def __str__(self):
        return f"Name: {self.name}, Sex: {self.sex}, Strength: {self.strength}, Agility: {self.agility}, Energy: {self.energy}"

class Wolf(Animal):
    max_age = 30
    breeding_age = 8
    def __init__(self, strength=WOLF_BASE_STRENGTH + random.randint(-5, 5), agility=WOLF_BASE_AGILITY + random.randint(-5, 5), energy=75):
        super().__init__(strength, agility)
        self.energy = energy
        self.breeding = Wolf.breeding_age

    def tire(self, amount=5):
        self.energy -= amount

    def __str__(self):
        return f"Name: {self.name}, Sex: {self.sex}, Strength: {self.strength}, Agility: {self.agility}, Energy: {self.energy}"    
