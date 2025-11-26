import json
import os

# Notebook path
nb_path = r'H:\\내 드라이브\\강의자료\\Vibe_Coding\\Plantar_Pressure\\footprint_pressure_test.ipynb'

# Load notebook JSON
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Code with added comments
new_code = """import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from PIL import Image
import os
import glob

# ---------------------------------------------------------
# 1. 한글 폰트 설정 (Windows 환경)
# ---------------------------------------------------------
# matplotlib에서 한글이 깨지지 않도록 'Malgun Gothic' 폰트를 설정합니다.
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스(-) 기호가 깨지는 것을 방지

# ---------------------------------------------------------
# 2. 이미지 디렉토리 설정 및 파일 탐색
# ---------------------------------------------------------
# 현재 작업 디렉토리를 기준으로 'test_foot_data' 폴더의 절대 경로를 생성합니다.
base_dir = os.path.abspath('')
data_dir = os.path.join(base_dir, 'test_foot_data')

# 디렉토리가 존재하는지 확인합니다.
if not os.path.isdir(data_dir):
    print(f"⚠️ Error: Directory not found: {data_dir}")
else:
    # glob을 사용하여 해당 디렉토리 내의 모든 .png 파일을 찾습니다.
    image_files = glob.glob(os.path.join(data_dir, '*.png'))
    
    if not image_files:
        print(f"⚠️ No .png files found in {data_dir}")
    else:
        print(f"🔎 Found {len(image_files)} images in {data_dir}\\n")
        
        # ---------------------------------------------------------
        # 3. 이미지 처리 루프 (각 이미지에 대해 반복)
        # ---------------------------------------------------------
        for i, image_path in enumerate(image_files):
            filename = os.path.basename(image_path)
            print(f"--- Processing Image {i+1}: {filename} ---")
            
            # [이미지 로드]
            # cv2.imread는 한글 경로를 제대로 인식하지 못할 수 있으므로,
            # PIL(Image.open)로 먼저 이미지를 열고 numpy 배열로 변환합니다.
            try:
                pil_img = Image.open(image_path)
                original_image = np.array(pil_img)
                
                # PIL은 이미지를 RGB 순서로 읽지만, OpenCV는 BGR 순서를 사용합니다.
                # 따라서 후속 처리를 위해 RGB -> BGR로 변환하여 OpenCV 형식으로 맞춥니다.
                original_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"❌ Error: Could not load image {filename}")
                print(e)
                continue

            # ---------------------------------------------------------
            # 4. 이미지 전처리 및 압력 맵 생성
            # ---------------------------------------------------------
            
            # 1) [시각화용 RGB 변환]
            # matplotlib으로 출력하기 위해 BGR 이미지를 다시 RGB로 변환합니다.
            original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            
            # 2) [그레이스케일 변환]
            # 압력 강도를 계산하기 위해 컬러 이미지를 흑백(Grayscale)으로 변환합니다.
            # 밝은 부분일수록 압력이 높은 것으로 간주됩니다.
            gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            
            # 3) [노이즈 제거 (Gaussian Blur)]
            # 이미지의 자글자글한 노이즈를 제거하고 부드럽게 만들기 위해 가우시안 블러를 적용합니다.
            # (5, 5)는 커널 크기이며, 0은 표준편차를 자동으로 계산함을 의미합니다.
            # 이 과정은 압력 분포의 왜곡을 최소화하는 데 중요합니다.
            gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 4) [정규화 (Normalization)]
            # 픽셀 값을 0.0 ~ 1.0 사이의 실수(float) 범위로 변환합니다.
            # (현재값 - 최소값) / (최대값 - 최소값) 공식을 사용하여
            # 압력의 상대적인 강도를 명확하게 표현합니다.
            pressure_map = gray_blur.astype(np.float32)
            pressure_normalized = (pressure_map - pressure_map.min()) / (pressure_map.max() - pressure_map.min())
            
            # ---------------------------------------------------------
            # 5. 히트맵 생성 (Jet Colormap)
            # ---------------------------------------------------------
            
            # 정규화된 값을 다시 0~255 범위의 정수(uint8)로 변환합니다.
            pressure_uint8 = (pressure_normalized * 255).astype(np.uint8)
            
            # cv2.applyColorMap을 사용하여 흑백 이미지에 컬러맵(Jet)을 입힙니다.
            # Jet 컬러맵: 파란색(낮은 압력) -> 초록색 -> 노란색 -> 빨간색(높은 압력)
            heatmap_jet = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_JET)
            
            # matplotlib 출력을 위해 BGR -> RGB로 변환합니다.
            heatmap_rgb = cv2.cvtColor(heatmap_jet, cv2.COLOR_BGR2RGB)
            
            # ---------------------------------------------------------
            # 6. 결과 시각화
            # ---------------------------------------------------------
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            
            # [원본 이미지]
            axes[0].imshow(original_rgb)
            axes[0].set_title(f'원본 입력 이미지\\n({filename})', fontsize=12, pad=10)
            axes[0].axis('off')
            
            # [그레이스케일 압력 맵]
            axes[1].imshow(gray_blur, cmap='gray')
            axes[1].set_title('그레이스케일 압력 맵\\n(Blurred)', fontsize=12, pad=10)
            axes[1].axis('off')
            
            # [Jet 컬러맵 히트맵]
            axes[2].imshow(heatmap_rgb)
            axes[2].set_title('Jet 컬러맵 압력 히트맵\\n(왜곡 최소화)', fontsize=12, pad=10)
            axes[2].axis('off')
            
            # [컬러바 추가]
            # 히트맵의 색상이 어떤 압력 강도를 나타내는지 보여주는 컬러바를 추가합니다.
            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='jet'), ax=axes[2], fraction=0.046, pad=0.04)
            cbar.set_label('압력 강도 (Pressure Intensity)', rotation=270, labelpad=20)
            
            plt.tight_layout()
            plt.show()
            
            # [이미지 정보 출력]
            print(f"원본 Shape: {original_image.shape}")
            print(f"압력 범위: {pressure_map.min():.2f} ~ {pressure_map.max():.2f}")
            print(f"정규화 범위: {pressure_normalized.min():.2f} ~ {pressure_normalized.max():.2f}")
            print("-" * 50 + "\\n")
"""

# Replace the code cell
for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        src = ''.join(cell.get('source', []))
        if 'import cv2' in src:
            cell['source'] = [line + '\n' for line in new_code.split('\n')]
            cell['outputs'] = []
            cell['execution_count'] = None
            break

# Write back
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('✅ notebook updated with detailed comments.')
