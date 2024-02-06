import argparse
from codegen import header


def main(h: header.Header) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base_dir", type=str, help="The base directory for the generated files"
    )
    parser.add_argument(
        "--base", type=str, help="The file name for the base variant"
    )
    parser.add_argument(
        "--tu", type=str, help="The file name for the tu variant"
    )
    parser.add_argument(
        "--mu", type=str, help="The file name for the mu variant"
    )
    parser.add_argument(
        "--tumu", type=str, help="The file name for the tumu variant"
    )
    args = parser.parse_args()
    if args.base:
        h.write(["", "m"], args.base_dir, f"{args.base}")
    if args.tu:
        h.write(["tu", "tum"], args.base_dir, f"{args.tu}")
    if args.mu:
        h.write(["mu"], args.base_dir, f"{args.mu}")
    if args.tumu:
        h.write(["tumu"], args.base_dir, f"{args.tumu}")
