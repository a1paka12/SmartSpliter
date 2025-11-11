import os
import pandas as pd

def load_datasets(root_dir):
    """
    폴더 구조 예시:
    datasets/
        A/
            fake/
            real/
        B/
            fake/
            real/
    """
    records = []
    for domain in os.listdir(root_dir):
        domain_path = os.path.join(root_dir, domain)
        if not os.path.isdir(domain_path):
            continue

        for label in os.listdir(domain_path):
            label_path = os.path.join(domain_path, label)
            if not os.path.isdir(label_path):
                continue

            for fname in os.listdir(label_path):
                if fname.lower().endswith((".jpg", ".png", ".jpeg")):
                    records.append({
                        "id": len(records),
                        "domain": domain,
                        "label": label,
                        "path": os.path.join(domain, label, fname)
                    })
    return pd.DataFrame(records)

def save_csv(df, path):
    df.to_csv(path, index=False)
