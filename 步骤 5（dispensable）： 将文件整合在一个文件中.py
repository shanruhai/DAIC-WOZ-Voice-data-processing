import numpy as np
import os

# 输入路径
data_dir = 'I:/DAICWOZ/processed_data/'
output_dir = 'D:/python/learn/SER_depression-master/preprocess/data/'
os.makedirs(output_dir, exist_ok=True)

# 加载特征和标签
train_features = np.load(os.path.join(data_dir, 'train_features.npy'))
dev_features = np.load(os.path.join(data_dir, 'dev_features.npy'))
test_features = np.load(os.path.join(data_dir, 'test_features.npy'))
train_labels = np.load(os.path.join(data_dir, 'train_labels.npy'))
dev_labels = np.load(os.path.join(data_dir, 'dev_labels.npy'))
test_labels = np.load(os.path.join(data_dir, 'test_labels.npy'))

# 合并数据
x = np.concatenate([train_features, dev_features, test_features], axis=0)  # 形状: (总样本数, 1000, 40)
y = np.concatenate([train_labels, dev_labels, test_labels], axis=0)       # 形状: (总样本数,)

# 保存为 SER_depression-master 期望的格式
data = {'x': x, 'y': y}
np.save(os.path.join(output_dir, 'DAICWOZ_V1_order3.npy'), data)
print(f"保存数据到 {output_dir}DAICWOZ_V1_order3.npy，特征形状: {x.shape}, 标签形状: {y.shape}")