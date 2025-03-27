import pandas as pd
import os
import shutil
from pathlib import Path

# 设置路径
feature_dir = 'I:/DAICWOZ/processed_features/'
csv_dir = 'I:/DAICWOZ/'

# 创建目标子文件夹
train_dir = os.path.join(feature_dir, 'train')
dev_dir = os.path.join(feature_dir, 'dev')
test_dir = os.path.join(feature_dir, 'test')
os.makedirs(train_dir, exist_ok=True)
os.makedirs(dev_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 读取分割文件
train_df = pd.read_csv(os.path.join(csv_dir, 'train_split_Depression_AVEC2017.csv'))
dev_df = pd.read_csv(os.path.join(csv_dir, 'dev_split_Depression_AVEC2017.csv'))
test_df = pd.read_csv(os.path.join(csv_dir, 'test_split_Depression_AVEC2017.csv'))

# 获取受访者 ID（根据每个文件的实际列名）
train_ids = set(train_df['Participant_ID'].astype(str).values)  # 大写 'P'
dev_ids = set(dev_df['Participant_ID'].astype(str).values)     # 大写 'P'
test_ids = set(test_df['participant_ID'].astype(str).values)   # 小写 'p'

# 检查 ID 是否有重叠
overlap = train_ids & dev_ids & test_ids
if overlap:
    print(f"警告: 以下 ID 在多个分割中重复: {overlap}")

# 移动特征文件
for feature_file in os.listdir(feature_dir):
    if feature_file.endswith('_P.npy'):
        participant_id = feature_file.split('_')[0]
        src_path = os.path.join(feature_dir, feature_file)

        if participant_id in train_ids:
            dst_path = os.path.join(train_dir, feature_file)
        elif participant_id in dev_ids:
            dst_path = os.path.join(dev_dir, feature_file)
        elif participant_id in test_ids:
            dst_path = os.path.join(test_dir, feature_file)
        else:
            print(f"警告: {participant_id} 未在任何分割文件中找到，跳过")
            continue

        try:
            shutil.move(src_path, dst_path)
            print(f"移动 {feature_file} 到 {dst_path}")
        except Exception as e:
            print(f"移动 {feature_file} 时出错: {str(e)}")

print("数据分割完成！")