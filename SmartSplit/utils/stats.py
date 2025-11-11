# smart_split/utils/stats.py

def print_ratio_report(train, val, test, label_col, label_map=None):
    
    # {0: 'dog', 1: 'cat'} (label_map이 제공된 경우)
    reverse_map = {v: k for k, v in label_map.items()} if label_map else None

    def ratio(df):
        dist = df[label_col].value_counts(normalize=True).mul(100).round(2).to_dict()
        if reverse_map:
            # {0: 50.0} -> {'dog': 50.0%}
            return {reverse_map.get(k, k): f"{v}%" for k, v in dist.items()}
        else:
            # {'dog': 50.0} -> {'dog': 50.0%}
            return {k: f"{v}%" for k, v in dist.items()}


    def domain_ratio(df):
        dist = df['domain'].value_counts(normalize=True).mul(100).round(2).to_dict()
        return {k: f"{v}%" for k, v in dist.items()}

    print("\n" + "="*40)
    print("📊 Final Split Ratio Report")
    print("="*40)
    print(f"Total: {len(train) + len(val) + len(test)} (Train: {len(train)}, Val: {len(val)}, Test: {len(test)})")
    
    print("\n--- Train Set ---")
    print("Labels :", ratio(train))
    print("Domains:", domain_ratio(train))
    
    print("\n--- Validation Set ---")
    print("Labels :", ratio(val))
    print("Domains:", domain_ratio(val))

    print("\n--- Test Set ---")
    print("Labels :", ratio(test))
    print("Domains:", domain_ratio(test))
    print("="*40)