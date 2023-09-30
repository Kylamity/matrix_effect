# config.py

# Image
IMAGE_NAME = "image" # output file name "[IMAGE_NAME]_[IMAGE_WIDTH]x[IMAGE_HEIGHT]
IMAGE_WIDTH = 2560
IMAGE_HEIGHT = 1440
BACKGROUND_COLOR = 'black'
SKIP_ITERATIONS = 2500 # disable image output for this many iterations
STOP_ITERATION = 500 # total iterations that will be output
SAVE_ALL = True # if true, only the final iteration will be saved
OUTPUT_DIR = "output"

# Character Segments
SEED_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()=+[]{};:<>/?"
RANDOMIZE_STRING = True # if true, segments will ignore seed string order
BASE_COLOR = [0, 166, 255] # [R, G, B] 0 - 255
ACCENT_COLOR = [255, 255, 255] # [R, G, B] 0 - 255
FONT_FACE = 'consola.ttf'
FONT_SIZE = 20 # does not change spacing
SPACING_X = 14 # grid horizontal / column spacing
SPACING_Y = 18 # grid vertical / row spacing
TRANSITION_LENGTH = 10 # length of color transitions at beginning and end of segments, keep this <= SEGMENT_LENGTH_DEVIATION * 2!!!
SEGMENT_LENGTH = 50 # typical character length for segments
SEGMENT_LENGTH_DEVIATION = 30 # +/- limit for segment character length randomizer, keep <= SEGMENT_LENGTH / 2!!!
SEGMENT_SEPARATION = 50 # typical distance separating segments in same column
SEGMENT_SEPARATION_DEVIATION = 25 # +/- limit for separation randomizer, keep <= SEGMENT_SEPARATION / 2!!!
