from __future__ import annotations

from dataclasses import dataclass

from .analysis_agents import ImpactAgent, ImprovementAgent, RootCauseAgent
from .data_loader import load_problem_definition, load_tsv
from .problem_evaluator import ProblemEvaluator
from .website_context import WebsiteContextAgent


@dataclass
class PipelineConfig:
    dialogs_path: str
    services_path: str
    brand_context_path: str
    definition_path: str


def run_pipeline(config: PipelineConfig) -> list[dict]:
    dialogs_df = load_tsv(config.dialogs_path)
    services_df = load_tsv(config.services_path)
    context_df = load_tsv(config.brand_context_path)
    definition = load_problem_definition(config.definition_path)

    evaluator = ProblemEvaluator(definition)
    website_agent = WebsiteContextAgent()
    root_cause_agent = RootCauseAgent()
    impact_agent = ImpactAgent()
    improvement_agent = ImprovementAgent()

    services_catalog = services_df.to_dict(orient="records")
    context_by_brand = {row["brand_id"]: row for _, row in context_df.iterrows()}

    results: list[dict] = []

    for _, row in dialogs_df.iterrows():
        row_data = row.to_dict()
        brand_id = row_data["brand_id"]
        brand_ctx = context_by_brand.get(brand_id, {})
        desired_experience = brand_ctx.get("desired_experience", "não informado")
        contracted_services = brand_ctx.get("contracted_services", "nenhum")

        website_context = website_agent.analyze(
            brand_name=row_data["brand_name"],
            industry=row_data["industry"],
            website_url=row_data["website_url"],
        )

        evaluation = evaluator.evaluate(row_data)
        if not evaluation["has_problem"]:
            results.append(
                {
                    "brand_id": brand_id,
                    "brand_name": row_data["brand_name"],
                    "status": evaluation["message"],
                }
            )
            continue

        affected_pct = (float(row_data["affected_customers"]) / float(row_data["total_customers"])) * 100

        root_cause = root_cause_agent.analyze(
            {
                "brand_name": row_data["brand_name"],
                "breaches": ", ".join(evaluation["breaches"]),
                "dialogue_sample": row_data["dialogue_sample"],
                "desired_experience": desired_experience,
                "website_context": website_context,
            }
        )

        impact_analysis = impact_agent.analyze(
            {
                "industry": row_data["industry"],
                "affected_pct": affected_pct,
                "desired_experience": desired_experience,
                "root_cause": root_cause,
            }
        )

        recommendations = improvement_agent.analyze(
            {
                "brand_name": row_data["brand_name"],
                "root_cause": root_cause,
                "impact_analysis": impact_analysis,
                "contracted_services": contracted_services,
                "services_catalog": services_catalog,
            }
        )

        results.append(
            {
                "brand_id": brand_id,
                "brand_name": row_data["brand_name"],
                "status": "problema identificado",
                "breaches": evaluation["breaches"],
                "website_context": website_context,
                "root_cause": root_cause,
                "impact_analysis": impact_analysis,
                "recommendations": recommendations,
            }
        )

    return results
