import math
def yanjing(px_list,py_list,mtx):
    pixel_to_mm= 1 / mtx[0, 0]
    eye_left_out_x = px_list[33]
    eye_left_out_y = py_list[33]
    eye_left_in_x = px_list[133]
    eye_left_in_y = py_list[133]
    eye_right_in_x = px_list[362]
    eye_right_in_y = py_list[362]

    zuoyan_chang = math.sqrt((eye_left_out_x - eye_left_in_x) ** 2 + (eye_left_out_y - eye_left_in_y) ** 2) * pixel_to_mm
    yanju = math.sqrt((eye_left_in_x - eye_right_in_x) ** 2 + (eye_left_in_y - eye_right_in_y) ** 2) * pixel_to_mm
    return zuoyan_chang, yanju