import math
def santing(px_list,py_list,mtx):
    pixel_to_mm = 1 / mtx[0, 0]
    fajixian_x = px_list[10]
    fajixian_y = py_list[10]
    yintang_x = px_list[72]
    yintang_y = py_list[72]
    bidi_x = px_list[164]
    bidi_y = py_list[164]
    xiabajian_x = px_list[152]
    xiabajian_y = py_list[152]

    shangting = math.sqrt(((fajixian_x - yintang_x) ** 2 + (fajixian_y - yintang_y) ** 2)) * pixel_to_mm
    zhongting = math.sqrt((yintang_x - bidi_x) ** 2 + (yintang_y - bidi_y) ** 2) * pixel_to_mm
    xiating = math.sqrt((bidi_x - xiabajian_x) ** 2 + (bidi_y - xiabajian_y) ** 2) * pixel_to_mm
    return shangting, zhongting, xiating