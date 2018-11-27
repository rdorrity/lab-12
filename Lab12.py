# Team SCSI Logic
# Sara Kazemi, Cody Young, Nathan Warren-Acord, Ryan Dorrity
# Lab 12
# 11/26/2018
# ###########################################################

# Welcome to Stargate: SCSI-1! a text-based adventure


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

# The Location class is used to initialize all of our rooms
# Each Location has:
# String: name (prints when you visit a room)
# String: description (prints the first time you visit a room or of you "look" at a room).
# List: interactions (items in the room you can interact with)
# Dictionary: connections (keys are Strings that refer to a valid direction a character can move from this Location
# and the values are reference variables of the rooms corresponding to those directions.
# boolean: visited: Initialized to False and changes to True once the player moves to a new room.
class Location:
    # Constructor for our locations.
    def __init__(self, name, description, interactions, connections):
        self.name = name
        self.description = description
        self.interactions = interactions
        self.connections = connections
        self.visited = False

    def print_description(self):
        print("\n\t~~" + self.name + "~~\n")
        if not self.visited:    # Only print the description of the room if Player hasn't been there before
                                # Note: Player can use "look" to see the description again
            print(self.description)

    def remove_item(self, item):
        if item in itemTable:   # When an item is removed from the room, we should remove its description
                                # from our itemTable and replace it with an empty string.
                                # This removes the item description from the room's description.
            self.description = self.description.replace(itemTable[item][2], "")

    def __getitem__(self):      # helper function. Not really used at the moment. Remove?
        return self.name


# Room Definitions
# Rooms are created ahead of time with dummy empty values because we need to refer to these objects in their
# connections dictionary.
main_room = Location("", "", [], {})
north_room = Location("", "", [], {})
south_room = Location("", "", [], {})
east_room = Location("", "", [], {})
west_room = Location("", "", [], {})

# Items in the world
# A dictionary that holds all the items in the world as keys. The values are lists.
# The 0th index of that list holds the description of the item when the Player examines the item
# The 1st index of the list holds the reference object (a Location or Player) that possesses the item
# The 2nd index of the list holds the description of the item that gets concatenated to the room's location
# if it is in that room. This description turns into the empty string when a Player takes the item.
itemTable = {
    "piece of metal": ["\nRadiates with a strange glow. Smooth to the touch.", main_room, "\nA shiny piece of\
 metal catches your eye on the west wall."]
}

# Room Initializations
# Now we can assign the instance variables with our real values without breaking the code.

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





# Handing user input
# We use regular expressions to find matches for valid commands
# These are called in our user_input function to determine
# What the appropriate response should be
cmdMove = re.compile(("^(north|n|south|s|west|w|east|e|up|down){1}$"), re.I)
cmdExit = re.compile(("^(Quit|Exit){1}$"), re.I)
cmdInv = re.compile("^(Inventory){1}$", re.I)
cmdLook = re.compile(("^(Scan|Look){1}$"), re.I)
cmdHelp = re.compile(("^(Help){1}$"), re.I)
cmdExamine = re.compile(("^Examine\s((\w+)(?:\s)?){1,4}$"), re.I)
cmdTake = re.compile(("^Take\s((\w+)(?:\s)?){1,4}$"), re.I)
cmdDrop = re.compile(("^Drop\s((\w+)(?:\s)?){1,4}$"), re.I)

# user_input takes a String cmmd and determines if it matches any of our regular expressions
# and responds accordingly
def user_input(cmmd):
    if cmdExit.search(cmmd):                        # exits game if Player inputs "exit" or "quit"
        print "Game Over. Thanks for playing!"
        raise SystemExit
    elif cmdHelp.search(cmmd):                      # re-prints out the directions if the Player inputs "help"
        print_directions()
    elif cmdInv.search(cmmd):                       # prints out the contents of the Player's inventory
        p.print_inventory()                         # to do: Print out "nothing in inventory" if empty
    elif cmdLook.search(cmmd):                      # prints out the description of the Player's Location
        print p.location.description                # when Player inputs "look"
    elif cmdExamine.search(cmmd):                   # prints out item's description if the Player types examine
        examine = cmdExamine.search(cmmd)
        examine = re.sub("examine ", "", examine.group(), 1) # need to fix
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


def print_intro():
    print "Your body aches. There is flowing water, somewhere, but you cannot tell where.\n\
Rolling over, blades of grass tickle your skin and the smell of ash brings\n\
burning tears. As you wipe your eyes, the surrounding structure comes into focus.\n\
You look around and discover you are in the ... "

def print_welcome():
    print "\t\t---------------------------------------------------------------\n"
    print "\t\t\t\t\t\tWelcome to Stargate: SCSI-1!\n\n\
    \tTo navigate the game world, type the following commands.\n\
    \tAlternate commands are followed with a slash (e.g. command1/command2).\n\
    \tCommands are not case sensitive.\n"
    print "\t\t---------------------------------------------------------------"

def print_directions():

 print "\n\n _Movement_\n\
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
    print_welcome()
    print_directions()
    raw_input("Press Enter to continue...\n")
    print_intro()
    Location.print_description(main_room)
    # run until exit or player dies
    while True:
      # prompt user for movement
      user_input(raw_input(">>>", ))
      # go to room and allow commands
p = Player()
main()







