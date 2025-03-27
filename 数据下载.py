import requests
import os
from tqdm import tqdm
import threading
import queue
import time
import sys

# 文件列表（保持不变）
files = [
    "300_P.zip", "301_P.zip", "302_P.zip", "303_P.zip", "304_P.zip",
    "305_P.zip", "306_P.zip", "307_P.zip", "308_P.zip", "309_P.zip",
    "310_P.zip", "311_P.zip", "312_P.zip", "313_P.zip", "314_P.zip",
    "315_P.zip", "316_P.zip", "317_P.zip", "318_P.zip", "319_P.zip",
    "320_P.zip", "321_P.zip", "322_P.zip", "323_P.zip", "324_P.zip",
    "325_P.zip", "326_P.zip", "327_P.zip", "328_P.zip", "329_P.zip",
    "330_P.zip", "331_P.zip", "332_P.zip", "333_P.zip", "334_P.zip",
    "335_P.zip", "336_P.zip", "337_P.zip", "338_P.zip", "339_P.zip",
    "340_P.zip", "341_P.zip", "343_P.zip", "344_P.zip", "345_P.zip",
    "346_P.zip", "347_P.zip", "348_P.zip", "349_P.zip", "350_P.zip",
    "351_P.zip", "352_P.zip", "353_P.zip", "354_P.zip", "355_P.zip",
    "356_P.zip", "357_P.zip", "358_P.zip", "359_P.zip", "360_P.zip",
    "361_P.zip", "362_P.zip", "363_P.zip", "364_P.zip", "365_P.zip",
    "366_P.zip", "367_P.zip", "368_P.zip", "369_P.zip", "370_P.zip",
    "371_P.zip", "372_P.zip", "373_P.zip", "374_P.zip", "375_P.zip",
    "376_P.zip", "377_P.zip", "378_P.zip", "379_P.zip", "380_P.zip",
    "381_P.zip", "382_P.zip", "383_P.zip", "384_P.zip", "385_P.zip",
    "386_P.zip", "387_P.zip", "388_P.zip", "389_P.zip", "390_P.zip",
    "391_P.zip", "392_P.zip", "393_P.zip", "395_P.zip", "396_P.zip",
    "397_P.zip", "399_P.zip", "400_P.zip", "401_P.zip", "402_P.zip",
    "403_P.zip", "404_P.zip", "405_P.zip", "406_P.zip", "407_P.zip",
    "408_P.zip", "409_P.zip", "410_P.zip", "411_P.zip", "412_P.zip",
    "413_P.zip", "414_P.zip", "415_P.zip", "416_P.zip", "417_P.zip",
    "418_P.zip", "419_P.zip", "420_P.zip", "421_P.zip", "422_P.zip",
    "423_P.zip", "424_P.zip", "425_P.zip", "426_P.zip", "427_P.zip",
    "428_P.zip", "429_P.zip", "430_P.zip", "431_P.zip", "432_P.zip",
    "433_P.zip", "434_P.zip", "435_P.zip", "436_P.zip", "437_P.zip",
    "438_P.zip", "439_P.zip", "440_P.zip", "441_P.zip", "442_P.zip",
    "443_P.zip", "444_P.zip", "445_P.zip", "446_P.zip", "447_P.zip",
    "448_P.zip", "449_P.zip", "450_P.zip", "451_P.zip", "452_P.zip",
    "453_P.zip", "454_P.zip", "455_P.zip", "456_P.zip", "457_P.zip",
    "458_P.zip", "459_P.zip", "461_P.zip", "462_P.zip", "463_P.zip",
    "464_P.zip", "465_P.zip", "466_P.zip", "467_P.zip", "468_P.zip",
    "469_P.zip", "470_P.zip", "471_P.zip", "472_P.zip", "473_P.zip",
    "474_P.zip", "475_P.zip", "476_P.zip", "477_P.zip", "478_P.zip",
    "479_P.zip", "480_P.zip", "481_P.zip", "482_P.zip", "483_P.zip",
    "484_P.zip", "485_P.zip", "486_P.zip", "487_P.zip", "488_P.zip",
    "489_P.zip", "490_P.zip", "491_P.zip", "492_P.zip"
]

# 基础下载地址和目录
base_url = "XXXX"  #The URL where the data is downloaded  DAIC-WOZ
download_dir = r"I:\DAICWOZ"#Save the address
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 创建下载队列
download_queue = queue.Queue()
for file in files:
    download_queue.put(file)

# 创建线程锁以同步进度条输出
print_lock = threading.Lock()


# 检查终端是否支持 ANSI（仅适用于 Windows）
def check_ansi_support():
    if os.name == 'nt':  # Windows 系统
        try:
            import msvcrt
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)  # 启用 ANSI 支持
        except:
            print("警告：当前终端可能不支持进度条原位更新。")
            print(
                "建议：1. 使用 PowerShell 或 Windows Terminal；2. 在 CMD 中运行 'reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f' 并重启 CMD。")
            return False
    return True


# 下载函数
def download_file(file, base_url, download_dir, thread_id, max_retries=3):
    url = base_url + file
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            file_path = os.path.join(download_dir, file)
            # 创建进度条，固定位置和更新频率
            with print_lock:
                pbar = tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    desc=f"{file} [Thread-{thread_id}]",
                    leave=True,  # 完成后保留进度条
                    position=thread_id,  # 为每个线程分配固定位置
                    ncols=100,  # 固定进度条宽度
                    mininterval=1,  # 每秒更新一次，减少刷新频率
                )

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=16384):
                    f.write(chunk)
                    with print_lock:
                        pbar.update(len(chunk))
            with print_lock:
                pbar.close()
                print(f"\n下载完成: {file}")
            return
        except requests.RequestException as e:
            with print_lock:
                print(f"\n下载失败 {file} (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                download_queue.put(file)


# 工作线程函数
def worker(thread_id):
    while True:
        try:
            file = download_queue.get(timeout=5)
            download_file(file, base_url, download_dir, thread_id)
            download_queue.task_done()
        except queue.Empty:
            break


# 主函数
def main():
    # 检查终端支持
    check_ansi_support()

    num_threads = 2
    threads = []

    print(f"开始下载，总文件数: {len(files)}，使用 {num_threads} 个线程")

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,), name=f"Worker-{i}")
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if download_queue.empty():
        print("所有文件下载完成！")
    else:
        print(f"下载完成，但仍有 {download_queue.qsize()} 个文件未成功下载")


if __name__ == "__main__":
    main()