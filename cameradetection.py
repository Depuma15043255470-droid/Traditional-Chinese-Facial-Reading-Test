import cv2
import numpy as np
def cameradetection (cap):
  frame_list = []
  save_count = 0
  while True:
    ret, frame = cap.read()  # 帧数据
    cv2.imshow("Laptop Camera", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC退出
      break
    if key == 32:
      frame_list.append(frame.copy())
      save_count += 1
      print(f"第{save_count}帧已存入列表，当前列表长度：{len(frame_list)}")
  pattern_size = (9,6)
  objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
  objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
  imgpoints = []  # 图像中的2D点
  objpoints = []  # 真实3D点
  mtx_list = []
  dist_list = []
  for img in frame_list:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# 转换为灰度图
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
    if ret:
      objpoints.append(objp)
      corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                          criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

      imgpoints.append(corners_refined)
      ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
      mtx_list.append(mtx)
      dist_list.append(dist)
  return mtx_list,dist_list