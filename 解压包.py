import os
import zipfile
import shutil
from tqdm import tqdm  # 用于显示进度条


def unzip_daic_woz(zip_dir, extract_dir, wav_output_dir):
    """
    解压 DAIC-WOZ 数据集的 ZIP 文件，并将所有 WAV 文件移动到指定目录。

    参数:
        zip_dir (str): ZIP 文件所在的目录
        extract_dir (str): 解压后文件存储的目录
        wav_output_dir (str): WAV 文件最终存储的目录
    """
    # 确保输出目录和 WAV 目录存在
    os.makedirs(extract_dir, exist_ok=True)
    os.makedirs(wav_output_dir, exist_ok=True)

    # 获取所有 ZIP 文件的列表（300_P.zip 到 492_P.zip）
    expected_files = [f"{i}_P.zip" for i in range(300, 493)]
    found_files = [f for f in os.listdir(zip_dir) if f.endswith("_P.zip")]

    # 检查缺失的文件
    missing_files = set(expected_files) - set(found_files)
    if missing_files:
        print(f"警告: 以下文件缺失: {sorted(missing_files)}")

    # 解压文件
    for zip_file in tqdm(found_files, desc="解压进度"):
        zip_path = os.path.join(zip_dir, zip_file)
        participant_id = zip_file.split("_")[0]  # 提取如 "300" 的 ID
        extract_path = os.path.join(extract_dir, f"{participant_id}_P")  # 每个受访者独立目录

        try:
            # 创建受访者特定的解压目录
            os.makedirs(extract_path, exist_ok=True)

            # 打开并解压 ZIP 文件
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"成功解压: {zip_file} -> {extract_path}")

            # 移动 WAV 文件到 wav_output_dir
            for root, _, files in os.walk(extract_path):
                for file in files:
                    if file.endswith(".wav"):
                        src_path = os.path.join(root, file)
                        dst_path = os.path.join(wav_output_dir, file)
                        # 如果目标文件已存在，添加受访者 ID 前缀避免覆盖
                        if os.path.exists(dst_path):
                            dst_path = os.path.join(wav_output_dir, f"{participant_id}_{file}")
                        shutil.move(src_path, dst_path)
                        print(f"移动 WAV 文件: {src_path} -> {dst_path}")

        except zipfile.BadZipFile:
            print(f"错误: {zip_file} 是一个损坏的 ZIP 文件")
        except Exception as e:
            print(f"处理 {zip_file} 时出错: {str(e)}")

    # 可选：删除解压后的临时目录
    # shutil.rmtree(extract_dir)


if __name__ == "__main__":
    # 设置路径
    zip_dir = "I:/DAICWOZ"          # ZIP 文件所在目录
    extract_dir = "I:/DAICWOZ/extracted"  # 解压后临时目录
    wav_output_dir = "I:/DAICWOZ/wav"     # WAV 文件最终目录

    # 运行解压和移动
    unzip_daic_woz(zip_dir, extract_dir, wav_output_dir)