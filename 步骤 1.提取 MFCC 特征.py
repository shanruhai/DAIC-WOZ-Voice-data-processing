import os
import numpy as np
import librosa
from pathlib import Path

# 设置输入和输出目录
data_dir = 'I:/DAICWOZ/wav/'  # WAV 文件所在的新目录
output_dir = 'I:/DAICWOZ/processed_features/'  # 保存特征的目录
os.makedirs(output_dir, exist_ok=True)

# 遍历 WAV 文件
for audio_file in os.listdir(data_dir):
    if audio_file.endswith('_AUDIO.wav'):
        # 提取文件名中的 ID，例如 "300_AUDIO.wav" -> "300"
        participant_id = audio_file.split('_')[0]
        audio_path = os.path.join(data_dir, audio_file)

        # 检查文件是否存在（冗余检查，通常不需要）
        if os.path.exists(audio_path):
            # 加载音频并提取 MFCC
            y, sr = librosa.load(audio_path, sr=16000)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

            # 保存 MFCC 特征，文件名格式为 "300_P.npy"
            save_path = os.path.join(output_dir, f'{participant_id}_P.npy')
            np.save(save_path, mfcc)
            print(f"保存 {participant_id}_P 的 MFCC 特征")
        else:
            print(f"警告: 文件 {audio_file} 不存在")