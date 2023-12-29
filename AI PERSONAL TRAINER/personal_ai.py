import math

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import threading
import queue

model_path="pose_landmarker_full.task"


class PersonalAI:
    def __init__(self, file_name="The Perfect Push Up _ Do it right! - YouTube e mais 13 páginas - Pessoal — Microsoft​ Edge 2023-12-29 02-38-27.mp4"):
        self.file_name = file_name
        self.image_q = queue.Queue()
        model_path="pose_landmarker_full.task"

        self.options = python.vision.PoseLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=model_path),
            running_mode=python.vision.RunningMode.VIDEO
        )

    # achar o angulo entre 3 pontos
    def find_angle(self, frame, landmarks, p1, p2, p3, draw: bool):
        land = landmarks.pose_landmarks[0]
        # altura, largura e profundidade
        h, w, c = frame.shape
        x1, y1 = (land[p1].x, land[p1].y)
        x2, y2 = (land[p2].x, land[p2].y)
        x3, y3 = (land[p3].x, land[p3].y)

        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
        # angulo do meio
        position = (int(x2 * w + 10), int(y2 * h + 10))
        if draw:
            frame = cv2.putText(frame, str(int(angle)), position, cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)

        return frame, angle

    def draw_landmarks_on_image(self, rgb_image, detection_result):
      pose_landmarks_list = detection_result.pose_landmarks
      annotated_image = np.copy(rgb_image)

      # Loop through the detected poses to visualize.
      for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
          landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
          annotated_image,
          pose_landmarks_proto,
          solutions.pose.POSE_CONNECTIONS,
          solutions.drawing_styles.get_default_pose_landmarks_style())
      return annotated_image

    def process_video(self, draw, display):

        with python.vision.PoseLandmarker.create_from_options(self.options) as landmarker:
            cap = cv2.VideoCapture(self.file_name)
            # timestamp
            calc_ts = [0.0]
            while (cap.isOpened()):
                ret, frame = cap.read()
                fps = cap.get(cv2.CAP_PROP_FPS)

                if ret:
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                    calc_ts.append(int(calc_ts[-1] + 1000/fps))

                    detection_result = landmarker.detect_for_video(mp_image, calc_ts[-1])
                    # ombro esquerdo do corpo
                    # detection_result.pose_landmarks[0][11]
                    # x=0.22 (22% da quantidade de pixels (22% de 900px))

                    if draw:
                        frame = self.draw_landmarks_on_image(frame, detection_result)

                    if display:
                        cv2.imshow('Frame', frame)
                        # Press Q to exit
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break

                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    # put into queue the frame, landmarks, timestamp
                    self.image_q.put((frame, detection_result, calc_ts[-1]))
                else:
                    break

        self.image_q.put((frame, landmarker, "done"))
        cap.release()
        cv2.destroyAllWindows()

    def run(self, draw: bool, display=False):
        t1 = threading.Thread(target=self.process_video, args=(draw, display))
        t1.start()


if __name__ == "__main__":
    personalAI = PersonalAI()
    personalAI.process_video(True, True)
