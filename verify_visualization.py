
import torch
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 및 학습 설정
x_train = torch.FloatTensor([[1], [2], [3]])
y_train = torch.FloatTensor([[3], [5], [7]])

W = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
lr = 0.1
epochs = 20

losses = []
W_history = []
b_history = []

# 2. 학습 진행
for epoch in range(epochs + 1):
    hypothesis = x_train * W + b
    cost = torch.mean((hypothesis - y_train) ** 2)

    losses.append(cost.item())
    W_history.append(W.item())
    b_history.append(b.item())

    cost.backward()
    with torch.no_grad():
        W -= lr * W.grad
        b -= lr * b.grad
        W.grad.zero_()
        b.grad.zero_()

# 3. 수정된 시각화 코드 검증
plt.figure(figsize=(15, 6))

# 왼쪽: Loss 그래프
plt.subplot(1, 2, 1)
plt.plot(losses, 'r-o')
plt.title('Change of Loss (Cost)')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.grid(True)

# 오른쪽: 회귀선 변화 그래프 (수정된 부분)
plt.subplot(1, 2, 2)
plt.scatter(x_train, y_train, c='black', label='Data', s=100, zorder=10)

epochs_to_plot = [0, 1, 3, 5, 10, 20]
x_range = np.linspace(0, 4, 100)

# 색상 맵: coolwarm (파랑 -> 빨강)
colors = plt.cm.coolwarm(np.linspace(0, 1, len(epochs_to_plot)))

print("Plotting lines with the following settings:")
for i, ep in enumerate(epochs_to_plot):
    if ep < len(W_history):
        w_val = W_history[ep]
        b_val = b_history[ep]
        y_range = w_val * x_range + b_val
        
        # 스타일 설정 확인
        if ep == 0:
            linestyle = '--'
            alpha = 0.5
            label = f'Epoch {ep} (Start)'
            color_name = "Blue-ish"
        elif ep == epochs_to_plot[-1]:
            linestyle = '-'
            alpha = 1.0
            label = f'Epoch {ep} (End)'
            color_name = "Red-ish"
        else:
            linestyle = '-'
            alpha = 0.7
            label = f'Epoch {ep}'
            color_name = "Intermediate"
            
        print(f"  - Epoch {ep}: Style='{linestyle}', Alpha={alpha}, Color~{color_name}")
        
        plt.plot(x_range, y_range, label=label, color=colors[i], lw=2, linestyle=linestyle, alpha=alpha)

plt.title('Evolution of Regression Line')
plt.legend()
plt.grid(True)
plt.show()
