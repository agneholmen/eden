from colorama import Fore, Style, Back

import argparse
import time

from animals import Wolf
from animals import Rabbit
from enums import Sex
import random

class Area:
    def __init__(self):
        self.grass = Grass() if random.randint(1, 3) == 1 else None
        self.rabbits = [Rabbit()] if random.randint(1, 2) == 1 else []
        self.wolves = [Wolf()] if random.randint(1, 3) == 1 else []

class Grass:
    max_size = 100

    def __init__(self, size=10):
        self.size = size

    def grow(self):
        self.size += 15
        if self.size > Grass.max_size:
            self.size = Grass.max_size

    def eaten(self, amount):
        self.size -= amount
        return amount if self.size >= 0 else amount + self.size

    def exists(self):
        return True if self.size > 0 else False

class World:
    def __init__(self, iterations, max_width, max_height):
        self.iterations = iterations
        self.max_width = max_width
        self.max_height = max_height

        self.map = []
        for _ in range(0, self.max_height):
            row = []
            for _ in range(0, self.max_width):
                row.append(Area())
            self.map.append(row)

    def print_world(self):
        line_string = "-"
        for _ in range(0, self.max_width):
            line_string += "-----"
        print(line_string)
        for row in self.map:
            # Grass
            row_string = "|"
            for cell in row:
                if cell.grass:
                    if cell.grass.size >= 100:
                        row_string += f" {Fore.GREEN}{Style.BRIGHT}{str(cell.grass.size)}{Style.RESET_ALL}|"
                    elif cell.grass.size >= 10:
                        row_string += f" {Fore.GREEN}{Style.BRIGHT}{str(cell.grass.size)}{Style.RESET_ALL} |"
                    else:
                        row_string += f" {Fore.GREEN}{Style.BRIGHT}{str(cell.grass.size)}{Style.RESET_ALL}  |"
                else:
                    row_string += "    |"
            print(row_string)

            # Rabbits
            row_string = "|"
            for cell in row:
                if cell.rabbits:
                    if len(cell.rabbits) >= 10:
                        row_string += f" {Fore.BLUE}{Style.BRIGHT}{str(len(cell.rabbits))}{Style.RESET_ALL} |"
                    else:
                        row_string += f" {Fore.BLUE}{Style.BRIGHT}{str(len(cell.rabbits))}{Style.RESET_ALL}  |"
                else:
                    row_string += "    |"
            print(row_string)

            # Wolves
            row_string = "|"
            for cell in row:
                if cell.wolves:
                    if len(cell.wolves) >= 10:
                        row_string += f" {Fore.RED}{Style.BRIGHT}{str(len(cell.wolves))}{Style.RESET_ALL} |"
                    else:
                        row_string += f" {Fore.RED}{Style.BRIGHT}{str(len(cell.wolves))}{Style.RESET_ALL}  |"
                else:
                    row_string += "    |"
            print(row_string)

            print(line_string)
            
        print(f"WOLVES, Number: {str(self.get_number_of_wolves())}, Strength: {str(self.get_wolf_average_strength())}, Agility: {str(self.get_wolf_average_agility())}, {self.get_wolf_sex_percentages()}")
        print(f"RABBITS, Number: {str(self.get_number_of_rabbits())}, Strength: {str(self.get_rabbit_average_strength())}, Agility: {str(self.get_rabbit_average_agility())}, {self.get_rabbit_sex_percentages()}")
        print(f"Number of grass: {str(self.get_number_of_grass())}")

    def find_neighbours(self, row_index, cell_index):
        neighbours = []

        possible = [(row_index - 1, cell_index - 1), (row_index - 1, cell_index),
                    (row_index - 1, cell_index + 1), (row_index, cell_index - 1),
                    (row_index, cell_index + 1), (row_index + 1, cell_index - 1),
                    (row_index + 1, cell_index), (row_index + 1, cell_index + 1)]

        for p in possible:
            if 0 <= p[0] <= self.max_height - 1 and 0 <= p[1] <= self.max_width - 1:
                neighbours.append(p)

        return neighbours

    def get_random_neighbour(self, row_index, cell_index):
        neighbours = self.find_neighbours(row_index, cell_index)
        r = random.randint(0, len(neighbours) - 1)
        neighbour = neighbours[r]
        
        return neighbour
    
    # Grass STAT functions
    def get_number_of_grass(self):
        grass = 0

        for row in self.map:
            for cell in row:
                if cell.grass:
                    grass += 1

        return grass

    # Rabbit STAT functions
    def get_number_of_rabbits(self):
        rabbits = 0

        for row in self.map:
            for cell in row:
                if cell.rabbits:
                    rabbits += len(cell.rabbits)

        return rabbits
    
    def get_rabbit_average_strength(self):
        number_of_rabbits = self.get_number_of_rabbits()
        if number_of_rabbits == 0:
            return 0
        total = 0
        for row in self.map:
            for cell in row:
                if cell.rabbits:
                    for rabbit in cell.rabbits:
                        total += rabbit.strength
        
        return round(total / self.get_number_of_rabbits(), 2)
    
    def get_rabbit_average_agility(self):
        number_of_rabbits = self.get_number_of_rabbits()
        if number_of_rabbits == 0:
            return 0
        total = 0
        for row in self.map:
            for cell in row:
                if cell.rabbits:
                    for rabbit in cell.rabbits:
                        total += rabbit.agility
        
        return round(total / self.get_number_of_rabbits(), 2)
    
    def get_rabbit_sex_percentages(self):
        number_of_rabbits = self.get_number_of_rabbits()
        if number_of_rabbits == 0:
            return "Male: 0%, Female: 0%"
        male = 0
        female = 0
        for row in self.map:
            for cell in row:
                if cell.rabbits:
                    for rabbit in cell.rabbits:
                        if rabbit.sex == Sex.FEMALE:
                            female += 1
                        else:
                            male += 1

        return f"Male: {round((male / (male + female)) * 100, 1)}%, Female: {round((female / (male + female)) * 100, 1)}%"
    
    # Wolf STAT functions
    def get_number_of_wolves(self):
        wolves = 0
        for row in self.map:
            for cell in row:
                if cell.wolves:
                    wolves += len(cell.wolves)

        return wolves
    
    def get_wolf_average_strength(self):
        number_of_wolves = self.get_number_of_wolves()
        if number_of_wolves == 0:
            return 0
        total = 0
        for row in self.map:
            for cell in row:
                if cell.wolves:
                    for wolf in cell.wolves:
                        total += wolf.strength
        
        return round(total / number_of_wolves, 2)
    
    def get_wolf_average_agility(self):
        number_of_wolves = self.get_number_of_wolves()
        if number_of_wolves == 0:
            return 0
        total = 0
        for row in self.map:
            for cell in row:
                if cell.wolves:
                    for wolf in cell.wolves:
                        total += wolf.agility
        
        return round(total / number_of_wolves, 2)
    
    def get_wolf_sex_percentages(self):
        male = 0
        female = 0
        number_of_wolves = self.get_number_of_wolves()
        if number_of_wolves == 0:
            return "Male: 0%, Female: 0%"
        for row in self.map:
            for cell in row:
                if cell.wolves:
                    for wolf in cell.wolves:
                        if wolf.sex == Sex.FEMALE:
                            female += 1
                        else:
                            male += 1

        return f"Male: {round((male / (male + female)) * 100, 1)}%, Female: {round((female / (male + female)) * 100, 1)}%"

def main(iterations, max_height, max_width, delay):
    world = World(iterations, max_height, max_width)

    print("Original:")
    world.print_world()

    for i in range(1, iterations + 1):
        print(f"Iteration {str(i)}:")
        # Grow
        for row_index, row in enumerate(world.map):
            for cell_index, cell in enumerate(row):
                if cell.grass:
                    cell.grass.grow()

        # Spread seeds
        for row_index, row in enumerate(world.map):
            for cell_index, cell in enumerate(row):
                if cell.grass:
                    s = world.get_random_neighbour(row_index, cell_index)
                    if not world.map[s[0]][s[1]].grass:
                        world.map[s[0]][s[1]].grass = Grass(10)

        # Rabbits
        for row_index, row in enumerate(world.map):
            for cell_index, cell in enumerate(row):
                if cell.rabbits:
                    # Sort by strength to add evolutional pressure for strength
                    cell.rabbits.sort(key=lambda x: x.strength, reverse=True)
                    for rabbit in cell.rabbits:
                        # Lose energy
                        rabbit.tire()
                        # Age
                        rabbit.increase_age()

                        # First eat if there's any grass and energy is 40 or below
                        if cell.grass and rabbit.energy <= 40:
                            rabbit.eat_grass(cell.grass)
                            if not cell.grass.exists():
                                cell.grass = None
                        # Otherwise move to different cell or die
                        elif rabbit.energy < 40:
                            if rabbit.is_dead():
                                cell.rabbits.remove(rabbit)
                                continue
                            else:
                                neighbours = world.find_neighbours(row_index, cell_index)
                                for n in neighbours:
                                    if world.map[n[0]][n[1]].grass:
                                        world.map[n[0]][n[1]].rabbits.append(rabbit)
                                        cell.rabbits.remove(rabbit)
                                        break
                                else:
                                    s = world.get_random_neighbour(row_index, cell_index)
                                    world.map[s[0]][s[1]].rabbits.append(rabbit)
                                    cell.rabbits.remove(rabbit)
                            continue

                        # Attempt to breed. First find partner.
                        if rabbit.breeding == 0 and rabbit.energy > 40:
                            # No other rabbits. Need to move
                            if len(cell.rabbits) == 1:
                                neighbours = world.find_neighbours(row_index, cell_index)
                                for n in neighbours:
                                    if world.map[n[0]][n[1]].rabbits:
                                        world.map[n[0]][n[1]].rabbits.append(rabbit)
                                        cell.rabbits.remove(rabbit)
                                        break
                                else:
                                    s = world.get_random_neighbour(row_index, cell_index)
                                    world.map[s[0]][s[1]].rabbits.append(rabbit)
                                    cell.rabbits.remove(rabbit)
                                continue
                            else:
                                for partner in cell.rabbits:
                                    if partner != rabbit and partner.sex != rabbit.sex and partner.breeding == 0:
                                        partner.breeding = 3
                                        rabbit.breeding = 3
                                        if cell.grass:
                                            number_of_children = 1 + random.randint(0, int(cell.grass.size / 5))
                                        else:
                                            number_of_children = 1
                                        for _ in range(0, number_of_children):
                                            r = Rabbit()
                                            r.strength = int(((partner.strength + rabbit.strength) / 2) + random.randint(0, 5))
                                            r.agility = int(((partner.agility + rabbit.agility) / 2) + random.randint(0, 5))

                                        cell.rabbits.append(r)
                                        break
                        # Check if dead and remove
                        if rabbit.is_dead():
                            cell.rabbits.remove(rabbit)

        # Wolves
        for row_index, row in enumerate(world.map):
            for cell_index, cell in enumerate(row):
                if cell.wolves:
                    # Sort by strength to add evolutional pressure for strength
                    cell.wolves.sort(key=lambda x: x.strength, reverse=True)
                    for wolf in cell.wolves:
                        # Lose energy
                        wolf.tire()
                        # Age
                        wolf.increase_age()

                        # Hunt if hungry (energy < 50)
                        if wolf.energy < 50:
                            if wolf.is_dead():
                                cell.wolves.remove(wolf)
                                continue
                            else:
                                # Try to catch a rabbit
                                if cell.rabbits:
                                    r = random.randint(0, len(cell.rabbits) - 1)
                                    random_rabbit = cell.rabbits[r]
                                    if (wolf.energy + wolf.strength) > (random_rabbit.energy + random_rabbit.agility):
                                        wolf.energy += random_rabbit.energy
                                        cell.rabbits.remove(random_rabbit)
                                    else:
                                        wolf.tire()
                                        random_rabbit.tire()
                                # Move to a different area, preferrably one with rabbits
                                else:
                                    neighbours = world.find_neighbours(row_index, cell_index)
                                    for n in neighbours:
                                        if world.map[n[0]][n[1]].rabbits:
                                            world.map[n[0]][n[1]].wolves.append(wolf)
                                            cell.wolves.remove(wolf)
                                            break
                                    else:
                                        s = world.get_random_neighbour(row_index, cell_index)
                                        world.map[s[0]][s[1]].wolves.append(wolf)
                                        cell.wolves.remove(wolf)
                                    continue

                        if wolf.energy > 50 and wolf.breeding == 0:
                            # No other wolves. Need to move
                            if len(cell.wolves) == 1:
                                neighbours = world.find_neighbours(row_index, cell_index)
                                for n in neighbours:
                                    if world.map[n[0]][n[1]].wolves:
                                        world.map[n[0]][n[1]].wolves.append(wolf)
                                        cell.wolves.remove(wolf)
                                        break
                                else:
                                    s = world.get_random_neighbour(row_index, cell_index)
                                    world.map[s[0]][s[1]].wolves.append(wolf)
                                    cell.wolves.remove(wolf)
                                continue
                            else:
                                for partner in cell.wolves:
                                    if partner != wolf and partner.sex != wolf.sex and partner.breeding == 0:
                                        partner.breeding = 10
                                        wolf.breeding = 10
                                        w = Wolf()
                                        w.strength = int(((partner.strength + wolf.strength) / 2) + random.randint(0, 5))
                                        w.agility = int(((partner.agility + wolf.agility) / 2) + random.randint(0, 5))

                                        cell.wolves.append(w)
                                        break

                        # Check if dead and remove
                        if wolf.is_dead():
                            cell.wolves.remove(wolf)

        world.print_world()
        time.sleep(delay)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", help="Number of iterations.", type=int, default=10)
    parser.add_argument("-mh", "--height", help="The height of the map in number of cells.", type=int, default=5)
    parser.add_argument("-mw", "--width", help="The width of the map in number of cells.", type=int, default=5)
    parser.add_argument("-d", "--delay", help="The delay in seconds between each iteration.", type=int, default=3)
    args = parser.parse_args()

    main(args.iterations, args.height, args.width, args.delay)
