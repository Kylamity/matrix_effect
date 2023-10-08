# classes.py

import random, math
from PIL import ImageFont, Image, ImageDraw
from config import *

def define_segment():
        segment: object = CharacterSegment(
            seed_string = SEED_STRING,
            randomize_string = RANDOMIZE_STRING,
            transition_length = TRANSITION_LENGTH_MIN,
            min_length = SEGMENT_LENGTH_MIN,
            max_length = SEGMENT_LENGTH_MAX
        )
        return segment

#-------------------------------------------------------------------------------------------------------
class Grid:
    def __init__(self, canvas_width: int, canvas_height: int, column_spacing: int, row_spacing: int):
        self.total_columns: int = None # total columns in grid
        self.total_rows: int = None # total rows in grid
        self.column_coords: list[int] = [] # pixel coordinates for each column
        self.row_coords: list[int] = [] # pixel coordinates for each row
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
    def __init__(self, seed_string: str, randomize_string: bool, transition_length: int, min_length: int, max_length: int):
        self.seed_string = seed_string # character types segment can contain
        self.randomize_string = randomize_string # if new_character() will randomize seed string
        self.transition_length = transition_length # number of transitionally colored characters
        self.length = random.randint(min_length, max_length) # total simultaneous characters allowed in segment
        self.column_id: int = None # column number of leading character
        self.row_id: int = None # row number of leading character
        self.characters: list[str] = [] # characters segment currently contains ([0] = oldest character)
        self.character_colors: list[int] = [] # colors of characters in characters list
        self.seed_character_index = random.randint(0, (len(self.seed_string) - 1)) # tracks current position in seed_string when seed not randomized
        self.speed = 1 # set by handler at spawn

    def new_character(self):
        seed_length = len(self.seed_string)
        # if randomize seed string, reference source string using random as index
        if self.randomize_string is True:
            index = random.randint(0, seed_length - 1)
        # if not randomize seed string, reference source string using seed_character_index counter
        else:
            index = self.seed_character_index
            self.seed_character_index += 1
            if self.seed_character_index >= seed_length:
                self.seed_character_index = 0
        # add the new character to the segment characters list
        new_character = self.seed_string[index]
        self.characters.append(new_character)
        if len(self.characters) > self.length:
            self.characters.pop(0)

#-------------------------------------------------------------------------------------------------------
class CharacterSegmentRGB:
    def __init__(self, main_color: list[int], leader_color: list[int], background_color: list[int], min_transition_length: int):
        self.color_a = main_color
        self.color_b = leader_color
        self.bg_color = background_color
        self.min_trans_length = min_transition_length

    def make_rgb_list(self, segment_length: int, segment_speed_mult: int):
        rgb_colors_list: list[int] = []
        for character in range(segment_length):
            rgb_colors_list.append((self.color_a[0], self.color_a[1], self.color_a[2]))
        return self.set_transitional_colors(rgb_colors_list, segment_speed_mult)

    def set_transitional_colors(self, rgb_colors_list, speed_mult):
        rgb_colors_list = rgb_colors_list
        rgb_top = [self.bg_color[0], self.bg_color[1], self.bg_color[2]]
        rgb_bottom = [self.color_b[0], self.color_b[1], self.color_b[2]]
        dyn_length = self.min_trans_length * speed_mult
        transition_multi = 1 / dyn_length
        for character in range(dyn_length):
            character_inv = (character + 1) * -1 # +1 and invert to address list top down
            rgb_bottom = self.blend_rgb_values(rgb_bottom, self.color_b, transition_multi)
            rgb_top = self.blend_rgb_values(rgb_top, self.bg_color, transition_multi)
            rgb_colors_list[character] = (rgb_bottom[0], rgb_bottom[1], rgb_bottom[2])
            rgb_colors_list[character_inv] = (rgb_top[0], rgb_top[1], rgb_top[2])
        rgb_colors_list[0] = (255, 255, 255)
        return rgb_colors_list

    def blend_rgb_values(self, rgb_1, rgb_2, transition_multi):
        rgb_out = [rgb_1[0], rgb_1[1], rgb_1[2]]
        # loop for r, g, b values
        for value in range(3):
            difference = self.color_a[value] - rgb_2[value]
            change_delta = round(difference * transition_multi)
            rgb_out[value] += change_delta
        return [rgb_out[0], rgb_out[1], rgb_out[2]]

#-------------------------------------------------------------------------------------------------------
class Renderer:
    def __init__(self, image_width: int, image_height: int, font_face: str, font_size: int, background_color: list[int]):
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

    def save_image(self, file_path: str):
        # set path and save image data to file as png
        ext_path = f'{file_path}.png'
        self.image.save(ext_path)

#-------------------------------------------------------------------------------------------------------
class CharacterSegmentHandler:
    def __init__(self, grid_object: object, segment_rgb_object: object, min_separation: int, max_separation: int):
        self.grid = grid_object
        self.rgb_object = segment_rgb_object
        self.segment_pool: object = []
        self.column_spawn_states: bool = []
        self.min_separation = min_separation
        self.max_separation = max_separation
        self.column_speeds: int = []
        self.set_column_speeds()

    def set_column_speeds(self):
        # loop for number of columns in grid, set random speed value from range 1-3
        last_speed = None
        for column in range(self.grid.total_columns):
            random_speed = random.randint(1, 3)
            while random_speed == last_speed:
                random_speed = random.randint(1, 3)
            else:
                self.column_speeds.append(random_speed)
            last_speed = random_speed

    def iterate(self):
        # method called in main loop
        self.init_spawn_states()
        self.check_spawns()
        self.spawn_segments()
        self.cycle_segments()
        self.cleanup_segments()

    def init_spawn_states(self):
        # for each column, add or set list item True
        if len(self.column_spawn_states):
            for column in range(self.grid.total_columns):
                self.column_spawn_states[column] = True
        else:
            for column in range(self.grid.total_columns):
                self.column_spawn_states.append(True)

    def check_spawns(self):
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
                new_segment.speed = self.column_speeds[column]
                new_rgb_colors_list = self.rgb_object.make_rgb_list(new_segment.length, self.column_speeds[column])
                new_segment.character_colors = new_rgb_colors_list
                self.segment_pool.append(new_segment)

    def cycle_segments(self):
        # loop for segments in pool, call new character and move segment row id + 1
        for segment in range(len(self.segment_pool)):
            for column in range(self.column_speeds[self.segment_pool[segment].column_id]):
                self.segment_pool[segment].new_character()
                self.segment_pool[segment].row_id += 1

    def cleanup_segments(self):
        # for segments in pool, if lead character row + length > total grid rows, remove from pool
        cull_segments = []
        for segment in range(len(self.segment_pool)):
            if (self.grid.total_rows - self.segment_pool[segment].length) > self.grid.total_rows:
                cull_segments.append(segment)
        for segment in range(len(cull_segments)):
            self.segment_pool.pop(segment)