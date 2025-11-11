def print_ratio_report(train, val, test, label_col):
    def ratio(df):
        return df[label_col].value_counts(normalize=True).to_dict()

    def domain_ratio(df):
        return df['domain'].value_counts(normalize=True).to_dict()

    print("\n📊 Dataset Ratio Report")
    print("Train:", ratio(train), " | Domains:", domain_ratio(train))
    print("Val  :", ratio(val),   " | Domains:", domain_ratio(val))
    print("Test :", ratio(test),  " | Domains:", domain_ratio(test))
    print(f"Train size: {len(train)}, Val: {len(val)}, Test: {len(test)}\n")
