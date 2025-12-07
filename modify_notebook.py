
import json
import os

nb_path = '/Users/jhkim/Library/CloudStorage/GoogleDrive-jhkim3217@gmail.com/내 드라이브/강의자료/Vibe_Coding/gradient_descent_tutorial.ipynb'

if not os.path.exists(nb_path):
    print(f"Error: File not found at {nb_path}")
    exit(1)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 시각화 셀 찾아서 수정하기
found_viz_cell = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "plt.title('Evolution of Regression Line')" in source:
            # 새로운 시각화 코드로 교체 (색상 및 스타일 개선)
            new_source = [
                "import matplotlib.pyplot as plt\n",
                "import numpy as np\n",
                "\n",
                "plt.figure(figsize=(15, 6))\n",
                "\n",
                "# 1. Loss 변화 그래프\n",
                "plt.subplot(1, 2, 1)\n",
                "plt.plot(losses, 'r-o')\n",
                "plt.title('Change of Loss (Cost)')\n",
                "plt.xlabel('Epoch')\n",
                "plt.ylabel('Loss')\n",
                "plt.grid(True)\n",
                "\n",
                "# 2. 회귀선 변화 그래프\n",
                "plt.subplot(1, 2, 2)\n",
                "plt.scatter(x_train, y_train, c='black', label='Data', s=100, zorder=10)\n",
                "\n",
                "# 주요 에포크의 선 그리기\n",
                "epochs_to_plot = [0, 1, 3, 5, 10, 20]\n",
                "x_range = np.linspace(0, 4, 100)\n",
                "\n",
                "# 색상 맵 변경 (coolwarm: 파랑 -> 빨강)\n",
                "colors = plt.cm.coolwarm(np.linspace(0, 1, len(epochs_to_plot)))\n",
                "\n",
                "for i, ep in enumerate(epochs_to_plot):\n",
                "    if ep < len(W_history):\n",
                "        w_val = W_history[ep]\n",
                "        b_val = b_history[ep]\n",
                "        y_range = w_val * x_range + b_val\n",
                "        \n",
                "        # 선 스타일 및 투명도 조정\n",
                "        if ep == 0:\n",
                "            linestyle = '--' # 초기값은 점선\n",
                "            alpha = 0.5\n",
                "            label = f'Epoch {ep} (Start)'\n",
                "        elif ep == epochs_to_plot[-1]:\n",
                "            linestyle = '-'  # 최종값은 실선\n",
                "            alpha = 1.0\n",
                "            label = f'Epoch {ep} (End)'\n",
                "        else:\n",
                "            linestyle = '-'\n",
                "            alpha = 0.7\n",
                "            label = f'Epoch {ep}'\n",
                "            \n",
                "        plt.plot(x_range, y_range, label=label, color=colors[i], lw=2, linestyle=linestyle, alpha=alpha)\n",
                "\n",
                "plt.title('Evolution of Regression Line')\n",
                "plt.legend()\n",
                "plt.grid(True)\n",
                "plt.show()"
            ]
            cell['source'] = new_source
            found_viz_cell = True
            break

if not found_viz_cell:
    print("Warning: Could not find the visualization cell to modify.")

# 파일 저장
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Successfully modified {nb_path}")
