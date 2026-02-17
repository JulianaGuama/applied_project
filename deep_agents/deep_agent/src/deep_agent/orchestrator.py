"""Main orchestration entrypoint for the Deep Data Analysis workflow."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .agents import (
    BusinessValidatorAgent,
    DataExplorerAgent,
    ExecutiveSummaryAgent,
    ImpactAssessmentAgent,
    IssueDetectionAgent,
    SolutionRecommenderAgent,
)
from .io import load_dataset, load_yaml_file
from .llm_factory import build_azure_apim_chat_model
from .models import AnalysisReport


class DeepAnalysisOrchestrator:
    """Coordinates end-to-end execution across specialist agents."""

    def __init__(self, base_dir: str | Path):
        """Initialize orchestrator with project-relative config locations."""

        self.base_dir = Path(base_dir)
        self.dataset_path = self.base_dir / "data" / "fake_customer_data.yaml"
        self.rules_path = self.base_dir / "config" / "business_rules.yaml"
        self.catalog_path = self.base_dir / "config" / "product_catalog.yaml"

        self.data_explorer = DataExplorerAgent()
        self.issue_detector = IssueDetectionAgent()
        self.impact_assessor = ImpactAssessmentAgent()
        self.solution_recommender = SolutionRecommenderAgent()
        self.business_validator = BusinessValidatorAgent()
        self.summary_agent = ExecutiveSummaryAgent()

    def run(self) -> AnalysisReport:
        """Execute the full workflow and return a structured analysis report."""

        dataset = load_dataset(self.dataset_path)
        rules = load_yaml_file(self.rules_path)
        catalog = load_yaml_file(self.catalog_path)
        llm = build_azure_apim_chat_model(temperature=0.1)

        df = pd.DataFrame(dataset.records)
        analysis_rules = rules["analysis_rules"]
        validation_rules = rules["business_validation"]

        exploration = self.data_explorer.run(
            df, analysis_rules["meaningful_correlation_threshold"]
        )
        issues = self.issue_detector.run(df, analysis_rules)
        impact = self.impact_assessor.run(df, issues)
        recommendations = self.solution_recommender.run(issues, catalog)
        validation = self.business_validator.run(
            issues=issues,
            impact=impact,
            validation_rules=validation_rules,
            llm=llm,
        )

        payload = {
            "exploration": exploration.model_dump(),
            "issues": [item.model_dump() for item in issues],
            "impact": impact.model_dump(),
            "recommendations": [item.model_dump() for item in recommendations],
            "validation": validation.model_dump(),
        }
        llm_summary = self.summary_agent.run(payload=payload, llm=llm)

        return AnalysisReport(
            exploration=exploration,
            issues=issues,
            impact=impact,
            recommendations=recommendations,
            validation=validation,
            llm_summary=llm_summary,
        )
