# smart_split/core.py

import os
import pandas as pd
import numpy as np
from .utils.io import load_datasets, save_csv
from .utils.stats import print_ratio_report

class SmartSplitter:
    """
    Multi-domain, multi-class dataset splitter
    Offers 3 balancing strategies: 'label', 'domain', 'intersection'
    """

    def __init__(self, data_path, class_list, label_map=None, balance_mode="label", label_col="label", ratio=(8,1,1), seed=42, output="./output"):
        self.data_path = data_path
        self.class_list = class_list
        self.label_map = label_map
        self.balance_mode = balance_mode
        self.label_col = label_col
        self.ratio = np.array(ratio)
        self.seed = seed
        self.output = output
        self.rng = np.random.RandomState(seed)
        self.load_map = self.label_map if self.label_map else {c: c for c in self.class_list}

    # --- 샘플링 헬퍼 ---
    def _sample_uniformly(self, df, group_by_col, target_count):
        """
        DataFrame(df)에서 target_count만큼 샘플링합니다.
        샘플링 시, group_by_col(예: 'label' 또는 'domain')의 비율을 최대한 맞춥니다.
        """
        groups = df[group_by_col].unique()
        n_groups = len(groups)
        
        if n_groups == 0:
            return df.sample(n=min(target_count, len(df)), random_state=self.seed)

        samples_per_group = target_count // n_groups
        remainder = target_count % n_groups

        balanced_dfs = []
        shuffled_groups = self.rng.permutation(groups)
        
        for i, group_val in enumerate(shuffled_groups):
            group_df = df[df[group_by_col] == group_val]
            
            n_to_sample = samples_per_group + (1 if i < remainder else 0)
            n_to_sample = min(n_to_sample, len(group_df)) 
            
            if n_to_sample > 0:
                balanced_dfs.append(group_df.sample(n=n_to_sample, random_state=self.seed))

        final_df = pd.concat(balanced_dfs) if balanced_dfs else pd.DataFrame(columns=df.columns)
        
        gap = target_count - len(final_df)
        if gap > 0:
            available_df = df[~df.index.isin(final_df.index)]
            n_to_fill = min(gap, len(available_df)) 
            if n_to_fill > 0:
                gap_df = available_df.sample(n=n_to_fill, random_state=self.seed)
                final_df = pd.concat([final_df, gap_df])

        return final_df.sample(frac=1, random_state=self.seed)

    # --- 밸런싱 전략 1: 라벨 우선 ---
    def _split_by_label_priority(self, df):
        class_counts = df[self.label_col].value_counts()
        min_class_count = class_counts.min()
        
        print(f"Balancing Plan [Label Priority]: Downsampling all classes to {min_class_count} samples.")

        balanced_dfs = []
        for class_name in self.class_list:
            label_val = self.load_map[class_name]
            class_df = df[df[self.label_col] == label_val]
            
            if len(class_df) == 0: continue

            if len(class_df) <= min_class_count:
                balanced_dfs.append(class_df)
            else:
                # [라벨 우선] 다수 라벨 -> '도메인' 균형 샘플링
                balanced_class_df = self._sample_uniformly(
                    class_df, 
                    group_by_col='domain', # 도메인 균형
                    target_count=min_class_count
                )
                balanced_dfs.append(balanced_class_df)
        
        balanced_df = pd.concat(balanced_dfs).reset_index(drop=True)
        # 분할 기준: 라벨
        return balanced_df, self.label_col 

    # --- 밸런싱 전략 2: 도메인 우선 ---
    def _split_by_domain_priority(self, df):
        domain_counts = df['domain'].value_counts()
        min_domain_count = domain_counts.min()
        
        print(f"Balancing Plan [Domain Priority]: Downsampling all domains to {min_domain_count} samples.")
        
        balanced_dfs = []
        for domain_name in df['domain'].unique():
            domain_df = df[df['domain'] == domain_name]

            if len(domain_df) <= min_domain_count:
                balanced_dfs.append(domain_df)
            else:
                # [도메인 우선] 다수 도메인 -> '라벨' 균형 샘플링
                balanced_domain_df = self._sample_uniformly(
                    domain_df, 
                    group_by_col=self.label_col, # 라벨 균형
                    target_count=min_domain_count
                )
                balanced_dfs.append(balanced_domain_df)

        balanced_df = pd.concat(balanced_dfs).reset_index(drop=True)
        # 분할 기준: 도메인
        return balanced_df, 'domain'

    # --- 밸런싱 전략 3: 교집합 (완벽 균형) ---
    def _split_by_intersection(self, df):
        # (도메인, 라벨) 교집합 그룹별 카운트
        group_counts = df.groupby(['domain', self.label_col]).size()
        
        if group_counts.empty:
            print("Error [Intersection]: No valid (domain, label) groups found.")
            return pd.DataFrame(columns=df.columns), self.label_col

        min_group_count = group_counts.min()
        min_group_name = group_counts.idxmin()
        
        print(f"Balancing Plan [Intersection]: Smallest group is {min_group_name} with {min_group_count} samples.")
        print(f"Downsampling ALL (domain, label) groups to {min_group_count} samples.")

        balanced_dfs = []
        # groupby().sample()은 그룹이 min_group_count보다 작으면 에러가 날 수 있으므로 apply 사용
        for (domain, label), group_df in df.groupby(['domain', self.label_col]):
            if len(group_df) >= min_group_count:
                balanced_dfs.append(group_df.sample(n=min_group_count, random_state=self.seed))
            else:
                # (이론상 min_group_count가 최소값이므로 이 경우는 없음)
                print(f"Warning [Intersection]: Group ({domain}, {label}) has {len(group_df)} samples, skipping.")

        if not balanced_dfs:
            print("Error [Intersection]: No data left after sampling.")
            return pd.DataFrame(columns=df.columns), self.label_col

        balanced_df = pd.concat(balanced_dfs).reset_index(drop=True)
        # 분할 기준: 라벨 (도메인도 가능)
        return balanced_df, self.label_col

    # --- 메인 실행 로직 ---
    def save(self, train_df, val_df, test_df):
        os.makedirs(self.output, exist_ok=True)
        save_csv(train_df, os.path.join(self.output, "train.csv"))
        save_csv(val_df, os.path.join(self.output, "val.csv"))
        save_csv(test_df, os.path.join(self.output, "test.csv"))
        print(f"\n✅ Split complete! Files saved in {self.output}")

    def run(self, report=True, stats_only=False):
        print("Loading datasets...", flush=True)

        # 1. 데이터 로드
        df = load_datasets(self.data_path, self.class_list, self.load_map)
        
        if df.empty:
            print(f"Error: No data loaded. If you input it as cli check --data path and --classes {self.class_list}")
            return
            
        # 2. 원본 데이터 통계 리포트
        print("\n" + "="*40)
        print("📊 Raw Data Stats (Before Balancing)")
        print("="*40)
        print(f"Total files found: {len(df)}")
        print(f"\nClass counts (raw):\n{df[self.label_col].value_counts()}")
        print(f"\nDomain counts (raw):\n{df['domain'].value_counts()}")
        print(f"\nCounts per (Domain, Label):\n{df.groupby('domain')[self.label_col].value_counts()}")
        print("="*40)

        label_dic = df[self.label_col].value_counts().to_dict()
        keys_less_than_10 = [key for key, value in label_dic.items() if value < 10]

        # 3. stats-only 모드면 여기서 중지 (밸런싱 계획 출력 전)
        if stats_only:
            print(f"\n--stats-only mode enabled with --balance-mode='{self.balance_mode}'.")
            print("Stopping before balancing, splitting, or saving.")
            print("="*40)
            return
        
        # 각 class 개수가 10개 미만이면 중지 및 에러메세지 출력 
        if keys_less_than_10:
            print("Error: Please check your data. There are fewer than 10 data points in your data.")
            print(f"Please keep at least 10 data points per class. Missing data: {", ".join(keys_less_than_10)}")
            return

        # 4. 선택된 밸런싱 모드 실행
        print(f"\nRunning with --balance-mode = '{self.balance_mode}'")
        
        balanced_df = None
        stratify_col = None # 분할 기준 (label 또는 domain)

        if self.balance_mode == 'label':
            balanced_df, stratify_col = self._split_by_label_priority(df)
        elif self.balance_mode == 'domain':
            balanced_df, stratify_col = self._split_by_domain_priority(df)
        elif self.balance_mode == 'intersection':
            balanced_df, stratify_col = self._split_by_intersection(df)
        
        if balanced_df is None or balanced_df.empty:
            print("Error: No data left after balancing. Cannot proceed.")
            return

        print(f"\nTotal balanced dataset size: {len(balanced_df)}")
        print(f"Final balanced class counts:\n{balanced_df[self.label_col].value_counts()}")
        print(f"Final balanced domain counts:\n{balanced_df['domain'].value_counts()}")

        # 5. 최종 분할 (Stratified)
        print(f"\nSplitting data (Stratify by '{stratify_col}')...", flush=True)
        train_ratio, val_ratio, test_ratio = self.ratio / self.ratio.sum()

        from sklearn.model_selection import train_test_split
        
        try:
            train_df, temp_df = train_test_split(
                balanced_df,
                test_size=(1 - train_ratio),
                stratify=balanced_df[stratify_col],
                random_state=self.seed
            )

            relative_val_ratio = val_ratio / (val_ratio + test_ratio)
            
            val_df, test_df = train_test_split(
                temp_df,
                test_size=(1 - relative_val_ratio),
                stratify=temp_df[stratify_col],
                random_state=self.seed
            )
        except ValueError as e:
            print("\n" + "="*50)
            print("CRITICAL ERROR during train_test_split:")
            print(f"'{e}'")
            print("\nThis usually means your smallest group count is too low for the ratio.")
            print("Check the 'Raw Data Stats' and README 'Troubleshooting' section.")
            print("="*50)
            return

        # 6. 저장 및 리포트
        self.save(train_df, val_df, test_df)
        
        if report:
            print_ratio_report(
                train_df, val_df, test_df, 
                label_col=self.label_col, 
                label_map=self.label_map
            )