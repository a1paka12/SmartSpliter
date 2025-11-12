🚀 SmartSplit: Multi-Domain, Multi-Class Dataset Splitter
SmartSplit은 AI 연구 및 대회를 위해 설계된 Python 유틸리티입니다. 복잡한 다중 도메인 및 다중 클래스 이미지 데이터셋을 지정된 비율(train/val/test)로 균형 있게 분할합니다.

Domain_A/dog/, Domain_B/cat/처럼 섞인 데이터셋을 입력하면, 완벽하게 균형 잡힌 train.csv, val.csv, test.csv 파일을 생성합니다.

💡 주요 기능
3가지 밸런싱 전략:

label (라벨 우선): 라벨 비율(e.g., dog:cat:bird = 1:1:1)을 완벽하게 보장합니다.

domain (도메인 우선): 도메인 비율(e.g., DomainA:DomainB = 1:1)을 완벽하게 보장합니다.

intersection (교집합): (DomainA, dog), (DomainB, cat) 등 모든 교집합 그룹의 수를 최소 그룹 기준으로 맞춥니다.

유연한 폴더 구조 지원: Domain/Class/file.jpg 구조와 Domain/class_file.jpg 구조를 모두 자동 탐지합니다.

CLI & Library: 터미널에서 간편하게 사용하거나, Python 스크립트에서 import하여 사용할 수 있습니다.

실행 전 검증: --stats-only (Dry Run) 옵션으로 데이터 스캔 결과와 밸런싱 계획을 미리 확인할 수 있습니다.

💾 설치
PyPI를 통해 간편하게 설치할 수 있습니다.

Bash

pip install SmartSpliter
📁 필수 데이터 폴더 구조
--data 인자로 지정한 폴더는 다음과 같은 "도메인" 하위 폴더를 가져야 합니다. io.py가 두 가지 구조를 모두 지원합니다.

구조 1: 클래스별 폴더 (권장)

datasets/
├── Domain_A/
│   ├── dog/
│   │   ├── dog_01.jpg
│   │   └── dog_02.jpg
│   └── cat/
│       └── cat_01.jpg
└── Domain_B/
    ├── dog/
    │   └── dog_03.jpg
    └── bird/
        └── bird_01.jpg
구조 2: 파일명에 클래스 포함

datasets/
├── Domain_C_shuffled/
│   ├── prefix_dog_pic.jpg
│   ├── prefix_cat_img.png
│   └── another_bird_file.jpg
└── Domain_D_mixed/
    ├── cat_folder/          (구조 1과)
    │   └── cat_in_box.jpg
    └── dog_on_grass.jpg     (구조 2가 혼용 가능)

📊 사용법 (CLI)
pip install SmartSpliter로 설치하면 SmartSplit 명령어를 터미널에서 즉시 사용할 수 있습니다.

기본 예시
datasets 폴더를 스캔하여 dog, cat, bird 클래스를 찾고, 라벨(label) 우선으로 8:1:1 비율로 분할합니다.

Bash

SmartSplit --data ./datasets --classes dog cat bird --ratio 8 1 1 --balance-mode label
or
python -m SmartSplit --data ./datasets --classes dog cat bird --ratio 8 1 1 --balance-mode label

전체 명령어 및 옵션
SmartSplit -h 실행 시 볼 수 있는 도움말입니다.

usage: smart-split [-h] --data DATA --classes CLASSES [CLASSES ...]
                   [--ratio RATIO RATIO RATIO]
                   [--balance-mode {label,domain,intersection}]
                   [--label-map LABEL_MAP] [--seed SEED] [--output OUTPUT]
                   [--stats-only] [--no-report]

SmartSplit - Multi-domain, Multi-class dataset splitter

options:
  -h, --help            show this help message and exit
  --data DATA           Path to the dataset directory (required)
  --classes CLASSES [CLASSES ...]
                        List of class names to find (e.g., dog cat bird). (required)
  --ratio RATIO RATIO RATIO
                        Train/Val/Test ratio (default: 8 1 1)

  --balance-mode {label,domain,intersection}
                        Balancing strategy (default: 'label'):
                        'label':        [라벨 우선]
                                        모든 라벨의 1:1:1... 비율을 보장합니다.
                                        (도메인 비율은 깨질 수 있습니다.)
                        'domain':       [도메인 우선]
                                        모든 도메인의 1:1:1... 비율을 보장합니다.
                                        (라벨 비율은 깨질 수 있습니다.)
                        'intersection': [교집합 (완벽 균형)]
                                        (도메인 x 라벨) 교집합의 최소 샘플 수로 모두 맞춥니다.
                                        (데이터 손실이 크거나 특정 라벨이 제외될 수 있습니다.)

  --label-map LABEL_MAP
                        [Optional] Map class names to integers. Example:
                        'dog:0,cat:1,bird:2'
  --seed SEED           Random seed (default: 42)
  --output OUTPUT       Output directory (default: ./output)

  --stats-only          [Helper] Run in 'dry-run' mode. Scans, counts, and
                        reports the balancing plan without splitting or saving.
  --no-report           Disable final ratio report output

🐍 사용법 (라이브러리)
Python 스크립트나 Jupyter Notebook에서 직접 import하여 사용할 수 있습니다.

예제 1: 기본 분할 실행
Python

from SmartSplit import SmartSplitter

# 1. 설정 정의
DATA_DIR = "./datasets"
CLASSES = ["dog", "cat", "bird"]
OUTPUT_DIR = "./output_from_script"

# 2. SmartSplitter 인스턴스 생성
splitter = SmartSplitter(
    data_path=DATA_DIR,
    class_list=CLASSES,
    balance_mode='label',  # 'domain' 또는 'intersection' 선택 가능
    label_map={'dog': 0, 'cat': 1, 'bird': 2}, # None으로 두면 라벨이 'dog', 'cat' 문자열로 저장됨
    ratio=(8, 1, 1),
    seed=42,
    output=OUTPUT_DIR
)

# 3. 분할 실행
# print() 문이 즉시 출력되도록 flush=True가 내장되어 있습니다.
splitter.run(report=True) 

print(f"작업 완료! {OUTPUT_DIR}에서 CSV 파일을 확인하세요.")
예제 2: 실행 전 스캔 (Dry Run)
splitter.run()을 호출하기 전에 --stats-only 헬퍼 기능을 사용할 수 있습니다.

Python

from SmartSplit import SmartSplitter

# 1. 스캔할 정보만 입력
splitter_check = SmartSplitter(
    data_path="./datasets",
    class_list=["dog", "cat", "bird", "rabbit"], # 일부러 존재하지 않는 클래스 포함
    balance_mode='label'
)

# 2. stats_only=True로 실행
print("데이터셋 스캔 및 밸런싱 계획을 확인합니다...")
splitter_check.run(stats_only=True)

#출력 예시:
Loading dependencies (pandas, sklearn)...
Loading datasets...
Scanning 2 domains...
Found structure: natures/... (parsing filenames)
Found structure: room/cat/...
Found structure: room/dog/...
Found structure: room/hamster/...
Found structure: room/rabbit/...
Found structure: sky/... (parsing filenames)
...Scan complete.

 ========================================
 📊 Raw Data Stats (Before Balancing)
 ========================================
 ...
 Class counts (raw):
 dog    5000
 cat    4500
 bird   1200
 Name: label, dtype: int64
 ...
 ========================================
 📋 Balancing Plan (PRIORITY: LABEL)
 ========================================
 Minority class is 'bird' with 1200 samples.
 All other classes will be downsampled to 1200 samples.

--stats-only mode enabled. Stopping...

⚠️ 문제 해결 (Troubleshooting)
ValueError: ...too few members... 또는 ValueError: The test_size...
가장 흔하게 발생하는 오류입니다.

ValueError: The least populated class in y has only 1 member, which is too few.
또는

ValueError: The test_size = 3 should be greater or equal to the number of classes = 4
원인: 이 오류는 sklearn이 데이터를 분할할 때 발생합니다. stratify(계층적 분할) 옵션은 train, val, test 세트 모두에 모든 클래스/그룹의 샘플이 최소 1개씩 들어가도록 하려고 합니다. 하지만 사용자가 지정한 --ratio에 비해 특정 클래스(또는 도메인, 교집합 그룹)의 샘플 수가 너무 적으면 분할이 불가능합니다.

해결책 (Rule of Thumb):

[밸런싱 후] 가장 적은 그룹의 파일 개수는 최소한 --ratio의 총합보다 많아야 합니다.

예시:

--ratio 8 1 1 (총합 10) → balance-mode로 선택된 최소 그룹이 최소 10개의 파일은 가져야 합니다.

--ratio 7 2 1 (총합 10) → 최소 10개의 파일이 필요합니다.

진단: 먼저 --stats-only 헬퍼 기능을 사용해 "Raw Data Stats" 리포트에서 각 클래스/도메인/교집합 그룹의 파일 개수를 확인하세요.

📜 라이선스
(여기에 MIT, Apache 2.0 등 원하는 라이선스 내용을 기재하세요.)