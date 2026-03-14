import cv2
import mediapipe as mp
def facialkeypoints (cap,mtx,dist):
    px_list=[]
    py_list=[]
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles


    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,  # 静态图片模式：False表示视频流，True表示静态图片
        max_num_faces=1,  # 最多检测人脸数量
        refine_landmarks=True,  # 精细化关键点（增加嘴唇、眼睛等区域的关键点）
        min_detection_confidence=0.5,  # 检测置信度阈值
        min_tracking_confidence=0.5)  # 跟踪置信度阈值

    while True:
        ret, frame = cap.read()
        h, w = frame.shape[:2]
        new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        frame_undist = cv2.undistort(frame, mtx, dist, None, new_mtx)
        results = face_mesh.process(frame_undist)
        if results.multi_face_landmarks:
            face_landmarks = list(results.multi_face_landmarks)[0]
            mp_drawing.draw_landmarks(
                image=frame_undist,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp_drawing.DrawingSpec(
                    color=(0, 255, 0),  # 绿色
                    thickness=1,  # 粗细
                    circle_radius=1  # 点大小
                ),
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
            # 绘制面部轮廓
            mp_drawing.draw_landmarks(
                image=frame_undist,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(
                    color=(0, 255, 0),  # 绿色
                    thickness=1,  # 粗细
                    circle_radius=1  # 点大小
                ),
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
            # 绘制眼睛
            mp_drawing.draw_landmarks(
                image=frame_undist,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=mp_drawing.DrawingSpec(
                    color=(0, 255, 0),  # 绿色
                    thickness=1,
                    circle_radius=1  # 点大小
                ),
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
        cv2.imshow('实时坐标', cv2.resize(frame_undist, (800, 600)))
        key = cv2.waitKey(1) & 0xFF
        height, width, _ = frame.shape
        if key == 27:
            for landmark in face_landmarks.landmark:
                px = int(landmark.x * width)
                py = int(landmark.y * height)
                px_list.append(px)
                py_list.append(py)
            break
    return px_list, py_list,frame