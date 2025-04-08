import cv2
import numpy as np

# 카메라 매트릭스 및 왜곡 계수
camera_matrix = np.array([[1959.4927, 0.0, 556.720408],
                          [0.0, 1842.37399, 437.56401],
                          [0.0, 0.0, 1.0]])
dist_coeffs = np.array([0.2785417, 0.38471694, -0.02475514, -0.13305862, -0.89482082])

# 영상 열기
video_path = "chessboard2.avi"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("영상을 열 수 없습니다:", video_path)
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("undistorted_output.mp4", fourcc, fps, (width, height))

print("렌즈 왜곡 보정 중... (최대 100프레임만 저장)")

frame_count = 0
max_frames = 100

while frame_count < max_frames:
    ret, frame = cap.read()
    if not ret:
        break
    undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs)
    out.write(undistorted)
    frame_count += 1

cap.release()
out.release()

print(f"완료! {frame_count}개의 프레임을 저장했습니다. → undistorted_output.mp4")