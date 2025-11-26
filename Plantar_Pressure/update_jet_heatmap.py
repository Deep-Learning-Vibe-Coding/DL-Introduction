import json
import os

# Path to notebook
notebook_path = r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb'

# Load notebook JSON
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New code block for processing raw webcam RGB image and Jet colormap
new_code = """import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 이미지 경로 (웹캠으로 촬영한 raw RGB 이미지, LUT 없음)
image_path = 'test_foot_data/0_Original_Source.png_left_256.png'

# 이미지 로드 및 존재 확인
original_image = cv2.imread(image_path)
if original_image is None:
    print(f"Error: Could not load image from {image_path}")
    import os
    print(f"Current working directory: {os.getcwd()}")
    if os.path.exists('test_foot_data'):
        print("test_foot_data 디렉토리 내용:")
        for f in os.listdir('test_foot_data'):
            print(f"  - {f}")
    else:
        print("test_foot_data 디렉토리가 존재하지 않습니다.")
else:
    # 1) BGR -> RGB 변환 (시각화를 위해)
    original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    # 2) 그레이스케일 변환 (압력 맵 계산을 위한 기본값)
    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    
    # 3) 노이즈 감소 (Gaussian blur) – 왜곡 최소화
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 4) 압력 맵 (float32) 및 정규화 (0-1) – 왜곡 최소화
    pressure_map = gray_blur.astype(np.float32)
    pressure_normalized = (pressure_map - pressure_map.min()) / (pressure_map.max() - pressure_map.min())
    
    # 5) Jet colormap 적용
    pressure_uint8 = (pressure_normalized * 255).astype(np.uint8)
    heatmap_jet = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_JET)
    heatmap_rgb = cv2.cvtColor(heatmap_jet, cv2.COLOR_BGR2RGB)
    
    # 6) 결과 시각화 (원본, 그레이스케일, Jet 히트맵)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes[0].imshow(original_rgb)
    axes[0].set_title('원본 입력 이미지\\n(Raw RGB)', fontsize=14, pad=10)
    axes[0].axis('off')
    
    axes[1].imshow(gray_blur, cmap='gray')
    axes[1].set_title('그레이스케일 압력 맵\\n(Blurred)', fontsize=14, pad=10)
    axes[1].axis('off')
    
    axes[2].imshow(heatmap_rgb)
    axes[2].set_title('Jet 컬러맵 압력 히트맵\\n(왜곡 최소화)', fontsize=14, pad=10)
    axes[2].axis('off')
    
    # 컬러바 추가 (Jet 컬러맵)
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='jet'), ax=axes[2], fraction=0.046, pad=0.04)
    cbar.set_label('압력 강도 (Pressure Intensity)', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.show()
    
    # 이미지 정보 출력
    print("\n=== 이미지 정보 ===")
    print(f"원본 Shape: {original_image.shape}")
    print(f"그레이스케일 Shape: {gray.shape}")
    print(f"압력 범위: {pressure_map.min():.2f} ~ {pressure_map.max():.2f}")
    print(f"정규화 범위: {pressure_normalized.min():.2f} ~ {pressure_normalized.max():.2f}")
    
    # 히트맵 저장
    output_path = 'pressure_heatmap_jet_processed.png'
    cv2.imwrite(output_path, heatmap_jet)
    print(f"\n✓ Jet colormap 히트맵이 저장되었습니다: {output_path}")
"""

# Find the first code cell that contains import cv2 (or a known marker) and replace its source
for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        if 'import cv2' in source:
            # Replace source lines
            cell['source'] = [line + '\n' for line in new_code.split('\n')]
            # Clear previous outputs
            cell['outputs'] = []
            cell['execution_count'] = None
            break

# Write back the notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('✅ notebook updated with Jet colormap processing for raw webcam image.')
