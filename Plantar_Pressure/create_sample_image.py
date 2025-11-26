import cv2
import numpy as np
import os

# 현재 디렉토리에 직접 생성
output_dir = 'test_foot_data'
os.makedirs(output_dir, exist_ok=True)

# 256x256 크기의 샘플 발 이미지 생성
height, width = 256, 256
image = np.zeros((height, width, 3), dtype=np.uint8)

# 배경을 흰색으로
image[:] = (255, 255, 255)

# 발 모양 생성
cv2.ellipse(image, (128, 200), (60, 40), 0, 0, 360, (50, 50, 50), -1)
cv2.ellipse(image, (128, 140), (50, 60), 0, 0, 360, (100, 100, 100), -1)
cv2.ellipse(image, (128, 70), (55, 35), 0, 0, 360, (150, 150, 150), -1)

# 발가락
toe_positions = [(90, 40, 12), (110, 30, 10), (128, 25, 10), (146, 30, 9), (162, 38, 8)]
for x, y, radius in toe_positions:
    cv2.circle(image, (x, y), radius, (120, 120, 120), -1)

# 발 아치
cv2.ellipse(image, (128, 140), (30, 40), 0, 0, 360, (200, 200, 200), -1)

# 노이즈 및 블러
noise = np.random.normal(0, 5, (height, width, 3))
image = np.clip(image + noise, 0, 255).astype(np.uint8)
image = cv2.GaussianBlur(image, (5, 5), 0)

# 간단한 파일명으로 저장
output_path = os.path.join(output_dir, 'foot_left.png')
success = cv2.imwrite(output_path, image)

print(f"이미지 저장: {'성공' if success else '실패'}")
print(f"경로: {output_path}")
print(f"절대 경로: {os.path.abspath(output_path)}")
print(f"파일 존재: {os.path.exists(output_path)}")

if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    print(f"\\n디렉토리 내용 ({len(files)}개):")
    for f in files:
        print(f"  - {f}")
