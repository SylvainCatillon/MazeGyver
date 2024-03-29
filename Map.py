from config import map_config as cfg


class Map:
    """The map of the game"""

    def __init__(self):
        self.wall_list = []
        self.floor_list = []
        self.start_cords = (0, 0)
        self.keeper_cords = (0, 0)
        self.height = 1
        self.width = 1

    def load_map(self, map_name):
        """Read the map file.
         Fill floor_list and wall_list.
         Set start position, keeper position, height and width of the map"""
        with open(map_name + ".txt", "r") as file:
            text = file.read()
        rows_list = text.split("\n")
        self.height = len(rows_list)
        width = 0
        x = 0
        for y, e in enumerate(rows_list):
            for x, f in enumerate(e):
                f = f.upper()
                if f in cfg["symbol_dict"].values():
                    if f == cfg["symbol_dict"]["wall"]:
                        self.wall_list.append((x, y))
                    else:
                        self.floor_list.append((x, y))
                    if f == cfg["symbol_dict"]["start"]:
                        self.start_cords = (x, y)
                    elif f == cfg["symbol_dict"]["keeper"]:
                        self.keeper_cords = (x, y)
            if x >= width:
                width = x+1
        self.width = width
