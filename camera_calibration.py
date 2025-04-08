import cv2
import numpy as np

# (예: 감지에 성공했던 사이즈로 설정)
chessboard_size = (7, 5)

# 체스보드의 각 코너 위치 정의
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

objpoints = []  # 3D world points
imgpoints = []  # 2D image points

cap = cv2.VideoCapture("chessboard2.avi")
if not cap.isOpened():
    print("영상 열기 실패")
    exit()

frame_count = 0
success_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret_cb, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    if ret_cb:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)
        success_count += 1

cap.release()

print(f"총 {frame_count}프레임 중 {success_count}개에서 체스보드 감지 성공.")

if len(objpoints) > 0:
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)
    print("Camera matrix:\n", camera_matrix)
    print("Distortion coefficients:\n", dist_coeffs)

    # 평균 재투영 오차 계산
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error
    rmse = total_error / len(objpoints)
    print(f"RMSE: {rmse:.4f}")
else:
    print("Calibration failed: No valid chessboard detections.")