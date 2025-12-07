
import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

# ============================================================================
# 1. 설정 및 데이터셋 클래스 (노트북과 동일)
# ============================================================================
BATCH_SIZE = 64
data_dir = "./data/asl_data"
train_csv = os.path.join(data_dir, "sign_mnist_train.csv")

class ASLDataset(Dataset):
    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        else:
            if not isinstance(image, torch.Tensor):
                image = torch.from_numpy(image).float()
        label = torch.tensor(label, dtype=torch.long)
        return image, label

# ============================================================================
# 2. 데이터 로드
# ============================================================================
if os.path.exists(train_csv):
    print("데이터 로드 중...")
    df_train = pd.read_csv(train_csv)
    
    train_labels = df_train.iloc[:, 0].values
    train_images = df_train.iloc[:, 1:].values.reshape(-1, 28, 28).astype(np.uint8)
    
    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.ToTensor(),
    ])
    
    train_dataset = ASLDataset(train_images, train_labels, transform=train_transform)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    print("데이터 로드 완료!")
else:
    print(f"파일을 찾을 수 없습니다: {train_csv}")
    exit()

# ============================================================================
# 3. 데이터 시각화 함수
# ============================================================================
def visualize_batch(loader, num_images=16):
    """
    데이터로더에서 배치를 가져와 이미지를 시각화합니다.
    """
    # 한 배치 가져오기
    images, labels = next(iter(loader))
    
    # 시각화할 이미지 개수 설정 (최대 배치 크기)
    num_images = min(num_images, len(images))
    
    # 그리드 크기 계산 (정사각형에 가깝게)
    rows = int(np.sqrt(num_images))
    cols = int(np.ceil(num_images / rows))
    
    plt.figure(figsize=(10, 10))
    for i in range(num_images):
        plt.subplot(rows, cols, i + 1)
        
        # 텐서를 이미지로 변환 (C, H, W) -> (H, W)
        # 흑백 이미지이므로 채널 차원 제거
        img = images[i].squeeze()
        
        plt.imshow(img, cmap='gray')
        
        # 레이블을 알파벳으로 변환 (0->A, 1->B, ...)
        label_idx = labels[i].item()
        label_char = chr(ord('A') + label_idx)
        
        plt.title(f"Label: {label_char} ({label_idx})")
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# 4. 시각화 실행
# ============================================================================
print("\n입력 데이터 시각화:")
visualize_batch(train_loader)
