
import torch
import matplotlib.pyplot as plt

# ============================================================================
# 1. 데이터 준비 (노트북과 동일)
# ============================================================================
x_train = torch.FloatTensor([[1], [2], [3]])
y_train = torch.FloatTensor([[3], [5], [7]])

# ============================================================================
# 2. 데이터 시각화
# ============================================================================
def visualize_data(x, y):
    """
    입력 데이터와 정답 레이블을 시각화합니다.
    """
    plt.figure(figsize=(8, 6))
    
    # 산점도 그리기
    plt.scatter(x, y, color='blue', label='Data Points', s=100)
    
    # 그래프 꾸미기
    plt.title('Input Data vs Target Label', fontsize=16)
    plt.xlabel('x_train (Input)', fontsize=14)
    plt.ylabel('y_train (Target)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    # 데이터 포인트에 좌표 표시
    for i in range(len(x)):
        plt.text(x[i], y[i], f'({x[i].item():.1f}, {y[i].item():.1f})', 
                 fontsize=12, ha='right', va='bottom')

    plt.show()

# 시각화 실행
print("입력 데이터 시각화:")
visualize_data(x_train, y_train)
