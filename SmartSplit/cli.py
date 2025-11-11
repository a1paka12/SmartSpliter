import argparse
from .core import SmartSplitter

def main():
    parser = argparse.ArgumentParser(description="SmartSplit - Multi-domain dataset splitter")
    parser.add_argument("--data", required=True)
    parser.add_argument("--label", default="label")
    parser.add_argument("--ratio", nargs=3, type=int, default=[8,1,1])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="./output")
    parser.add_argument("--no-report", action="store_true", help="Disable ratio report output")
    args = parser.parse_args()

    splitter = SmartSplitter(
        data_path=args.data,
        label_col=args.label,
        ratio=tuple(args.ratio),
        seed=args.seed,
        output=args.output,
    )
    splitter.run(report=not args.no_report)

if __name__ == "__main__":
    main()
