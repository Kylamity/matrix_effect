# config.py

# Image
IMAGE_NAME = "image" # prefixes output file name
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
BACKGROUND_COLOR = [0, 0, 0, 0] # [R, G, B, A] 0 - 255
PRE_ITERATE = 500 # will iterate for this value before beginning output iterations
OUTPUT_ITERATIONS = 500 # total output images / iterations that will be saved
SAVE_ALL = False # if false, saves only single image after pre-iterations complete
SAVE_ALPHA = False # if true will save as 32 bit RGBA
OUTPUT_DIR = "images"  # supports relative path, path must exist

# Character Segments
#SEED_STRING = """ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()=+[]{};:<>/?""" # for standard fonts
SEED_STRING = """abcdefghijklmnopqrstuvwxyz!"#%&()~+-/*=.,{}?$<>:""" # for 'matrix code nfi.ttf' font
RANDOMIZE_STRING = True # if true, segments will ignore seed string order
BASE_COLOR = [0, 150, 0, 255] # [R, G, B, A] 0 - 255 (segment "body" color)
ACCENT_COLOR = [255, 255, 255, 255] # [R, G, B, A] 0 - 255 (segment "leader" color)
#FONT_FACE = 'consola.ttf'
FONT_FACE = 'matrix code nfi.ttf' # must have font installed
FONT_SIZE = 30 # should be adjusted with spacing
GRID_COLUMN_SPACING = 18 # grid column spacing
GRID_ROW_SPACING = 28 # grid row spacing
TRANSITION_LENGTH_MIN = 5 # min length of dynamic segment color transitions
SEGMENT_LENGTH_MIN = 30 # upper limit for segment length randomization
SEGMENT_LENGTH_MAX = 100 # upper limit for segment length randomization
SEGMENT_SEPARATION_MIN = 20 # upper limit for separation randomization
SEGMENT_SEPARATION_MAX = 200 # lower limit for separation randomization