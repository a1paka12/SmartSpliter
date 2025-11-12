import os
from SmartSplit import SmartSplitter

# 1. 분할에 필요한 설정값들을 정의합니다.
DATA_DIR = "./sample_datasets"
CLASSES = ["dog", "cat", "hamster", "rabbit"]
ENCODING_MAP = {"dog": 0, "cat": 1, "bird": 2}

current_script_path = os.path.abspath(__file__)

current_script_dir = os.path.dirname(current_script_path)

target_folder_path = os.path.join(current_script_dir, "intersection_output") # (e.g., C:\project\output)

dataset_folder_path = os.path.join(current_script_dir, DATA_DIR)

os.makedirs(target_folder_path, exist_ok=True)

# 2. SmartSplitter 인스턴스를 생성합니다.
splitter = SmartSplitter(
    data_path=dataset_folder_path,
    class_list=CLASSES,
    label_map=ENCODING_MAP,  # 라벨 인코딩 맵을 전달
    ratio=(8, 1, 1),       # 튜플 형태로 비율 전달
    seed=42,
    output=target_folder_path
)

# 3. 분할 작업을 실행합니다.
# report=True가 기본값이지만 명시적으로 켜고 끌 수 있습니다.
splitter.run(report=True)