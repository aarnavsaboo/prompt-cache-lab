from argparse import ArgumentParser
import json
from .trials import make_trials


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    make = sub.add_parser("make")
    make.add_argument("--prefix-chars", type=int, default=8000)
    make.add_argument("--requests", type=int, default=10)
    make.add_argument("--mode", choices=["stable","mutated","alternating"], default="stable")
    args = parser.parse_args()
    for row in make_trials(args.prefix_chars, args.requests, args.mode):
        print(json.dumps(row.__dict__))


if __name__ == "__main__":
    main()
