"""Run targeted local header OCR on a preserved quarterly intake."""
import argparse
import json
from pathlib import Path
from modules.company_intelligence.quarterly_header_region import extract_header_regions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    print(json.dumps(extract_header_regions(args.run, workspace=Path(__file__).resolve().parents[1]), indent=2))


if __name__ == '__main__':
    main()
