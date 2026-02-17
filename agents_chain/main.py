from __future__ import annotations

import argparse
import json

from src.agents_chain.pipeline import PipelineConfig, run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline de análise de qualidade de diálogos B2B")
    parser.add_argument("--dialogs", default="data/brand_dialogs.tsv")
    parser.add_argument("--services", default="data/services_catalog.tsv")
    parser.add_argument("--brand-context", default="data/brand_context.tsv")
    parser.add_argument("--definition", default="config/problem_definition.yaml")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = PipelineConfig(
        dialogs_path=args.dialogs,
        services_path=args.services,
        brand_context_path=args.brand_context,
        definition_path=args.definition,
    )
    results = run_pipeline(config)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
