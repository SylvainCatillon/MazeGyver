from random import randrange
from config import game_config as cfg
from Map import Map
from Item import Item
from Player import Player
if cfg["use_pygame"]:
    from PyGame.Display import Display
    from PyGame.Input import Input
else:
    from Terminal.Display import Display
    from Terminal.Input import Input


class Game:
    """Class containing the current game.
    Control the progress of the game, by interacting with other classes"""

    def __init__(self):
        self.keep_playing = True
        self.player = Player()
        self.items_list = [Item(name) for name in cfg["item_names_list"]]
        self.map = Map()
        self.map.load_map("maps/map1")
        self.input = Input()
        self.display = Display(
            self.map.width, self.map.height,
            self.map.floor_list, self.map.wall_list)

    def place_items(self):
        """Place randomly the items on the map"""
        square_list = [cords for cords in self.map.floor_list if
                       cords != self.map.start_cords and
                       cords != self.map.keeper_cords]
        for item in self.items_list:
            cords = square_list.pop(randrange(len(square_list)))
            item.cords = cords

    def get_new_cords(self):
        """Get the new cords of the player.
        Ask an input direction, quit if the direction is "Q".
        Else, convert direction into cords by asking Player.
        Return the cords if they are on the map and are not a wall."""
        direction = self.input.game_input
        if direction == "Q":
            return "QUIT"
        cords = self.player.directions_dict[direction]
        if cords not in self.map.floor_list:
            return self.get_new_cords()
        return cords

    def check_items(self):
        """Check if the player has found an item"""
        cords = self.player.cords
        for item in self.items_list:
            if not item.found and cords == item.cords:
                item.found = True
                self.display.item_collected(item.name, cords)

    def reset_game(self):
        """Reset some value to prepare a new game"""
        for item in self.items_list:
            item.found = False
        self.display.reset()

    def end(self):
        """Check if the game is over. Return False if the game continue.
        Return True and calculate victory if the game is ending"""
        if self.player.cords != self.map.keeper_cords:
            return self.play()
        victory = True
        for item in self.items_list:
            if not item.found:
                victory = False
        self.display.end(victory)
        self.keep_playing = self.input.end_input
        if self.keep_playing:
            self.reset_game()

    def play(self):
        """Play the Game"""
        new_cords = self.get_new_cords()
        if new_cords == "QUIT":
            self.keep_playing = False
        else:
            self.player.cords = new_cords
            self.display.move_player(new_cords)
            self.check_items()
            self.end()

    def launch(self):
        """Launch the game"""
        self.player.cords = self.map.start_cords
        self.place_items()
        self.display.start(
            self.items_list, self.map.start_cords, self.map.keeper_cords)
        self.play()
