import json

# Read the notebook
with open(r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the code cell and modify it to show both raw and processed images
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'import matplotlib.pyplot as plt' in source:
            # Create new code to display raw input and processed output
            new_code = """import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# Load the raw input image (original, unprocessed)
raw_image = cv2.imread('pressure_heatmap_output.png')

# Load the processed image (flattened and equalized)
processed_image = cv2.imread('pressure_heatmap.png')

if raw_image is None or processed_image is None:
    print("Error: Could not load one or both images")
    print(f"Raw image loaded: {raw_image is not None}")
    print(f"Processed image loaded: {processed_image is not None}")
else:
    # Convert BGR to RGB for matplotlib
    raw_rgb = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
    processed_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    
    # Create figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Show raw input (original, unprocessed)
    axes[0].imshow(raw_rgb)
    axes[0].set_title('원본 입력 이미지 (Raw Input)\\n평탄화 및 균등화 전', fontsize=14, pad=10)
    axes[0].axis('off')
    
    # Show processed image (flattened and equalized)
    axes[1].imshow(processed_rgb)
    axes[1].set_title('처리된 히트맵 (Processed Heatmap)\\n평탄화 및 균등화 후', fontsize=14, pad=10)
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("\\n=== 원본 이미지 정보 (Raw Input) ===")
    print(f"Shape: {raw_image.shape}")
    print(f"Data type: {raw_image.dtype}")
    print(f"Min value: {raw_image.min()}")
    print(f"Max value: {raw_image.max()}")
    
    print("\\n=== 처리된 이미지 정보 (Processed) ===")
    print(f"Shape: {processed_image.shape}")
    print(f"Data type: {processed_image.dtype}")
    print(f"Min value: {processed_image.min()}")
    print(f"Max value: {processed_image.max()}")
"""
            cell['source'] = new_code.split('\n')
            cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
            # Clear outputs
            cell['outputs'] = []
            cell['execution_count'] = None

# Save the modified notebook
with open(r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("✓ 노트북이 원본 raw 이미지를 표시하도록 수정되었습니다!")
print("✓ 왼쪽: 원본 입력 이미지 (pressure_heatmap_output.png)")
print("✓ 오른쪽: 처리된 히트맵 (pressure_heatmap.png)")
print("\n이제 Jupyter Notebook을 실행하면 원본 raw 이미지와 처리된 이미지를 비교할 수 있습니다.")
