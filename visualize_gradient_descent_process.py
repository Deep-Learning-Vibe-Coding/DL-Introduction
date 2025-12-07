
import torch
import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# 1. 데이터 및 모델 설정
# ============================================================================
x_train = torch.FloatTensor([[1], [2], [3]])
y_train = torch.FloatTensor([[3], [5], [7]])

W = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
lr = 0.1
epochs = 20

# 학습 과정 기록용 리스트
losses = []
W_history = []
b_history = []

# ============================================================================
# 2. 학습 진행 (Gradient Descent)
# ============================================================================
for epoch in range(epochs + 1):
    # 가설 및 손실 계산
    hypothesis = x_train * W + b
    cost = torch.mean((hypothesis - y_train) ** 2)

    # 기록 저장
    losses.append(cost.item())
    W_history.append(W.item())
    b_history.append(b.item())

    # 업데이트
    cost.backward()
    with torch.no_grad():
        W -= lr * W.grad
        b -= lr * b.grad
        W.grad.zero_()
        b.grad.zero_()

# ============================================================================
# 3. 시각화
# ============================================================================
plt.figure(figsize=(15, 6))

# --- [왼쪽 그래프] Loss(비용) 변화 ---
plt.subplot(1, 2, 1)
plt.plot(losses, 'r-o', linewidth=2, markersize=6)
plt.title('Change of Loss (Cost)', fontsize=16)
plt.xlabel('Epoch', fontsize=14)
plt.ylabel('Loss (MSE)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.text(10, max(losses)*0.5, 'Loss decreases rapidly!', fontsize=12, color='red')

# --- [오른쪽 그래프] 회귀선(Regression Line)의 변화 ---
plt.subplot(1, 2, 2)
# 원본 데이터 점 찍기
plt.scatter(x_train, y_train, c='black', label='Data Points', s=150, zorder=10)

# 시각화할 에포크 선정 (초반, 중반, 후반)
epochs_to_plot = [0, 1, 3, 5, 10, 20]
x_range = np.linspace(0, 4, 100)

# 색상맵 생성 (점점 진해지도록)
colors = plt.cm.viridis(np.linspace(0, 1, len(epochs_to_plot)))

for i, epoch in enumerate(epochs_to_plot):
    if epoch < len(W_history):
        w_val = W_history[epoch]
        b_val = b_history[epoch]
        
        # 회귀선 계산
        y_range = w_val * x_range + b_val
        
        # 그래프 그리기
        label = f'Epoch {epoch}'
        if epoch == 0: label += ' (Start)'
        if epoch == 20: label += ' (End)'
        
        plt.plot(x_range, y_range, label=label, color=colors[i], linewidth=2, alpha=0.8)

plt.title('Evolution of Regression Line', fontsize=16)
plt.xlabel('x', fontsize=14)
plt.ylabel('y', fontsize=14)
plt.xlim(0, 4)
plt.ylim(0, 9)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
