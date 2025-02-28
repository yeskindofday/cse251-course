"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Your name here>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.

Claim: 5
"""

import random
import multiprocessing as mp
import os.path
import time
from datetime import datetime
from multiprocessing.connection import Connection

# Include cse 251 common Python files - Don't change
from cse251 import *
set_working_directory(__file__)


CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables


class Bag():
    """ bag of marbles - Don't change for the 93% """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change for the 93% """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, parent_pipe: Connection, delay: float, marble_count: int):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.parent_pipe = parent_pipe
        self.delay = delay
        self.marble_count = marble_count

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marble_count):
            i = random.randint(0, len(self.colors) - 1)
            self.parent_pipe.send(self.colors[i])

            time.sleep(self.delay)

        self.parent_pipe.send(None)
        self.parent_pipe.close()


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self, child_pipe: Connection, parent_pipe: Connection, delay: float, bag_count: int):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.child_pipe = child_pipe
        self.parent_pipe = parent_pipe
        self.delay = delay

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bag = Bag()
        while True:
            marble = self.child_pipe.recv()
            if marble:
                bag.add(marble)

            bag_is_full = bag.get_size() >= self.bag_count
            marbles_are_remaining_after_done = marble is None and bag.get_size() >= 1

            if bag_is_full or marbles_are_remaining_after_done:
                self.parent_pipe.send(bag)
                bag = Bag()

            if marble is None:
                break

            time.sleep(self.delay)

        self.child_pipe.close()
        self.parent_pipe.send(None)
        self.parent_pipe.close()


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, child_pipe: Connection, parent_pipe: Connection, delay: float, gift_counter: mp.Value):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.child_pipe = child_pipe
        self.parent_pipe = parent_pipe
        self.delay = delay
        self.gift_counter = gift_counter

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while (bag := self.child_pipe.recv()) is not None:
            i = random.randint(0, len(self.marble_names) - 1)
            gift = Gift(self.marble_names[i], bag)
            self.gift_counter.value += 1
            self.parent_pipe.send(gift)

            time.sleep(self.delay)

        self.child_pipe.close()
        self.parent_pipe.send(None)
        self.parent_pipe.close()


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """

    def __init__(self, child_pipe: Connection, delay: float, boxes_filename: str):
        mp.Process.__init__(self)
        # Add any arguments and variables here
        self.child_pipe = child_pipe
        self.delay = delay
        self.boxes_filename = boxes_filename

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        lines = []
        while (gift := self.child_pipe.recv()) is not None:
            current_time = str(datetime.now().time())
            lines.append(f"Created - {current_time}: {str(gift)}\n")
            time.sleep(self.delay)
        with open(self.boxes_filename, "w") as f:
            f.writelines(lines)

        self.child_pipe.close()


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(
            f'The file {filename} doesn\'t exist.  No boxes were created.')


def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(
            f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # create Pipes between creator -> bagger -> assembler -> wrapper
    parent_pipes = []
    child_pipes = []
    for _ in range(3):
        parent, child = mp.Pipe()
        parent_pipes.append(parent)
        child_pipes.append(child)

    # create variable to be used to count the number of gifts
    gift_counter = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # Create the processes (ie., classes above)
    processes = []
    processes.append(Marble_Creator(
        parent_pipes[0], settings[CREATOR_DELAY], settings[MARBLE_COUNT]))
    processes.append(Bagger(
        child_pipes[0], parent_pipes[1], settings[BAGGER_DELAY], settings[BAG_COUNT]))
    processes.append(Assembler(
        child_pipes[1], parent_pipes[2], settings[ASSEMBLER_DELAY], gift_counter))
    processes.append(
        Wrapper(child_pipes[2], settings[WRAPPER_DELAY], BOXES_FILENAME))

    log.write('Starting the processes')
    for p in processes:
        p.start()

    log.write('Waiting for processes to finish')
    for p in processes:
        p.join()

    display_final_boxes(BOXES_FILENAME, log)

    # Log the number of gifts created.
    log.write(f"Number of gifts created: {gift_counter.value}")


if __name__ == '__main__':
    main()
