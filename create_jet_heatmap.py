import json

# Read the notebook
with open(r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the code cell and modify it to use Jet colormap for pressure distribution
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'import matplotlib.pyplot as plt' in source:
            # Create new code with Jet colormap pressure heatmap
            new_code = """import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 이미지 경로
image_path = 'test_foot_data/0_Original_Source.png_left_256.png'

# 이미지 로드
original_image = cv2.imread(image_path)

if original_image is None:
    print(f"Error: Could not load image from {image_path}")
    print("\\n현재 디렉토리의 파일을 확인하세요.")
    import os
    if os.path.exists('test_foot_data'):
        print("test_foot_data 디렉토리 내용:")
        print(os.listdir('test_foot_data'))
    else:
        print("test_foot_data 디렉토리가 존재하지 않습니다.")
else:
    # 그레이스케일로 변환
    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    
    # 압력 분포 계산 (밝기 값을 압력으로 간주)
    # 왜곡 최소화를 위해 정규화
    pressure_map = gray.astype(np.float32)
    
    # 정규화 (0-1 범위로)
    pressure_normalized = (pressure_map - pressure_map.min()) / (pressure_map.max() - pressure_map.min())
    
    # Jet colormap 적용
    # cv2.COLORMAP_JET을 사용하여 압력 분포 시각화
    pressure_uint8 = (pressure_normalized * 255).astype(np.uint8)
    heatmap_jet = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_JET)
    
    # BGR to RGB 변환
    original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    heatmap_rgb = cv2.cvtColor(heatmap_jet, cv2.COLOR_BGR2RGB)
    
    # 3개의 서브플롯 생성
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. 원본 이미지
    axes[0].imshow(original_rgb)
    axes[0].set_title('원본 입력 이미지\\n(Original Input)', fontsize=14, pad=10)
    axes[0].axis('off')
    
    # 2. 그레이스케일 압력 맵
    axes[1].imshow(gray, cmap='gray')
    axes[1].set_title('압력 분포 (그레이스케일)\\n(Pressure Distribution)', fontsize=14, pad=10)
    axes[1].axis('off')
    
    # 3. Jet colormap 히트맵
    im = axes[2].imshow(heatmap_rgb)
    axes[2].set_title('압력 분포 히트맵 (Jet Colormap)\\n왜곡 최소화', fontsize=14, pad=10)
    axes[2].axis('off')
    
    # 컬러바 추가
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='jet'), ax=axes[2], fraction=0.046, pad=0.04)
    cbar.set_label('압력 강도 (Pressure Intensity)', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.show()
    
    print("\\n=== 이미지 정보 ===")
    print(f"원본 Shape: {original_image.shape}")
    print(f"압력 맵 Shape: {pressure_map.shape}")
    print(f"압력 범위: {pressure_map.min():.2f} ~ {pressure_map.max():.2f}")
    print(f"정규화된 압력 범위: {pressure_normalized.min():.2f} ~ {pressure_normalized.max():.2f}")
    
    # 히트맵 저장
    output_path = 'pressure_heatmap_jet.png'
    cv2.imwrite(output_path, heatmap_jet)
    print(f"\\n✓ Jet colormap 히트맵이 저장되었습니다: {output_path}")
"""
            cell['source'] = new_code.split('\n')
            cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
            # Clear outputs
            cell['outputs'] = []
            cell['execution_count'] = None

# Save the modified notebook
with open(r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("✓ 노트북이 Jet colormap 압력 분포 히트맵을 생성하도록 수정되었습니다!")
print("✓ 이미지 경로: test_foot_data/0_Original_Source.png_left_256.png")
print("✓ 왜곡 최소화를 위한 정규화 적용")
print("✓ 3개의 이미지 표시:")
print("  1. 원본 입력 이미지")
print("  2. 그레이스케일 압력 분포")
print("  3. Jet colormap 히트맵 (왜곡 최소화)")
print("\\n주의: test_foot_data/0_Original_Source.png_left_256.png 파일이 필요합니다.")
