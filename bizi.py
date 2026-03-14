import math
def bizi(px_list,py_list,mtx):
    pixel_to_mm = 1 / mtx[0, 0]
    shangen_x = px_list[168]
    shangen_y = py_list[168]
    bijian_x = px_list[4]
    bijian_y = py_list[4]
    biyi_left_x = px_list[207]
    biyi_left_y = py_list[207]
    biyi_right_x = px_list[427]
    biyi_right_y = py_list[427]

    bigao = math.sqrt((shangen_x - bijian_x) ** 2 + (shangen_y - bijian_y) ** 2) * pixel_to_mm
    biyi_kuan = math.sqrt((biyi_left_x - biyi_right_x) ** 2 + (biyi_left_y - biyi_right_y) ** 2) * pixel_to_mm
    return bigao, biyi_kuan