# footprint_pressure_test.ipynb - Jet Colormap 압력 분포 히트맵

## 최종 수정 완료 (2025-11-24 23:57)

`footprint_pressure_test.ipynb` 노트북이 **Jet colormap을 사용한 압력 분포 히트맵**을 생성하도록 수정되었습니다.

### 🎯 핵심 기능

#### 1. Jet Colormap 압력 분포 히트맵 ✨
```python
# 그레이스케일로 변환
gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# 압력 분포 계산 및 정규화 (왜곡 최소화)
pressure_map = gray.astype(np.float32)
pressure_normalized = (pressure_map - pressure_map.min()) / (pressure_map.max() - pressure_map.min())

# Jet colormap 적용
pressure_uint8 = (pressure_normalized * 255).astype(np.uint8)
heatmap_jet = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_JET)
```

#### 2. 왜곡 최소화 처리
- **정규화**: 0-1 범위로 정규화하여 왜곡 최소화
- **Jet Colormap**: 압력 강도를 색상으로 직관적으로 표현
  - 🔵 파란색: 낮은 압력
  - 🟢 녹색: 중간 압력
  - 🟡 노란색: 높은 압력
  - 🔴 빨간색: 매우 높은 압력

#### 3. 3개의 이미지 비교 표시
| 순서 | 이미지 | 설명 |
|------|--------|------|
| 1 | 원본 입력 이미지 | test_foot_data/0_Original_Source.png_left_256.png |
| 2 | 그레이스케일 압력 분포 | 밝기 값을 압력으로 변환 |
| 3 | **Jet Colormap 히트맵** | 왜곡 최소화된 압력 분포 시각화 |

#### 4. 컬러바 추가
- 압력 강도를 시각적으로 표시
- "압력 강도 (Pressure Intensity)" 레이블

### 📊 전체 코드 구조

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 이미지 로드
image_path = 'test_foot_data/0_Original_Source.png_left_256.png'
original_image = cv2.imread(image_path)

# 그레이스케일 변환
gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# 압력 분포 정규화 (왜곡 최소화)
pressure_map = gray.astype(np.float32)
pressure_normalized = (pressure_map - pressure_map.min()) / (pressure_map.max() - pressure_map.min())

# Jet colormap 적용
pressure_uint8 = (pressure_normalized * 255).astype(np.uint8)
heatmap_jet = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_JET)

# 3개의 서브플롯으로 표시
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 1. 원본 이미지
axes[0].imshow(original_rgb)
axes[0].set_title('원본 입력 이미지\\n(Original Input)')

# 2. 그레이스케일 압력 분포
axes[1].imshow(gray, cmap='gray')
axes[1].set_title('압력 분포 (그레이스케일)\\n(Pressure Distribution)')

# 3. Jet colormap 히트맵
axes[2].imshow(heatmap_rgb)
axes[2].set_title('압력 분포 히트맵 (Jet Colormap)\\n왜곡 최소화')

# 컬러바 추가
cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='jet'), ax=axes[2])
cbar.set_label('압력 강도 (Pressure Intensity)', rotation=270, labelpad=20)
```

### 🚀 사용 방법

1. **이미지 준비**
   - 파일: `test_foot_data/0_Original_Source.png_left_256.png`
   - 샘플 이미지가 자동으로 생성되어 있습니다

2. **Jupyter Notebook 실행**
   - `footprint_pressure_test.ipynb` 열기
   - 셀 실행 (Shift + Enter)

3. **결과 확인**
   - 3개의 이미지가 나란히 표시됨
   - Jet colormap 히트맵으로 압력 분포 확인
   - 컬러바로 압력 강도 파악

### 📁 파일 구조

```
Plantar_Pressure/
├── footprint_pressure_test.ipynb  # 수정된 노트북
├── test_foot_data/
│   └── 0_Original_Source.png_left_256.png  # 입력 이미지
├── pressure_heatmap_jet.png  # 생성된 Jet 히트맵 (자동 저장)
└── MODIFICATION_SUMMARY.md  # 이 문서
```

### 🎨 Jet Colormap 색상 의미

| 색상 | 압력 강도 | 의미 |
|------|-----------|------|
| 🔵 파란색 (Blue) | 0-25% | 매우 낮은 압력 |
| 🟦 하늘색 (Cyan) | 25-40% | 낮은 압력 |
| 🟢 녹색 (Green) | 40-60% | 중간 압력 |
| 🟡 노란색 (Yellow) | 60-75% | 높은 압력 |
| 🟠 주황색 (Orange) | 75-90% | 매우 높은 압력 |
| 🔴 빨간색 (Red) | 90-100% | 최대 압력 |

### 💡 왜곡 최소화 기법

1. **정규화 (Normalization)**
   ```python
   pressure_normalized = (pressure_map - pressure_map.min()) / (pressure_map.max() - pressure_map.min())
   ```
   - 전체 범위를 0-1로 정규화
   - 극단값의 영향 최소화

2. **Float32 사용**
   ```python
   pressure_map = gray.astype(np.float32)
   ```
   - 정밀도 향상
   - 계산 오차 감소

3. **OpenCV Jet Colormap**
   ```python
   cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_JET)
   ```
   - 표준 Jet colormap 사용
   - 일관된 색상 매핑

### 📊 출력 정보

노트북 실행 시 다음 정보가 출력됩니다:

```
=== 이미지 정보 ===
원본 Shape: (256, 256, 3)
압력 맵 Shape: (256, 256)
압력 범위: 45.00 ~ 255.00
정규화된 압력 범위: 0.00 ~ 1.00

✓ Jet colormap 히트맵이 저장되었습니다: pressure_heatmap_jet.png
```

### 🔧 문제 해결

#### 이미지를 찾을 수 없다는 오류

**해결 방법 1**: 샘플 이미지 재생성
```bash
python create_sample_foot_image.py
```

**해결 방법 2**: 실제 이미지 사용
- `test_foot_data/0_Original_Source.png_left_256.png`에 실제 발 이미지 배치

**해결 방법 3**: 경로 확인
```python
import os
print(os.path.exists('test_foot_data/0_Original_Source.png_left_256.png'))
```

#### 한글이 깨지는 경우

```python
# 다른 폰트 사용
plt.rcParams['font.family'] = 'NanumGothic'  # 나눔고딕
# 또는
plt.rcParams['font.family'] = 'Batang'  # 바탕체
```

### 📝 수정 이력

| 날짜 | 시간 | 수정 내용 |
|------|------|-----------|
| 2025-11-24 | 23:46:14 | 초기 수정: 평탄화되지 않은 원본 입력 히트맵 표시 |
| 2025-11-24 | 23:50:07 | 한글 폰트 설정 추가 (맑은 고딕) |
| 2025-11-24 | 23:52:22 | 원본 raw 이미지 표시 기능 추가 |
| 2025-11-24 | **23:57:45** | **Jet colormap 압력 분포 히트맵 생성 (왜곡 최소화)** |

### 🎓 추가 정보

#### 다른 Colormap 사용하기

OpenCV에서 지원하는 다른 colormap들:

```python
# HOT colormap (검정-빨강-노랑-흰색)
heatmap = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_HOT)

# RAINBOW colormap (무지개 색상)
heatmap = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_RAINBOW)

# VIRIDIS colormap (파랑-녹색-노랑)
heatmap = cv2.applyColorMap(pressure_uint8, cv2.COLORMAP_VIRIDIS)
```

#### 압력 임계값 설정

특정 압력 이상만 표시하려면:

```python
# 50% 이상의 압력만 표시
threshold = 0.5
pressure_thresholded = np.where(pressure_normalized > threshold, pressure_normalized, 0)
```

---

## ✅ 완료!

이제 노트북을 실행하면 **Jet colormap을 사용한 압력 분포 히트맵**을 확인할 수 있습니다! 🎉

**왜곡이 최소화**되어 정확한 압력 분포를 시각화할 수 있습니다.
