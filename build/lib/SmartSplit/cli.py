# smart_split/cli.py

import argparse
from .core import SmartSplitter

def parse_label_map(label_str):
    """ "dog:0,cat:1" 형식의 문자열을 {'dog': 0, 'cat': 1} 딕셔너리로 변환 """
    label_map = {}
    try:
        pairs = label_str.split(',')
        for pair in pairs:
            key, value = pair.split(':')
            label_map[key.strip()] = int(value.strip())
        return label_map
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid label format. Must be 'key1:val1,key2:val2'. Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="SmartSplit - Multi-domain, Multi-class dataset splitter",
        formatter_class=argparse.RawTextHelpFormatter # 도움말 줄바꿈
    )
    
    # --- 기본 인자 ---
    parser.add_argument("--data", required=True, help="Path to the dataset directory")
    parser.add_argument(
        "--classes", 
        required=True, 
        nargs='+',
        help="List of class names to find (e.g., dog cat bird)."
    )
    parser.add_argument(
        "--ratio", 
        nargs=3, 
        type=int, 
        default=[8,1,1], 
        help="Train/Val/Test ratio (default: 8 1 1)"
    )
    
    # --- 밸런싱 모드 (핵심) ---
    parser.add_argument(
        "--balance-mode",
        choices=['label', 'domain', 'intersection'],
        default='label',
        help="""Balancing strategy (default: 'label'):
'label':        [Label priority]
                Guarantees a 1:1:1... ratio for all labels.
                (Domain ratios may be broken.)
'domain':       [Domain priority]
                Guarantees a 1:1:1... ratio for all domains.
                (Label ratios may be broken.)
'intersection': [Intersection (perfect balance)]
                Matches all domains to the minimum number of samples in the (domain x label) intersection.
                (Data loss may be significant or certain labels may be excluded.)
"""
    )

    # --- 선택적 인자 ---
    parser.add_argument(
        "--label-map",
        type=parse_label_map,
        default=None,
        help="[Optional] Map class names to integers. Example: 'dog:0,cat:1,bird:2'"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", default="./output", help="Output directory")
    
    # --- 헬퍼/리포트 ---
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="[Helper] Run in 'dry-run' mode. Scans, counts, and reports the balancing plan without splitting or saving."
    )
    parser.add_argument("--no-report", action="store_true", help="Disable final ratio report output")
    
    args = parser.parse_args()

    splitter = SmartSplitter(
        data_path=args.data,
        class_list=args.classes,
        label_map=args.label_map,
        balance_mode=args.balance_mode, # 모드 전달
        label_col='label',
        ratio=tuple(args.ratio),
        seed=args.seed,
        output=args.output,
    )
    
    splitter.run(
        report=not args.no_report,
        stats_only=args.stats_only
    )

if __name__ == "__main__":
    main()