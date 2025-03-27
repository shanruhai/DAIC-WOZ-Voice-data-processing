import os
import numpy as np
import pandas as pd
from pathlib import Path

# 设置路径
feature_dir = 'I:/DAICWOZ/processed_features/'
csv_dir = 'I:/DAICWOZ/'
output_dir = 'I:/DAICWOZ/processed_data/'
os.makedirs(output_dir, exist_ok=True)

# 分割文件夹
splits = {
    'train': os.path.join(feature_dir, 'train'),
    'dev': os.path.join(feature_dir, 'dev'),
    'test': os.path.join(feature_dir, 'test')
}

# 读取分割文件
train_df = pd.read_csv(os.path.join(csv_dir, 'train_split_Depression_AVEC2017.csv'))
dev_df = pd.read_csv(os.path.join(csv_dir, 'dev_split_Depression_AVEC2017.csv'))
test_df = pd.read_csv(os.path.join(csv_dir, 'test_split_Depression_AVEC2017.csv'))

# 创建 ID 到标签的映射
label_dict = {}
for df, split_name in [(train_df, 'train'), (dev_df, 'dev')]:
    id_col = 'Participant_ID'
    for pid, label in zip(df[id_col].astype(str), df['PHQ8_Binary']):
        label_dict[pid] = label

# 测试集 ID
test_ids = set(test_df['participant_ID'].astype(str).values)

# 指定最大帧数和特征维度
MAX_FRAMES = 1000
FEATURE_DIM = 40


def pad_or_truncate(feature, max_frames, feature_dim):
    """填充或截断特征到指定形状 (max_frames, feature_dim)"""
    current_frames, current_dim = feature.shape
    # 调整时间维度
    if current_frames > max_frames:
        feature = feature[:max_frames, :]
    elif current_frames < max_frames:
        feature = np.pad(feature, ((0, max_frames - current_frames), (0, 0)), mode='constant')
    # 调整特征维度
    if current_dim > feature_dim:
        feature = feature[:, :feature_dim]
    elif current_dim < feature_dim:
        feature = np.pad(feature, ((0, 0), (0, feature_dim - current_dim)), mode='constant')
    return feature


# 处理每个分割
for split_name, split_dir in splits.items():
    features = []
    labels = []

    for feature_file in os.listdir(split_dir):
        if feature_file.endswith('_P.npy'):
            participant_id = feature_file.split('_')[0]
            feature_path = os.path.join(split_dir, feature_file)

            # 加载并调整特征
            feature = np.load(feature_path)
            feature = pad_or_truncate(feature, MAX_FRAMES, FEATURE_DIM)
            features.append(feature)

            # 处理标签
            if split_name in ['train', 'dev']:
                if participant_id in label_dict:
                    labels.append(label_dict[participant_id])
                else:
                    print(f"警告: {participant_id} 在 {split_name} 中没有找到标签，跳过")
                    continue
            elif split_name == 'test':
                labels.append(-1)

    # 转换为 NumPy 数组
    features_array = np.stack(features)  # 形状: (样本数, MAX_FRAMES, FEATURE_DIM)
    labels_array = np.array(labels)  # 形状: (样本数,)

    # 保存结果
    np.save(os.path.join(output_dir, f'{split_name}_features.npy'), features_array)
    np.save(os.path.join(output_dir, f'{split_name}_labels.npy'), labels_array)
    print(f"保存 {split_name} 数据: 特征形状 {features_array.shape}, 标签形状 {labels_array.shape}")

print("特征聚合并填充完成！")