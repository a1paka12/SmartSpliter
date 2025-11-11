import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from .utils.io import load_datasets, save_csv
from .utils.stats import print_ratio_report

class SmartSplitter:
    """
    Multi-domain, multi-class dataset splitter
    - Keeps domain balance (A/B/C/...)
    - Keeps label balance (real/fake)
    """

    def __init__(self, data_path, label_col="label", ratio=(8,1,1), seed=42, output="./output"):
        self.data_path = data_path
        self.label_col = label_col
        self.ratio = np.array(ratio)
        self.seed = seed
        self.output = output

    def balance_domains(self, df):
        """
        각 도메인(domain)별 real/fake 개수를 확인하고,
        최소한의 수로 잘라서 균형을 맞춤
        """
        balanced = []
        domains = df['domain'].unique()

        for domain in domains:
            sub = df[df['domain'] == domain]
            counts = sub[self.label_col].value_counts()
            if len(counts) < 2:
                continue
            min_count = counts.min()
            balanced.append(
                sub.groupby(self.label_col, group_keys=False).apply(lambda x: x.sample(min_count, random_state=self.seed))
            )
        return pd.concat(balanced).reset_index(drop=True)

    def split(self):
        df = load_datasets(self.data_path)
        df = self.balance_domains(df)

        train_ratio, val_ratio, test_ratio = self.ratio / self.ratio.sum()
        train_df, temp_df = train_test_split(
            df, test_size=(1 - train_ratio),
            stratify=df[self.label_col], random_state=self.seed
        )

        relative_val = val_ratio / (val_ratio + test_ratio)
        val_df, test_df = train_test_split(
            temp_df, test_size=(1 - relative_val),
            stratify=temp_df[self.label_col], random_state=self.seed
        )

        return train_df, val_df, test_df

    def save(self, train_df, val_df, test_df):
        os.makedirs(self.output, exist_ok=True)
        save_csv(train_df, os.path.join(self.output, "train.csv"))
        save_csv(val_df, os.path.join(self.output, "val.csv"))
        save_csv(test_df, os.path.join(self.output, "test.csv"))

    def run(self, report=True):
        train_df, val_df, test_df = self.split()
        self.save(train_df, val_df, test_df)
        if report:
            print_ratio_report(train_df, val_df, test_df, label_col=self.label_col)
        print(f"✅ Split complete! Files saved in {self.output}")
