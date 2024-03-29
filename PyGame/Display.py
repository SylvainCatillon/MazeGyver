import pygame as pg
from config import display_config as cfg


class Display:
    """Use PyGame to display the MazeGyver game"""

    def __init__(self, map_width, map_height, floor_list, wall_list):
        pg.init()
        self.screen_width = cfg["screen_size"][0]-(
                cfg["screen_size"][0] % map_width)
        self.screen_height = cfg["screen_size"][1]-(
                cfg["screen_size"][1] % map_height)
        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height))
        pg.display.set_caption("MazeGyver")
        pg.display.set_icon(pg.image.load("resources/tile-crusader-logo.png"))
        self.square_width = self.screen_width//map_width
        self.square_height = self.screen_height//map_height
        self.font = pg.font.Font(None, self.square_width)
        self.floor_rect_dict = {
            (x, y): pg.Rect(x * self.square_width, y * self.square_height,
                            self.square_width, self.square_height)
            for (x, y) in floor_list}
        self.wall_rect_dict = {
            (x, y): pg.Rect(x * self.square_width, y * self.square_height,
                            self.square_width, self.square_height)
            for (x, y) in wall_list}
        if cfg["inventory"]:
            self.screen = pg.display.set_mode(
                (self.screen_width, self.screen_height+self.square_height))
            self.items_found = 0
            self.inventory_rect_list = []
        self.displayed_player_pos = (0, 0)
        self.image_dict = {}
        pg.key.set_repeat(350, 60)

    @property
    def square_size(self):
        return self.square_width, self.square_height

    def load_image(self, name):
        """Load an image from a png file in resources directory.
         Scales it and put it in self.images_dict"""
        file_name = "resources/{}.png".format(name)
        image = pg.image.load(file_name).convert_alpha()
        self.image_dict[name.lower()] = pg.transform.scale(image,
                                                           self.square_size)

    def load_background(self):
        """Load the floor and wall images from a sprite sheet."""
        sprite_sheet = pg.image.load(cfg["floor_tiles"])
        floor_width = sprite_sheet.get_width() // cfg["nb_floors"][0]
        floor_height = sprite_sheet.get_height() // cfg["nb_floors"][1]
        floor_image = pg.Surface((floor_width, floor_height))
        floor_area = (floor_width*cfg["floor_index"][0], floor_height *
                      cfg["floor_index"][1], floor_width, floor_height)
        floor_image.blit(sprite_sheet, (0, 0), floor_area)
        self.image_dict["floor"] = pg.transform.scale(
            floor_image, self.square_size)
        wall_image = pg.Surface((floor_width, floor_height))
        wall_area = (floor_width*cfg["wall_index"][0], floor_height *
                     cfg["wall_index"][1], floor_width, floor_height)
        wall_image.blit(sprite_sheet, (0, 0), wall_area)
        self.image_dict["wall"] = pg.transform.scale(
            wall_image, self.square_size)

    def prepare_inventory(self, items_list):
        """Prepare an inventory to be displayed.
        Inventory is a line at the bottom of the screen,
        which display a welcome message at the start.
        Every time an item is found, a message and the image of the item
        can be displayed in the inventory"""
        text_width = self.screen_width-self.square_width*len(items_list)
        text_rect = pg.Rect(0, self.screen_height,
                            text_width, self.square_height)
        self.inventory_rect_list.append(text_rect)
        for i in range(len(items_list)):
            rect = pg.Rect(text_width+self.square_width*i, self.screen_height,
                           self.square_width, self. square_height)
            self.inventory_rect_list.append(rect)
        text_surf = self.font.render(cfg["welcome_text"].format(
            len(items_list)), True, cfg["text_color"])
        if text_surf.get_width() > text_rect.width:
            text_surf = pg.transform.scale(text_surf, (text_rect.width,
                                                       text_surf.get_height()))
        self.screen.blit(text_surf, text_rect)

    def prepare_map(self, start, keeper):
        """Prepare the map to be displayed on the screen"""
        for floor_rect in self.floor_rect_dict.values():
            self.screen.blit(self.image_dict["floor"], floor_rect)
        for wall_rect in self.wall_rect_dict.values():
            self.screen.blit(self.image_dict["wall"], wall_rect)
        self.screen.blit(self.image_dict["keeper"],
                         self.floor_rect_dict[keeper])
        self.screen.blit(self.image_dict["player"],
                         self.floor_rect_dict[start])

    def prepare_item(self, item):
        """Load the image of an item, and prepare it to be displayed on screen.
        Take an Object Item as argument"""
        self.load_image(item.name)
        self.screen.blit(self.image_dict[item.name.lower()],
                         self.floor_rect_dict[item.cords])

    def start(self, items_list, start, keeper):
        """Start the display"""
        self.load_background()
        self.load_image("Player")
        self.load_image("Keeper")
        if cfg["inventory"]:
            self.prepare_inventory(items_list)
        self.prepare_map(start, keeper)
        self.displayed_player_pos = start
        for item in items_list:
            self.prepare_item(item)
        pg.display.update()

    def move_player(self, cords):
        """Update the screen to follow player movement"""
        old_rect = self.floor_rect_dict[self.displayed_player_pos]
        new_rect = self.floor_rect_dict[cords]
        self.screen.blit(self.image_dict["floor"], old_rect)
        self.screen.blit(self.image_dict["player"], new_rect)
        self.displayed_player_pos = cords
        pg.display.update([old_rect, new_rect])

    def item_collected(self, item_name, cords):
        """Update the screen to delete collected item.
        If Inventory is on, display a message and the item"""
        if cfg["inventory"]:
            self.items_found += 1
            text_rect = self.inventory_rect_list[0]
            item_rect = self.inventory_rect_list[self.items_found]
            text_surf = pg.Surface(text_rect.size)
            text_surf.blit(self.font.render(cfg["item_text"] + item_name,
                                            True, cfg["text_color"]), (0, 0))
            self.screen.blit(text_surf, text_rect)
            self.screen.blit(self.image_dict[item_name.lower()], item_rect)
            pg.display.update([text_rect, item_rect])
        rect = self.floor_rect_dict[cords]
        self.screen.blit(self.image_dict["floor"], rect)
        self.screen.blit(self.image_dict["player"], rect)
        pg.display.update(rect)

    def form_end_screen(self, text):
        """Prepare the end screen.
        Take the text to be displayed for argument"""
        end_screen = pg.Surface(self.screen.get_size())
        lines_list = text.split("\n")
        for i, line in enumerate(lines_list):
            text_surf = self.font.render(line, True, cfg["text_color"])
            text_height = text_surf.get_height()
            if text_surf.get_width() > end_screen.get_width():
                text_surf = pg.transform.scale(
                    text_surf, (end_screen.get_width(), text_height))
            text_width = text_surf.get_width()
            x_cord = end_screen.get_width()/2 - text_width/2
            y_cord = end_screen.get_height()/2 - (
                    (len(lines_list))/2 - i)*text_height
            end_screen.blit(text_surf, (x_cord, y_cord))
        self.screen.blit(end_screen, (0, 0))

    def end(self, victory):
        """Call form_end_screen() with the right text,
        and display the end screen"""
        if victory:
            self.form_end_screen(cfg["victory_text"]+"\n\n"+cfg["end_text"])
        else:
            self.form_end_screen(cfg["defeat_text"]+"\n\n"+cfg["end_text"])
        pg.display.update()

    def reset(self):
        """Reset some values of the display to prepare a new game"""
        if cfg["inventory"]:
            self.inventory_rect_list = []
            self.items_found = 0
