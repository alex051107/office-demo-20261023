"""Run the paired task's offline checks against this saved trajectory report."""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=Path)
    arguments = parser.parse_args()
    task = arguments.task or root.parents[1] / 'ZCloud-电力监管-001-20261020/powercor-2020-capex-reconciliation'
    entry = task / 'validation/run_regression.py'
    if not entry.is_file():
        parser.error('Place the paired task package beside this report, or supply --task.')
    subprocess.run([sys.executable, '-B', str(entry), '--trajectory', str(root)], check=True)


if __name__ == '__main__':
    main()
