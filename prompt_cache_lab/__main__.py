from argparse import ArgumentParser
from pathlib import Path
import json

from .analysis import group_latency, warmup_curve
from .io import read_rows, read_specs
from .planner import expand
from .runner import execute_ollama, write_jsonl


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("config")

    exe = sub.add_parser("execute")
    exe.add_argument("plan")
    exe.add_argument("--model", required=True)
    exe.add_argument("--out", required=True)
    exe.add_argument("--endpoint", default="http://127.0.0.1:11434")

    report = sub.add_parser("report")
    report.add_argument("path")
    report.add_argument("--curve", action="store_true")

    args = parser.parse_args()

    if args.cmd == "plan":
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        for spec in expand(config):
            print(json.dumps(spec.to_dict(), sort_keys=True))
    elif args.cmd == "execute":
        rows = [execute_ollama(x, args.model, args.endpoint) for x in read_specs(args.plan)]
        write_jsonl(args.out, rows)
        print(json.dumps({"completed": len(rows)}))
    else:
        rows = read_rows(args.path)
        data = warmup_curve(rows) if args.curve else group_latency(rows)
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
