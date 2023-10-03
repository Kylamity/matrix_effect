# config.py

# Image
IMAGE_NAME = "image" # prefixes output file name
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
BACKGROUND_COLOR = [0, 0, 0] # [R, G, B] 0 - 255
PRE_ITERATE = 1000 # will iterate for this value before beginning output iterations
OUTPUT_ITERATIONS = 500 # total output images / iterations that will be saved
SAVE_ALL = True # if false, only the final output iteration will be saved
OUTPUT_DIR = "images" # supports relative path, path must exist

# Character Segments
SEED_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()=+[]{};:<>/?"
RANDOMIZE_STRING = True # if true, segments will ignore seed string order
BASE_COLOR = [58, 143, 186] # [R, G, B] 0 - 255 (segment "body" color)
ACCENT_COLOR = [255, 255, 255] # [R, G, B] 0 - 255 (segment "leader" color)
FONT_FACE = 'consola.ttf'
FONT_SIZE = 22 # should be adjusted with spacing
GRID_COLUMN_SPACING = 16 # grid column spacing
GRID_ROW_SPACING = 20 # grid row spacing
TRANSITION_LENGTH = 8 # length of segment color transitions, should be < 1/2 SEGMENT_LENGTH_MIN
SEGMENT_LENGTH_MIN = 20 # upper limit for segment length randomization, should be > 2 * TRANSITION_LENGTH
SEGMENT_LENGTH_MAX = 100 # upper limit for segment length randomization
SEGMENT_SEPARATION_MIN = 20 # upper limit for separation randomization
SEGMENT_SEPARATION_MAX = 100 # lower limit for separation randomization


