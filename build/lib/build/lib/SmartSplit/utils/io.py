# smart_split/utils/io.py

import os
import re

def parse_label_from_filename(fname, class_list):
    """ 
    파일명(fname)에 class_list(e.g., ['dog', 'cat'])의 키워드가 포함되어 있는지 확인.
    정확도를 위해 _class, .class, class_ 등으로 구분된 경우를 우선 탐색.
    """
    fname_lower = fname.lower()
    
    # 1순위: 구분자(_ . -)로 분리된 정확한 클래스명 탐색
    for class_name in class_list:
        # e.g., "my_dog_01.jpg", "happy.cat.png", "bird-flying.jpg"
        if re.search(f'[_.-]{re.escape(class_name)}[_.-]', fname_lower):
            return class_name
        # e.g., "dog_01.jpg", "cat.png"
        if fname_lower.startswith(f'{class_name}_') or fname_lower.startswith(f'{class_name}.'):
             return class_name

    # 2순위: 1순위에서 못찾으면 단순 포함 탐색 (e.g., "bigdoghouse.jpg" -> 'dog')
    # (주의: 'wolf' 클래스가 'wolfdog' 파일명에 매칭될 수 있음)
    for class_name in class_list:
        if class_name in fname_lower:
            return class_name
            
    return None

def load_datasets(root_dir, class_list, label_map):
    """
    두 가지 폴더 구조를 모두 지원:
    1. root_dir/Domain/Class/file.jpg 
    2. root_dir/Domain/shuffled_file_with_class_name.jpg
    
    class_list: ['dog', 'cat', 'bird']
    label_map: {'dog': 0, 'cat': 1, 'bird': 2}
    """
    records = []

    for domain in os.listdir(root_dir):
        domain_path = os.path.join(root_dir, domain)
        if not os.path.isdir(domain_path):
            continue

        # 하위 폴더 탐색 (Structure 1: Domain/Class/file.jpg)
        is_structure_1 = False
        for sub_name in os.listdir(domain_path):
            sub_path = os.path.join(domain_path, sub_name)
            
            # 하위 폴더 이름이 'dog', 'cat' 등 클래스 리스트와 일치하는지 확인
            if os.path.isdir(sub_path) and sub_name in class_list:
                is_structure_1 = True
                print(f"Found structure: {domain}/{sub_name}/...", flush=True)
                for fname in os.listdir(sub_path):
                    if fname.lower().endswith((".jpg", ".png", ".jpeg")):
                        records.append({
                            "id": len(records),
                            "domain": domain,
                            "label": label_map[sub_name], # 0, 1, 2 등으로 변환
                            "path": os.path.join(domain, sub_name, fname)
                        })

        # Structure 1이 아니었다면 Structure 2 (Domain/shuffled.jpg)로 간주
        if not is_structure_1:
            print(f"Found structure: {domain}/... (parsing filenames)", flush=True)
            for fname in os.listdir(domain_path):
                if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
                    continue
                
                # 파일명에서 'dog', 'cat' 등 파싱
                parsed_class = parse_label_from_filename(fname, class_list)
                
                if parsed_class:
                    records.append({
                        "id": len(records),
                        "domain": domain,
                        "label": label_map[parsed_class], # 0, 1, 2 등으로 변환
                        "path": os.path.join(domain, fname)
                    })
                # else:
                #     print(f"Warning: Skipping file, cannot parse class: {fname}")
    print("...Scan complete.", flush=True)
    import pandas as pd
    return pd.DataFrame(records)

def save_csv(df, path):
    df.to_csv(path, index=False)