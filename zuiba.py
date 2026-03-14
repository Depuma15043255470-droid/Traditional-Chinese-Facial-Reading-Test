import math
def zuiba(px_list,py_list,mtx):
    pixel_to_mm= 1 / mtx[0, 0]
    mouth_left_x = px_list[61]
    mouth_left_y = py_list[61]
    mouth_right_x = px_list[291]
    mouth_right_y = py_list[291]
    zuikuan = math.sqrt((mouth_left_x - mouth_right_x) ** 2 + (mouth_left_y - mouth_right_y) ** 2) * pixel_to_mm
    return zuikuan