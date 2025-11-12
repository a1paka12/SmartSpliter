import os
from SmartSplit import SmartSplitter

# 1. 설정 정의 (label_map=None)
DATA_DIR = "./sample_datasets"
CLASSES = ["dog", "cat", "hamster", "rabbit"]

current_script_path = os.path.abspath(__file__)

current_script_dir = os.path.dirname(current_script_path)

target_folder_path = os.path.join(current_script_dir, "intersection_output") # (e.g., C:\project\output)

dataset_folder_path = os.path.join(current_script_dir, DATA_DIR)

os.makedirs(target_folder_path, exist_ok=True)

# 2. 인스턴스 생성
splitter = SmartSplitter(
    data_path=dataset_folder_path,
    class_list=CLASSES,
    label_map=None,      # 이 부분을 None으로 설정
    balance_mode='label', # label, domain, intersection
    ratio=(7, 2, 1),   # 다른 비율도 가능
    output=target_folder_path
)

splitter1 = SmartSplitter(
    data_path=dataset_folder_path,
    class_list=CLASSES,
    label_map=None,      # 이 부분을 None으로 설정
    balance_mode='domain', # label, domain, intersection
    ratio=(7, 2, 1),   # 다른 비율도 가능
    output=target_folder_path
)

splitter2 = SmartSplitter(
    data_path=dataset_folder_path,
    class_list=CLASSES,
    label_map=None,      # 이 부분을 None으로 설정
    balance_mode='intersection', # label, domain, intersection
    ratio=(7, 2, 1),   # 다른 비율도 가능
    output=target_folder_path
)

#3. 실행
# splitter.run(stats_only=True)
splitter.run()
# splitter1.run()
# splitter2.run()