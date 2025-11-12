# 🚀 SmartSplit : Multi-Domain, Multi-Class Dataset Splitter


SmartSplit is a Python utility designed for AI research and competitions. 

It splits complex multi-domain and multi-class image datasets into balanced segments (train/val/test) at specified ratios.

If you input a mixed dataset like Domain_A/dog/, Domain_B/cat/, it will generate perfectly balanced train.csv, val.csv, and test.csv files.

# 💡 Introduce
* **Three** balancing strategies:

  * **label priority** : Perfectly guarantees label ratios (e.g., dog:cat:bird = 1:1:1).

  * **domain priority** : Perfectly guarantees domain ratios (e.g., DomainA:DomainB = 1:1).

  * **intersection** : Matches all intersection groups, such as (DomainA, dog) and (DomainB, cat), to the minimum group count.

* Flexible folder structure support: Automatically detects the following structures.
  ```
  Domain/Class/file.jpg
  Domain/class_file.jpg 
  ```

* CLI & Library : Easy to use from the **terminal** or **import** into a Python script.

* Pre-run verification: Preview the data scan results and balancing plan with the --stats-only (Dry Run) option.

# 💾 Installation
It can be easily installed via pip.

bash Shell
```
pip install SmartSplitter
```

# 📁 Required Data Folder Structure
The folder specified as the data argument must have the following "domain" subfolders.

io.py supports the following both structures.

Structure 1: Folders by class (recommended)
```
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
```
Structure 2: Including the class in the file name
```

datasets/
├── Domain_C_shuffled/
│   ├── prefix_dog_pic.jpg
│   ├── prefix_cat_img.png
│   └── another_bird_file.jpg
└── Domain_D_mixed/
    ├── cat_folder/
    │    └── cat_in_box.jpg
    ├── dog_folder/   
         └── dog_on_grass.jpg
```

**Structure 1 and Structure 2 can be mixed**

# 📊 Usage (CLI)
Installing
```
pip install SmartSplitter
```
make the SmartSplit command immediately available in your terminal.


* Basic example

   Scan the datasets folder to find dog, cat, and bird classes, and split them in a 8:1:1 ratio with labels first.

  Bash Shell
  ```bash
  SmartSplit --data ./datasets --classes dog cat bird --ratio 8 1 1 --balance-mode label
  ```
  or
  ```bash
  python -m SmartSplit --data ./datasets --classes dog cat bird --ratio 8 1 1 --balance-mode label
  ```

* Full commands and options

  Here's the help you'll see when you run **SmartSplit -h**.

```

smart-split [-h] --data DATA --classes CLASSES [CLASSES ...]
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
                        'label':        [Label priority]
                Guarantees a 1:1:1... ratio for all labels.
                (Domain ratios may be broken.)
'domain':       [Domain priority]
                Guarantees a 1:1:1... ratio for all domains.
                (Label ratios may be broken.)
'intersection': [Intersection (perfect balance)]
                Matches all domains to the minimum number of samples in the (domain x label) intersection.
                (Data loss may be significant or certain labels may be excluded.)

  --label-map LABEL_MAP
                        [Optional] Map class names to integers. Example:
                        'dog:0,cat:1,bird:2'
  --seed SEED           Random seed (default: 42)
  --output OUTPUT       Output directory (default: ./output)

  --stats-only          [Helper] Run in 'dry-run' mode. Scans, counts, and
                        reports the balancing plan without splitting or saving.
  --no-report           Disable final ratio report output
```
# 🔧Usage (Library)
You can import and use it directly in a Python script or Jupyter Notebook.

* **Example 1**: Running a basic split

```python
import os
from SmartSplitter import SmartSplitter

# Setting Definition
DATA_DIR = "./datasets"
CLASSES = ["dog", "cat", "bird"]
DATA_DIR = "./sample_datasets"
CLASSES = ["dog", "cat", "hamster", "rabbit"]

current_script_path = os.path.abspath(__file__)

current_script_dir = os.path.dirname(current_script_path)

target_folder_path = os.path.join(current_script_dir, "intersection_output") # (e.g., C:\project\output)

dataset_folder_path = os.path.join(current_script_dir, DATA_DIR)

os.makedirs(target_folder_path, exist_ok=True)

# Creating a SmartSplitter instance
splitter = SmartSplitter(
    data_path=dataset_folder_path,
    class_list=CLASSES,
    balance_mode='label',  # You can choose 'domain' or 'intersection'
    label_map={'dog': 0, 'cat': 1, 'bird': 2}, # If left as None, the label will be saved as the string 'dog', 'cat'
    ratio=(8, 1, 1),
    seed=42,
    output=target_folder_path
)

# split execution
splitter.run(report=True) 

print(f"작업 완료! {OUTPUT_DIR}에서 CSV 파일을 확인하세요.")
```

* **Example 2** : Scan before execution (Dry Run)
You can use the --stats-only helper function before calling splitter.run().

```python

from SmartSplitter import SmartSplitter

# Enter only the information you want to scan
splitter_check = SmartSplitter(
    data_path="./datasets",
    class_list=["dog", "cat", "bird", "rabbit"], # Including classes that intentionally do not exist
    balance_mode='label'
)

# Run with stats_only=True
print("Check the dataset scan and balancing plan...")
splitter_check.run(stats_only=True)
```


**Output example :**
```bash
Loading datasets...
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
Total files found: 54

Class counts (raw):
label
rabbit     21
hamster    13
dog        10
cat        10
Name: count, dtype: int64

Domain counts (raw):
domain
room       24
natures    15
sky        15
Name: count, dtype: int64

Counts per (Domain, Label):
domain   label
natures  rabbit     8
         hamster    3
         cat        2
         dog        2
room     cat        6
         dog        6
         hamster    6
         rabbit     6
sky      rabbit     7
         hamster    4
         cat        2
         dog        2
Name: count, dtype: int64
========================================

--stats-only mode enabled with --balance-mode='label'.
Stopping before balancing, splitting, or saving.
========================================
```
# ⚠️ Troubleshooting

```
FileNotFoundError: ...
```
This error occurs after installing the os module and entering os.path as data_path.

These are the most common error.

```
**ValueError: ...too few members...** 

or 

**ValueError: The test_size...**

or

**ValueError: The least populated class in y has only 1 member, which is too few.** 

or

**ValueError: The test_size = 3 should be greater or equal to the number of classes = 4**
```

**Cause:**

This error occurs when sklearn splits the data. 
The stratify option attempts to ensure that each class/group has at least one sample in each of the train, val, and test sets. 

However, if the number of samples for a particular class (or domain, or intersection group) is too small compared to the user-specified --ratio, splitting is not possible.

**Rule of Thumb :**

**[After balancing]** The number of files in the smallest group must be at least as large as the sum of --ratio.

**Example :**

--ratio 8 1 1 (Total 10) → The minimum group selected with balance-mode must have at least 10 files.

--ratio 7 2 1 (Total 10) → At least 10 files are required.

**Diagnosis :**

First, use the --stats-only helper function to check the number of files in each class/domain/intersection group in the "Raw Data Stats" report.
# 📜 License
[LICENSE](https://raw.githubusercontent.com/a1paka12/SmartSpliter/refs/heads/main/LICENSE)
# 🎞Copyright for sample photos
All photos were downloaded from [pixabay](https://pixabay.com/en/).