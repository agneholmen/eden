from enum import Enum

import random

class Sex(Enum):
    MALE = 1
    FEMALE = 2

def randomize():
    if random.randint(1, 2) == 1:
        return Sex.MALE
    else:
        return Sex.FEMALE
