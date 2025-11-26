import json

# Read the notebook
with open(r'H:\내 드라이브\강의자료\Vibe_Coding\Plantar_Pressure\footprint_pressure_test.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the code cell and modify it
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'pressure_heatmap.png' in source:
            # Create new code that shows the original input heatmap
            # We'll load the image and show it before any processing
            new_code = """import cv2
import numpy as np
import matplotlib.pyplot as plt

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

print("✓ 노트북이 성공적으로 수정되었습니다!")
print("✓ 이제 평탄화되지 않은 원본 입력 히트맵이 표시됩니다.")
print("✓ Jupyter Notebook을 열어서 셀을 실행하세요.")
