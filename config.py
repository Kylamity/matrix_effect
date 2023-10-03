# config.py

# Image
IMAGE_NAME = "image" # prefixes output file name
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
BACKGROUND_COLOR = [255, 255, 255] # [R, G, B] 0 - 255
PRE_ITERATE = 500 # will iterate for this value before beginning output iterations
OUTPUT_ITERATIONS = 500 # total output images / iterations that will be saved
SAVE_ALL = False # if true, only the final output iteration will be saved
OUTPUT_DIR = "output" # supports relative path, path must exist

# Character Segments
SEED_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()=+[]{};:<>/?"
RANDOMIZE_STRING = True # if true, segments will ignore seed string order, currently only working in True state***********
BASE_COLOR = [0, 0, 0] # [R, G, B] 0 - 255 (segment "body" color)
ACCENT_COLOR = [200, 0, 0] # [R, G, B] 0 - 255 (segment "leader" color)
FONT_FACE = 'consola.ttf'
FONT_SIZE = 20 # should be adjusted with spacing
GRID_COLUMN_SPACING = 14 # grid column spacing
GRID_ROW_SPACING = 18 # grid row spacing
TRANSITION_LENGTH = 12 # length of segment color transitions, should be < 1/2 SEGMENT_LENGTH_MIN
SEGMENT_LENGTH_MIN = 25 # upper limit for segment length randomization, should be > 2 * TRANSITION_LENGTH
SEGMENT_LENGTH_MAX = 50 # upper limit for segment length randomization
SEGMENT_SEPARATION_MIN = 10 # upper limit for separation randomization
SEGMENT_SEPARATION_MAX = 50 # lower limit for separation randomization

