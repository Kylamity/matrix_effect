# matrix.py

import os, time
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


def render_segments(is_alpha_mask = False):
    for segment in range(len(segmentHandler.segment_pool)):
        print_row = segmentHandler.segment_pool[segment].row_id
        for char in range(len(segmentHandler.segment_pool[segment].characters)):
            c = (char + 1) * -1
            if print_row in range(grid.total_rows):
                renderer.draw_character(
                    character = segmentHandler.segment_pool[segment].characters[c],
                    pixel_x = grid.column_coords[segmentHandler.segment_pool[segment].column_id],
                    pixel_y = grid.row_coords[print_row],
                    color = segmentHandler.segment_pool[segment].character_colors[char]
                )
            print_row -= 1


def main():
    # check config globals are compatible
    if not sanitize_config():
        return None

    # if output dir doesn't exist, create
    if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    timestamp = time.time()

    # perform pre-iteration cycles
    if PRE_ITERATE:
        print(f"Processing {PRE_ITERATE} pre-iterations...")
        for pre_iteration in range(PRE_ITERATE):
            segmentHandler.iterate()
        duration = round(time.time() - timestamp, 1)
        print(f"Completed in {duration} sec")
        timestamp = time.time()

    # perform output iteration cycles
    print(f"Processing output iterations...")
    for output_iteration in range(OUTPUT_ITERATIONS):
        iteration_actual = output_iteration + 1
        segmentHandler.iterate()
        render_segments()
        full_image_name = f"{IMAGE_NAME}_{iteration_actual}_{IMAGE_WIDTH}x{IMAGE_HEIGHT}"
        save_path = os.path.join(OUTPUT_DIR, full_image_name)
        renderer.save_image(save_path)
        renderer.new_image()
        # single / sequence output mode logic
        if SAVE_ALL:
            print(f"Iteration {iteration_actual} of {OUTPUT_ITERATIONS} saved")
        else:
            print(f"Iteration saved")
            break

    duration = round(time.time() - timestamp, 1)
    print(f"Completed in {duration} sec")
    print("\nExiting")


if __name__ == '__main__':
    main()