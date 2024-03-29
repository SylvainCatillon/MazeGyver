# MazeGyver
A simple 2D maze game, using PyGame. You're playing [MacGyver](https://www.youtube.com/watch?v=lc8RFPZUkiQ), who is stuck in a maze. The exit is watched by a keeper.
You have to collect three items placed randomly on the map: a bottle of ether, a needle and a plastic tube. Then, you can make a syringe and send the keeper to sleep.
If you reach the exit without the items, you die.

# Getting started
Use the requirement.txt to install the needed package: 
`pip install -r requirements.txt`\
To launch the game, open `main.py`

# Config
You can change variables in config.py to change the config:

- display_config:
  - floor_tiles: Path of the floors' sprite sheet.
  - nb_floors: Number of sprites on the floors sprite sheet. Change only if you change of spritesheet
  - floor_index : Index of the floor image, as (column index, row index). Change if you want to change of floor image
  - wall_index : Index of the wall image, as (column index, row index). Change if you want to change of wall image
  - screen_size: Size of the screen, as (width, height)
  - inventory: Set it to True if you want the inventory to be displayed
  - text_color: You can change the color of the text, with tree indices between 0 and 255: (red, green, blue)
  - You can change the messages of the game by changing several text variables

- map_config:
  - symbol_dict: A dictionary with the symbols of the map. Change it if you change the map file

- game_config:
  - item_names_list: Change it if you changes the items of the map. **The image's file name must be the same as the item's**
  - use_pygame: Set it to True to use PyGame.
