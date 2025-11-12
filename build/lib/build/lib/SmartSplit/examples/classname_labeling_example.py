import os
from SmartSplit import SmartSplitter

# 1. 경로와 클래스만 설정
DATA_DIR = "./sample_datasets"
CLASSES = ["dog", "cat", "hamster", "rabbit"]

current_script_path = os.path.abspath(__file__)

current_script_dir = os.path.dirname(current_script_path)

target_folder_path = os.path.join(current_script_dir, "intersection_output") # (e.g., C:\project\output)

dataset_folder_path = os.path.join(current_script_dir, DATA_DIR)

os.makedirs(target_folder_path, exist_ok=True)

# 2. 인스턴스 생성
# output, ratio 등은 dry-run에 필요 없으므로 생략 가능
splitter_check = SmartSplitter(
    data_path=dataset_folder_path,
    class_list=CLASSES
)

# 3. stats_only=True 플래그로 run() 호출
print("데이터셋 스캔 및 밸런싱 계획을 확인합니다...")
splitter_check.run(stats_only=True)