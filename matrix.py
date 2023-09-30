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
    column_spacing = SPACING_X,
    row_spacing = SPACING_Y
)
segmentHandler: object = SegmentHandler(
    grid_object = grid,
    typical_separation = SEGMENT_SEPARATION,
    segment_separation_deviation = SEGMENT_SEPARATION_DEVIATION
)


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
    timestamp = time.time()
    print("Processing...")

    for iteration in range(STOP_ITERATION + SKIP_ITERATIONS):
        iteration_actual = iteration - SKIP_ITERATIONS
        segmentHandler.iterate()
        if SAVE_ALL or STOP_ITERATION == iteration_actual:
            if iteration > SKIP_ITERATIONS:
                render_segments()
                renderer.save_image(f'{IMAGE_NAME}_{iteration_actual}_{IMAGE_WIDTH}x{IMAGE_HEIGHT}')
                renderer.new_image()
                print(f"Iteration {iteration_actual} saved")

    duration = round(time.time() - timestamp, 1)
    print(f"\nCompleted in {duration} sec, Exiting.")


if __name__ == '__main__':
    main()