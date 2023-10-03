# classes.py

import random, math, os
from PIL import ImageFont, Image, ImageDraw
from config import *


def define_segment():
        segment: object = CharacterSegment(
            seed_string = SEED_STRING,
            randomize_string = RANDOMIZE_STRING,
            transition_length = TRANSITION_LENGTH,
            min_length = SEGMENT_LENGTH_MIN,
            max_length = SEGMENT_LENGTH_MAX,
            primary_color = BASE_COLOR,
            secondary_color = ACCENT_COLOR,
            background_color = BACKGROUND_COLOR
        )
        return segment

#-------------------------------------------------------------------------------------------------------
class Grid:
    def __init__(self, canvas_width: int, canvas_height: int, column_spacing: int, row_spacing: int):
        self.total_columns: int = None # total columns in grid
        self.total_rows: int = None # total rows in grid
        self.column_coords: int = [] # pixel coordinates for each column
        self.row_coords: int = [] # pixel coordinates for each row
        self.init_grid_values(canvas_width, canvas_height, column_spacing, row_spacing)

    def init_grid_values(self, canvas_width, canvas_height, column_spacing, row_spacing):
        # set max columns and rows that can fit within canvas dimensions, round down
        self.total_columns = math.floor(canvas_width / column_spacing)
        self.total_rows = math.floor(canvas_height / row_spacing)
        # create origin pixel coordinates for each row and column
        for column in range(self.total_columns):
            self.column_coords.append(column_spacing * column)
        for row in range(self.total_rows):
            self.row_coords.append(row_spacing * row)

#-------------------------------------------------------------------------------------------------------
class CharacterSegment:
    def __init__(self, seed_string: str, randomize_string: bool, transition_length: int, min_length: int, max_length: int, primary_color: list, secondary_color: list, background_color: list):
        self.seed_string = seed_string # character types segment can contain
        self.randomize_string = randomize_string # if new_character() will randomize seed string
        self.transition_length = transition_length # number of transitionally colored characters
        self.color_a = primary_color # leading character color
        self.color_b = secondary_color # body characters color
        self.bg_color = background_color # color of surface segment is rendered on
        self.length = random.randint(min_length, max_length) # total simultaneous characters allowed in segment
        self.column_id: int = None # column number of leading character
        self.row_id: int = None # row number of leading character
        self.characters: str = [] # characters segment currently contains ([0] = oldest character)
        self.character_colors: str = [] # colors of characters in characters list
        self.seed_character_index = 0 # tracks current position in seed_string when seed not randomized
        self.set_colors()

    def new_character(self):
        # if segment not already at full length, add character
        if len(self.characters) < self.length:
            # if randomize seed string, reference source string using random as index
            if self.randomize_string is True:
                random_index = random.randint(0, len(self.seed_string) - 1)
                new_character = self.seed_string[random_index]
            # if not randomize seed string, reference source string using seed_character_index counter
            else:
                new_character = self.seed_string[self.seed_character_index]
                self.seed_character_index += 1
                if self.seed_character_index >= len(self.seed_string):
                    self.seed_character_index = 0
            # add the new character to the segment characters list
            self.characters.append(new_character)

    def set_colors(self):
        # populate colors list with color a
        for character in range(self.length):
            self.character_colors.append((self.color_a[0], self.color_a[1], self.color_a[2]))
        # re-populate with transitional colors at either end of list
        # track the transitional rgb starting with the first color to be set on either end of list / stack
        rgb_bottom = [self.color_b[0], self.color_b[1], self.color_b[2]] # had issues here when passing lists 1:1
        rgb_top = [self.bg_color[0], self.bg_color[1], self.bg_color[2]]
        # loop for number of transitional characters defined in config
        for character in range(self.transition_length):
            character_inv = (character + 1) * -1 # +1 and invert for colors list top down index
            # loop for r, g, b values
            for value in range(3):
                # bottom of stack up
                value_delta_bottom = self.color_a[value] - self.color_b[value]
                change_delta_bottom = round(value_delta_bottom / self.transition_length)
                rgb_bottom[value] = rgb_bottom[value] + change_delta_bottom
                # top of stack down
                value_delta_top = self.color_a[value] - self.bg_color[value]
                change_delta_top = round(value_delta_top / self.transition_length)
                rgb_top[value] = rgb_top[value] + change_delta_top
            # set the character color list items to the new rgb values
            self.character_colors[character] = (rgb_bottom[0], rgb_bottom[1], rgb_bottom[2])
            self.character_colors[character_inv] = (rgb_top[0], rgb_top[1], rgb_top[2])

#-------------------------------------------------------------------------------------------------------
class Renderer:
    def __init__(self, image_width: int, image_height: int, font_face: str, font_size: int, background_color: list):
        self.image_width = image_width # output image canvas width
        self.image_height = image_height # output image canvas height
        self.bg_color = (background_color[0], background_color[1], background_color[2], ) # output image background fill color (rgb)
        self.font: object = ImageFont.truetype(font_face, font_size) # stores font data
        self.image: object = None # stores image data
        self.draw: object = None
        self.new_image()

    def new_image(self):
        # over-write current image object data with background color
        self.image = Image.new('RGB', (self.image_width, self.image_height), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

    def draw_character(self, character: str, pixel_x: int, pixel_y: int, color: str):
        # render text at pixel x,y coords
        self.draw.text((pixel_x, pixel_y), character, fill = color, font = self.font)

    def save_image(self, file_name: str):
        # set path and save image data to file as png
        file_extension = "png"
        save_path = f"{file_name}.{file_extension}"
        self.image.save(save_path)

#-------------------------------------------------------------------------------------------------------
class SegmentHandler:
    def __init__(self, grid_object: object, min_separation: int, max_separation: int):
        self.grid = grid_object
        self.segment_pool: object = []
        self.column_spawn_states: bool = []
        self.min_separation = min_separation
        self.max_separation = max_separation
        self.column_speeds: int = []
        self.init_spawn_states()
        self.set_column_speeds()

    def set_column_speeds(self):
        # loop for columns in grid
        for column in range(self.grid.total_columns):
            # set 3 speed levels from random range 1-3
            self.column_speeds.append(random.randint(1, 3))

    def init_spawn_states(self):
        # for each column, add an item to list with value True
        for column in range(self.grid.total_columns):
            self.column_spawn_states.append(True)

    def iterate(self):
        # method called in main loop
        self.check_spawns()
        self.spawn_segments()
        self.cycle_segments()
        self.cleanup_segments()

    def check_spawns(self):
        # set all spawn states true
        for column in range(len(self.column_spawn_states)):
            self.column_spawn_states[column] = True
        # cycle through segments in pool, if segment length + lead character is not far enough from row 0, set column spawn state false
        for segment in range(len(self.segment_pool)):
            clearance = self.segment_pool[segment].length + self.segment_pool[segment].separation
            column_id = self.segment_pool[segment].column_id
            row_id = self.segment_pool[segment].row_id
            if row_id < clearance:
                self.column_spawn_states[column_id] = False

    def spawn_segments(self):
        # loop for columns in grid, if spawn state is true create new segment and add it to pool
        for column in range(self.grid.total_columns):
            if self.column_spawn_states[column] is True:
                new_segment = define_segment()
                new_segment.column_id = column
                new_segment.row_id = -1 # cycle_segments will +1 before image output
                new_segment.separation = random.randint(self.min_separation, self.max_separation)
                self.segment_pool.append(new_segment)

    def cycle_segments(self):
        # loop for segments in pool, call new character and move segment row id + 1
        for segment in range(len(self.segment_pool)):
            for cycle in range(self.column_speeds[self.segment_pool[segment].column_id]):
                self.segment_pool[segment].new_character()
                self.segment_pool[segment].row_id += 1

    def cleanup_segments(self):
        # for segments in pool, if lead character row + length > total grid rows, remove from pool
        for segment in range(len(self.segment_pool)):
            if (self.grid.total_rows - self.segment_pool[segment].length) > self.grid.total_rows:
                self.segment_pool.pop(segment)
