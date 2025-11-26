import json

# Read the notebook
with open(r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the code cell and modify it to include Korean font settings
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'import matplotlib.pyplot as plt' in source:
            # Create new code with Korean font support
            new_code = """import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 또는 다른 한글 폰트 사용 가능:
# plt.rcParams['font.family'] = 'NanumGothic'  # 나눔고딕
# plt.rcParams['font.family'] = 'Batang'  # 바탕체

# Load the image
frame = cv2.imread('pressure_heatmap.png')

if frame is None:
    print("Error: Could not load image")
else:
    # Convert BGR to RGB for matplotlib
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Create the original input heatmap (before flattening)
    # This is the raw heatmap without any flattening or equalization
    original_input = frame.copy()
    
    # Create figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Show original input (non-flattened)
    original_rgb = cv2.cvtColor(original_input, cv2.COLOR_BGR2RGB)
    axes[0].imshow(original_rgb)
    axes[0].set_title('Original Input Heatmap\\n(평탄화되지 않은 원본 입력)', fontsize=14, pad=10)
    axes[0].axis('off')
    
    # Show the same image again (or you can apply processing here)
    axes[1].imshow(frame_rgb)
    axes[1].set_title('Loaded Heatmap\\n(로드된 히트맵)', fontsize=14, pad=10)
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("\\n=== Image Information ===")
    print(f"Shape: {frame.shape}")
    print(f"Data type: {frame.dtype}")
    print(f"Min value: {frame.min()}")
    print(f"Max value: {frame.max()}")
"""
            cell['source'] = new_code.split('\n')
            cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
            # Clear outputs
            cell['outputs'] = []
            cell['execution_count'] = None

# Save the modified notebook
with open(r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("✓ 한글 폰트 설정이 추가되었습니다!")
print("✓ 사용된 폰트: 맑은 고딕 (Malgun Gothic)")
print("✓ 이제 pyplot 제목이 한글로 제대로 표시됩니다.")
print("\n다른 폰트를 사용하려면 코드에서 다음 중 하나를 선택하세요:")
print("  - 'Malgun Gothic' (맑은 고딕)")
print("  - 'NanumGothic' (나눔고딕)")
print("  - 'Batang' (바탕체)")
