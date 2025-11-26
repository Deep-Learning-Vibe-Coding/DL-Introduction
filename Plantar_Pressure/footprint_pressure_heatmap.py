import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_pressure_heatmap(image_path, output_path="pressure_heatmap.png"):
    """
    주어진 RGB 발자국 이미지로부터 압력 분포 히트맵을 생성합니다.

    Args:
        image_path (str): 입력 이미지 파일 경로.
        output_path (str): 저장될 히트맵 이미지 파일 경로.
    """
    # 1. 이미지 파일 존재 여부 확인
    if not os.path.exists(image_path):
        print(f"오류: 입력 파일을 찾을 수 없습니다: {image_path}")
        return

    # 2. 유니코드 경로 문제 해결을 위해 np.fromfile과 cv2.imdecode 사용
    try:
        with open(image_path, 'rb') as f:
            file_bytes = np.fromfile(f, dtype=np.uint8)
        # OpenCV 이미지로 디코딩
        image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise IOError("cv2.imdecode가 이미지를 디코딩하지 못했습니다.")
    except Exception as e:
        print(f"오류: 이미지를 로드하는 중 문제가 발생했습니다: {image_path}")
        print(f"세부 정보: {e}")
        return

    # 3. BGR 이미지를 그레이스케일로 변환하여 압력 강도 맵 생성
    # 픽셀의 밝기를 압력으로 간주하여 왜곡을 최소화합니다.
    pressure_map = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 4. 압력이 없는 영역(값이 0인 픽셀)을 마스킹 처리
    # 이렇게 하면 배경(검은색)이 히트맵 색상에 영향을 주지 않습니다.
    masked_pressure_map = np.ma.masked_where(pressure_map == 0, pressure_map)

    # 5. Matplotlib을 사용하여 히트맵 생성
    fig, ax = plt.subplots(figsize=(6, 10)) # 이미지 비율에 맞게 figsize 조정 가능

    # 'jet' 컬러맵 가져오기
    cmap = plt.get_cmap('jet')
    # 마스킹된 영역(압력 0)을 검은색으로 설정
    cmap.set_bad(color='black')

    # 히트맵 이미지 표시
    im = ax.imshow(masked_pressure_map, cmap=cmap)

    # 컬러바(압력 강도 범례) 추가
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Pressure Intensity', rotation=270, labelpad=15)

    # 제목 추가 및 축 숨기기
    ax.set_title('Footprint Pressure Heatmap')
    ax.axis('off')

    # 6. 결과 이미지를 파일로 저장
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    print(f"히트맵이 성공적으로 생성되어 '{output_path}'에 저장되었습니다.")

    # (선택사항) 화면에 결과 표시
    # plt.show()

if __name__ == '__main__':
    # 사용자가 제공한 입력 이미지 경로
    input_image = "h:\\내 드라이브\\강의자료\\Vibe_Coding\\0_Original_Source.png_left_256.png"
    
    # 히트맵 생성 함수 호출
    create_pressure_heatmap(input_image)
