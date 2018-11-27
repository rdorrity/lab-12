# Team SCSI Logic
# Sara Kazemi, Cody Young, Nathan Warren-Acord, Ryan Dorrity
# Lab 11
# 11/22/2018
# ###########################################################

# Welcome everyone! This is just a template I started for the lab.
# Please feel free to change anything. I thought this might help 
# keep us organized, but please share any ideas you have for 
# this lab.

# Please note that any code you see in my section is mostly just
# for my own practice and not meant as a basis for how we should 
# code this project together.


##############################################################
##############################################################
#############          Sara Kazemi        ####################
# Game map:
#
#                     --------------------
#                    |                    |
#                    |                    |
#                    |                    |
#                    |     NORTH ROOM     |
#                    |                    |
#                    |                    |
#                    |                    |
# ----------------------------DOOR --------------------------
# |                  |                    |                  |
# |                  |                    |                  |
# |                  |                    |                  |
# |                  D                    D                  |
# |   WEST ROOM      O      START         O   EAST ROOM      |
# |                  O                    O                  |
# |                  R                    R                  |
# |                  |                    |                  |
#  ---------------------------DOOR --------------------------
#                    |                    |
#                    |                    |
#                    |                    |
#                    |                    |
#                    |    SOUTH ROOM      |
#                    |                    |
#                    |                    |
#                    |                    |
#                    |                    |
#                     --------------------
#

import re


class Location:

    def __init__(self, name, description, interactions, connections):
        self.name = name
        self.description = description
        self.interactions = interactions
        self.connections = connections
        self.visited = False

    def print_description(self):
        print("\n\t~~" + self.name + "~~\n")
        if not self.visited:
            print(self.description)

    def remove_item(self, item):
        if item in itemTable:
            self.description = self.description.replace(itemTable[item][2], "")

    def __getitem__(self):
        return self.name


# Room Definitions
main_room = Location("", "", [], {})
north_room = Location("", "", [], {})
south_room = Location("", "", [], {})
east_room = Location("", "", [], {})
west_room = Location("", "", [], {})

# Items in the world
itemTable = {
    "piece of metal": ["\nRadiates with a strange glow. Smooth to the touch.", main_room, "\nA shiny piece of\
 metal catches your eye on the west wall."]
}

# Room Initializations

# Main Room
main_room.name = "Main Room"
main_room.interactions = []
main_room.description = "Lit with a flickering torchlight, the room darkens at the corners. \
The walls are\nCyclopean stone and painted with moss. \
Motes of flora drift lightly and your feet\nsettle on soft grass. \
Four doors face you in each cardinal direction." + itemTable["piece of metal"][2]
main_room.connections = {"north": north_room, "south": south_room, \
                         "east": east_room, "west": west_room}

# North Room
north_room.name = "North Room"
north_room.description = "You are standing on a marble floor. Ahead of you is a grand staircase, flanked by two lamp posts.\n\
There is a fireplace to the left, a table to the right of you, and a statue with a grandfather clock\n\
next to it. On the table, there is a key. There is a door to the south."
north_room.interactions = []
north_room.connections = {"south": main_room}

# South Room
south_room.name = "South Room"
south_room.description = "There is a staircase leading downstairs, with a portrait on the wall. You can faintly hear\n\
flowing water coming from the stairwell. There is a door to the north."
south_room.interactions = []
south_room.connections = {"north": main_room}

# East Room
east_room.name = "East Room"
east_room.description = "You are standing on a stone floor. Flanking you on both sides are rows of portraits of various\n\
people who look unfamiliar. Each portrait is surrounded by two unlit torches. There is a chandelier\n\
hanging from the ceiling, and various wooden cabinets around the room. In the corner, there is an\n\
empty stone fountain."
east_room.interactions = []
east_room.connections = {"west": main_room}

# West Room
west_room.name = "West Room"
west_room.description = "You are standing on a wood floor. There is a large, round gyroscope-like structure in the middle,\n\
rotating slowly. Around you are shelves filled with old books, and there are several pieces of old\n\
parchment scattered on the floor. The script on the pieces of parchment is faded, and you can barely\n\
read it. In the corner, there is a chest in an alcove sitting on a velvet pillow, covered by\n\
glass. There is a door to the east."
west_room.interactions = []
west_room.connections = {"east": main_room}

cmdMove = re.compile(("^(north|n|south|s|west|w|east|e|up|down){1}$"), re.I)
cmdExit = re.compile(("^(Quit|Exit){1}$"), re.I)
cmdInv = re.compile("^(Inventory){1}$", re.I)
cmdLook = re.compile(("^(Scan|Look){1}$"), re.I)
cmdHelp = re.compile(("^(Help){1}$"), re.I)
cmdExamine = re.compile(("^Examine\s((\w+)(?:\s)?){1,4}$"), re.I)
cmdTake = re.compile(("^Take\s((\w+)(?:\s)?){1,4}$"), re.I)
cmdDrop = re.compile(("^Drop\s((\w+)(?:\s)?){1,4}$"), re.I)


def user_input(cmmd):
    if cmdExit.search(cmmd):
        print "Game Over. Thanks for playing!"
        raise SystemExit
    elif cmdHelp.search(cmmd):
        print_directions()
    elif cmdInv.search(cmmd):
        p.print_inventory()
    elif cmdLook.search(cmmd):
        print p.location.description
    elif cmdExamine.search(cmmd):
        examine = cmdExamine.search(cmmd)
        examine = re.sub("examine ", "", examine.group(), 1)
        # Examine function call would go here <--
        # if examine in (player inv) or examine in (room inv):
        # Print out that object description
        # else:
        # Print that player can't do that
    elif cmdTake.search(cmmd):
        take = cmdTake.search(cmmd)
        take = re.sub("take ", "", take.group(), 1)
        p.take_item(take)
    elif cmdDrop.search(cmmd):
        dropped = cmdDrop.search(cmmd)
        dropped = re.sub("drop ", "", dropped.group(), 1)
        # Dropped function call would go here <--
        # If in player's inv:
        # Remove from player's inv and add to room inv
        # Else:
        # Tell player it failed
    elif cmdMove.search(cmmd):
        move = cmdMove.search(cmmd).group(0)
        Player.move(p, move)
    else:
        print "I don't know that command."


class Player():
    def __init__(self):
        self.location = main_room

    def take_item(self, item):
        self.location.remove_item(item)
        if item in itemTable:
            itemTable[item][1] = self
            print "You took the " + item

    def move(self, direction):
        possibilities = ["north", "south", "east", "west", "up", "down"]
        for possibility in possibilities:
            if direction == possibility[0] or direction == possibility:
                if possibility in self.location.connections:
                    self.location.visited = True
                    self.location = self.location.connections[possibility]
                    self.location.print_description()
                else:
                    print "There's nowhere to go to the " + direction

    def print_inventory(self):
        for item in itemTable:
            if itemTable[item][1] == self:
                print item


def print_welcome():
    print "Your body aches. There is flowing water, somewhere, but you cannot tell where.\n\
Rolling over, blades of grass tickle your skin and the smell of ash brings\n\
burning tears. As you wipe your eyes, the surrounding structure comes into focus.\n\
You look around and discover you are in the ... "


def print_directions():
    print "\t\t---------------------------------------------------------------\n"
    print "\t\t\t\tWelcome to Stargate: SCSI-1!\n\t\tTo navigate the game world, type the following commands.\n\
\t\tAlternate commands are followed with a slash (e.g. command1/command2).\n\
\t\tCommands are not case sensitive.\n"
    print "\t\t---------------------------------------------------------------"
    print "\n\n_Movement_\n\
 Move north: n/north\n\
 Move south: s/south\n\
 Move west: w/west\n\
 Move east: e/east\n\n\
 _Player Actions_\n\
 Check inventory: inventory\n\
 Take item: take\n\
 Drop item: drop\n\
 Look around: look/scan\n\
 Examine item/room: examine\n\
 Exit game: quit/exit\n\n\
To access this help menu at any time, type \"help\".\n"


def main():
    print_directions()
    raw_input("Press Enter to continue...\n")
    print_welcome()
    Location.print_description(main_room)
    # run until exit or player dies
    while True:
      # prompt user for movement
      user_input(raw_input(">>>", ))
      # go to room and allow commands
p = Player()
main()







