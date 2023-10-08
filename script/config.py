# config.py

# Image
IMAGE_NAME = "image" # prefixes output file name
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
BACKGROUND_COLOR = [0, 0, 0] # [R, G, B] 0 - 255
PRE_ITERATE = 500 # will iterate for this value before beginning output iterations
OUTPUT_ITERATIONS = 500 # total output images / iterations that will be saved
SAVE_ALL = True # if false, saves only single image after pre-iterations complete
OUTPUT_DIR = "images"  # supports relative path, path must exist

# Character Segments
#SEED_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()=+[]{};:<>/?"
SEED_STRING = """abcdefghijklmnopqrstuvwxyz!"#%&()~+-/*=.,{}?$<>:"""
RANDOMIZE_STRING = True # if true, segments will ignore seed string order
BASE_COLOR = [0, 150, 0] # [R, G, B] 0 - 255 (segment "body" color)
ACCENT_COLOR = [255, 255, 255] # [R, G, B] 0 - 255 (segment "leader" color)
#FONT_FACE = 'consola.ttf'
FONT_FACE = 'matrix code nfi.ttf' # must have font installed
FONT_SIZE = 24 # should be adjusted with spacing
GRID_COLUMN_SPACING = 18 # grid column spacing
GRID_ROW_SPACING = 22 # grid row spacing
TRANSITION_LENGTH_MIN = 6 # min length of dynamic segment color transitions
SEGMENT_LENGTH_MIN = 50 # upper limit for segment length randomization
SEGMENT_LENGTH_MAX = 100 # upper limit for segment length randomization
SEGMENT_SEPARATION_MIN = 25 # upper limit for separation randomization
SEGMENT_SEPARATION_MAX = 250 # lower limit for separation randomization
