"""Example script to run Deep Agent with fake data and export a markdown report."""

from __future__ import annotations

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from deep_agent.orchestrator import DeepAnalysisOrchestrator


def to_markdown(report) -> str:
    """Convert report object to Markdown for quick stakeholder review."""

    lines = [
        "# Deep Agent Analysis Report",
        "",
        "## Validation Status",
        f"- Approved: **{report.validation.approved}**",
        f"- Confidence: **{report.validation.confidence:.2f}**",
        "",
        "## Impact",
        f"- Total monthly revenue at risk: **USD {report.impact.total_monthly_revenue_at_risk_usd:,.2f}**",
        f"- Operational load index: **{report.impact.operational_load_index:.2f}**",
        "",
        "## Issues",
    ]

    for issue in report.issues:
        lines.append(
            f"- Customer `{issue.customer_id}` | `{issue.issue_type}` | severity `{issue.severity}` | evidence `{issue.evidence}`"
        )

    lines.extend(["", "## Recommendations"])
    for item in report.recommendations:
        lines.append(
            f"- Customer `{item.customer_id}` -> product `{item.product_id}` + solution `{item.solution_id}`. {item.rationale}"
        )

    lines.extend(["", "## Executive Summary", report.llm_summary])
    return "\n".join(lines)


def main() -> None:
    """Run workflow end-to-end and write markdown output."""

    orchestrator = DeepAnalysisOrchestrator(base_dir=BASE_DIR)
    report = orchestrator.run()

    output_path = Path(__file__).resolve().parent / "fake_analysis_report.md"
    output_path.write_text(to_markdown(report), encoding="utf-8")
    print(f"Report generated at: {output_path}")


if __name__ == "__main__":
    main()
