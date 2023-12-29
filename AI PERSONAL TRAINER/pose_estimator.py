# import cv2
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from mediapipe import solutions
# from mediapipe.framework.formats import landmark_pb2
# import numpy as np
#
#
# file_name="The Perfect Push Up _ Do it right! - YouTube e mais 13 páginas - Pessoal — Microsoft​ Edge 2023-12-29 02-38-27.mp4"
# model_path="pose_landmarker_full.task"
#
#
# def draw_landmarks_on_image(rgb_image, detection_result):
#   pose_landmarks_list = detection_result.pose_landmarks
#   annotated_image = np.copy(rgb_image)
#
#   # Loop through the detected poses to visualize.
#   for idx in range(len(pose_landmarks_list)):
#     pose_landmarks = pose_landmarks_list[idx]
#
#     # Draw the pose landmarks.
#     pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
#     pose_landmarks_proto.landmark.extend([
#       landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
#     ])
#     solutions.drawing_utils.draw_landmarks(
#       annotated_image,
#       pose_landmarks_proto,
#       solutions.pose.POSE_CONNECTIONS,
#       solutions.drawing_styles.get_default_pose_landmarks_style())
#   return annotated_image
#
#
# options = python.vision.PoseLandmarkerOptions(
#     base_options=python.BaseOptions(model_asset_path=model_path),
#     running_mode=python.vision.RunningMode.VIDEO
# )
#
# with python.vision.PoseLandmarker.create_from_options(options) as landmarker:
#     cap = cv2.VideoCapture(file_name)
#     # timestamp
#     calc_ts = [0.0]
#     while (cap.isOpened()):
#         ret, frame = cap.read()
#         fps = cap.get(cv2.CAP_PROP_FPS)
#
#         if ret:
#             mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
#             calc_ts.append(int(calc_ts[-1] + 1000/fps))
#
#             detection_result = landmarker.detect_for_video(mp_image, calc_ts[-1])
#
#             frame = draw_landmarks_on_image(frame, detection_result)
#             cv2.imshow('Frame', frame)
#
#             # ombro esquerdo do corpo
#             # detection_result.pose_landmarks[0][11]
#             # x=0.22 (22% da quantidade de pixels (22% de 900px))
#
#             # Press Q to exit
#             if cv2.waitKey(25) & 0xFF == ord('q'):
#                 break
#         else:
#             break
#
# cap.release()
# cv2.destroyAllWindows()