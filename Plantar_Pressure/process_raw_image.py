import cv2
import numpy as np
import os

# Correct absolute path to the raw input image
input_path = r'H:\\내 드라이브\\강의자료\\Vibe_Coding\\Plantar_Pressure\\test_foot_data\\0_Original_Source.png_left_256.png'

if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input image not found: {input_path}")

# Load image
original_image = cv2.imread(input_path)
if original_image is None:
    raise ValueError('Failed to load image')

# Convert to grayscale (pressure map)
gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# Compute pressure map and normalize to minimize distortion
pressure_map = gray.astype(np.float32)
pressure_normalized = (pressure_map - pressure_map.min()) / (pressure_map.max() - pressure_map.min())

# Apply Jet colormap
pressure_uint8 = (pressure_normalized * 255).astype(np.uint8)
heatmap_jet = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_JET)

# Save the Jet colormap heatmap
output_path = r'H:\\내 드라이브\\강의자료\\Vibe_Coding\\Plantar_Pressure\\pressure_heatmap_jet_processed.png'
cv2.imwrite(output_path, heatmap_jet)

print('✅ Processing complete!')
print(f'Input image: {input_path}')
print(f'Output heatmap saved to: {output_path}')
print('Image info:')
print(f'  Original shape: {original_image.shape}')
print(f'  Pressure map shape: {pressure_map.shape}')
print(f'  Pressure range: {pressure_map.min():.2f} - {pressure_map.max():.2f}')
print(f'  Normalized range: {pressure_normalized.min():.2f} - {pressure_normalized.max():.2f}')
