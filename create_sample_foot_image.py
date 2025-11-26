import cv2
import numpy as np

# 256x256 크기의 샘플 발 이미지 생성
# 실제 발 모양을 시뮬레이션
height, width = 256, 256
image = np.zeros((height, width, 3), dtype=np.uint8)

# 배경을 흰색으로
image[:] = (255, 255, 255)

# 발 모양 생성 (타원형)
# 발뒤꿈치 (더 강한 압력 - 어두운 색)
cv2.ellipse(image, (128, 200), (60, 40), 0, 0, 360, (50, 50, 50), -1)

# 발바닥 중앙 (중간 압력)
cv2.ellipse(image, (128, 140), (50, 60), 0, 0, 360, (100, 100, 100), -1)

# 앞발 (발가락 부분 - 약한 압력)
cv2.ellipse(image, (128, 70), (55, 35), 0, 0, 360, (150, 150, 150), -1)

# 발가락 5개 추가
toe_positions = [
    (90, 40, 12),   # 엄지발가락
    (110, 30, 10),  # 검지발가락
    (128, 25, 10),  # 중지발가락
    (146, 30, 9),   # 약지발가락
    (162, 38, 8),   # 새끼발가락
]

for x, y, radius in toe_positions:
    cv2.circle(image, (x, y), radius, (120, 120, 120), -1)

# 발 아치 부분 (압력이 약함 - 밝은 색)
cv2.ellipse(image, (128, 140), (30, 40), 0, 0, 360, (200, 200, 200), -1)

# 약간의 노이즈 추가 (더 자연스럽게)
noise = np.random.normal(0, 5, (height, width, 3))
image = np.clip(image + noise, 0, 255).astype(np.uint8)

# 가우시안 블러로 부드럽게
image = cv2.GaussianBlur(image, (5, 5), 0)

# 저장
output_path = r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\test_foot_data\0_Original_Source.png_left_256.png'
cv2.imwrite(output_path, image)

print(f"✓ 샘플 발 이미지가 생성되었습니다: {output_path}")
print(f"✓ 이미지 크기: {image.shape}")
print(f"✓ 압력 분포 범위: {image.min()} ~ {image.max()}")
print("\n이제 Jupyter Notebook을 실행하여 Jet colormap 히트맵을 확인하세요!")
