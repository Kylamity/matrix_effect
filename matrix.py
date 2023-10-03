# matrix.py

import time
from classes import *
from config import *

renderer: object = Renderer(
    image_width = IMAGE_WIDTH,
    image_height = IMAGE_HEIGHT,
    font_face = FONT_FACE,
    font_size = FONT_SIZE,
    background_color = BACKGROUND_COLOR
)
grid: object = Grid(
    canvas_width = IMAGE_WIDTH,
    canvas_height = IMAGE_HEIGHT,
    column_spacing = GRID_COLUMN_SPACING,
    row_spacing = GRID_ROW_SPACING
)
segmentHandler: object = SegmentHandler(
    grid_object = grid,
    min_separation = SEGMENT_SEPARATION_MIN,
    max_separation = SEGMENT_SEPARATION_MAX
)


def sanitize_config():
    rejections: str = []

    if TRANSITION_LENGTH * 2 >= SEGMENT_LENGTH_MIN:
        rejections.append("TRANSITION_LENGTH must be less than half of SEGMENT_LENGTH_MIN")
    if SEGMENT_LENGTH_MIN > SEGMENT_LENGTH_MAX:
        rejections.append("SEGMENT_LENGTH_MIN must be less than SEGMENT_LENGTH_MAX")
    if SEGMENT_SEPARATION_MIN > SEGMENT_SEPARATION_MAX:
        rejections.append("SEGMENT_SEPARATION_MIN must be less than SEGMENT_SEPARATION_MAX")

    rejection_count = len(rejections)
    if rejection_count:
        print("\nConfig Error:")
        for rejection in range(rejection_count):
            print(f"    {rejections[rejection]}")
        return False

    return True


def render_segments():
    for segment in range(len(segmentHandler.segment_pool)):
        print_row = segmentHandler.segment_pool[segment].row_id
        for char in range(len(segmentHandler.segment_pool[segment].characters)):
            if print_row in range(grid.total_rows):
                renderer.draw_character(
                    character = segmentHandler.segment_pool[segment].characters[char],
                    pixel_x = grid.column_coords[segmentHandler.segment_pool[segment].column_id],
                    pixel_y = grid.row_coords[print_row],
                    color = segmentHandler.segment_pool[segment].character_colors[char]
                )
            print_row -= 1


def main():
    if not sanitize_config():
        return None

    if PRE_ITERATE:
        timestamp = time.time()
        print(f"Processing {PRE_ITERATE} pre-iterations...")
        for pre_iteration in range(PRE_ITERATE):
            segmentHandler.iterate()

        duration = round(time.time() - timestamp, 1)
        print(f"Completed in {duration} sec")

    timestamp = time.time()
    if SAVE_ALL:
        print(f"Processing {OUTPUT_ITERATIONS} output iterations...")
    else:
        print(f"Processing to output iteration {OUTPUT_ITERATIONS}")
    for output_iteration in range(OUTPUT_ITERATIONS):
        iteration_actual = output_iteration + 1
        segmentHandler.iterate()
        if SAVE_ALL or iteration_actual == OUTPUT_ITERATIONS:
            render_segments()
            renderer.save_image(f'{IMAGE_NAME}_{iteration_actual}_{IMAGE_WIDTH}x{IMAGE_HEIGHT}')
            renderer.new_image()
            print(f"Iteration {iteration_actual} saved")

    duration = round(time.time() - timestamp, 1)
    print(f"Completed in {duration} sec, Exiting.")


if __name__ == '__main__':
    main()