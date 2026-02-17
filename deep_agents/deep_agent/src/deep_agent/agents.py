"""Specialist agents used by the Deep Analysis orchestrator."""

from __future__ import annotations

from typing import Any

import pandas as pd
from langchain.prompts import ChatPromptTemplate

from .models import (
    BusinessValidationResult,
    DataExplorationResult,
    DetectedIssue,
    ImpactAssessment,
    Recommendation,
)


class DataExplorerAgent:
    """Performs data profiling and correlation analysis."""

    def run(self, df: pd.DataFrame, meaningful_correlation_threshold: float) -> DataExplorationResult:
        """Run exploratory analysis and return normalized findings."""

        numeric_df = df.select_dtypes(include=["number"])
        numeric_summary = {
            column: {
                "mean": float(numeric_df[column].mean()),
                "std": float(numeric_df[column].std(ddof=0) if len(numeric_df) > 1 else 0.0),
                "min": float(numeric_df[column].min()),
                "max": float(numeric_df[column].max()),
            }
            for column in numeric_df.columns
        }

        correlations = numeric_df.corr(numeric_only=True)
        meaningful_correlations: list[dict[str, Any]] = []
        seen_pairs: set[tuple[str, str]] = set()

        for a in correlations.columns:
            for b in correlations.columns:
                if a == b or (b, a) in seen_pairs:
                    continue
                seen_pairs.add((a, b))
                coefficient = float(correlations.loc[a, b])
                if abs(coefficient) >= meaningful_correlation_threshold:
                    meaningful_correlations.append(
                        {
                            "column_a": a,
                            "column_b": b,
                            "coefficient": round(coefficient, 4),
                        }
                    )

        return DataExplorationResult(
            row_count=len(df),
            columns=list(df.columns),
            null_ratio_by_column={
                column: float(df[column].isna().mean()) for column in df.columns
            },
            numeric_summary=numeric_summary,
            meaningful_correlations=meaningful_correlations,
        )


class IssueDetectionAgent:
    """Detects issues per customer using enterprise business thresholds."""

    def run(self, df: pd.DataFrame, analysis_rules: dict[str, Any]) -> list[DetectedIssue]:
        """Apply business thresholds to identify problems for each customer."""

        issues: list[DetectedIssue] = []

        for _, row in df.iterrows():
            customer_id = str(row["customer_id"])

            if row["churn_risk_score"] >= analysis_rules["churn_risk_high_threshold"]:
                issues.append(
                    DetectedIssue(
                        customer_id=customer_id,
                        issue_type="high_churn_risk",
                        severity="high",
                        evidence={"churn_risk_score": float(row["churn_risk_score"])},
                    )
                )

            if row["support_tickets_last_30d"] >= analysis_rules["support_tickets_high_threshold"]:
                issues.append(
                    DetectedIssue(
                        customer_id=customer_id,
                        issue_type="support_overload",
                        severity="medium",
                        evidence={
                            "support_tickets_last_30d": int(row["support_tickets_last_30d"])
                        },
                    )
                )

            if row["avg_payment_delay_days"] >= analysis_rules["payment_delay_high_threshold"]:
                issues.append(
                    DetectedIssue(
                        customer_id=customer_id,
                        issue_type="payment_delay_risk",
                        severity="medium",
                        evidence={"avg_payment_delay_days": int(row["avg_payment_delay_days"])},
                    )
                )

            if row["product_adoption_score"] <= analysis_rules["product_adoption_low_threshold"]:
                issues.append(
                    DetectedIssue(
                        customer_id=customer_id,
                        issue_type="low_product_adoption",
                        severity="high",
                        evidence={"product_adoption_score": float(row["product_adoption_score"])},
                    )
                )

        return issues


class ImpactAssessmentAgent:
    """Estimates business and operational impact of detected issues."""

    ISSUE_MULTIPLIER = {
        "high_churn_risk": 0.50,
        "support_overload": 0.10,
        "payment_delay_risk": 0.15,
        "low_product_adoption": 0.20,
    }

    def run(self, df: pd.DataFrame, issues: list[DetectedIssue]) -> ImpactAssessment:
        """Estimate impact in dollars and operational index for current issue set."""

        revenue_lookup = {
            str(row["customer_id"]): float(row["monthly_revenue_usd"])
            for _, row in df.iterrows()
        }

        issue_impacts: list[dict[str, Any]] = []
        total_revenue_at_risk = 0.0
        operational_load_index = 0.0

        for issue in issues:
            base_revenue = revenue_lookup.get(issue.customer_id, 0.0)
            multiplier = self.ISSUE_MULTIPLIER.get(issue.issue_type, 0.05)
            estimated_impact = base_revenue * multiplier

            if issue.issue_type in {"support_overload", "payment_delay_risk"}:
                operational_load_index += 1.0

            total_revenue_at_risk += estimated_impact
            issue_impacts.append(
                {
                    "customer_id": issue.customer_id,
                    "issue_type": issue.issue_type,
                    "estimated_monthly_impact_usd": round(estimated_impact, 2),
                }
            )

        return ImpactAssessment(
            issue_impacts=issue_impacts,
            total_monthly_revenue_at_risk_usd=round(total_revenue_at_risk, 2),
            operational_load_index=round(operational_load_index, 2),
        )


class SolutionRecommenderAgent:
    """Maps issue types to product and solution catalog entries."""

    def run(self, issues: list[DetectedIssue], catalog: dict[str, Any]) -> list[Recommendation]:
        """Create recommendations for each issue based on catalog mapping."""

        products = catalog.get("products", [])
        solutions = catalog.get("solutions", [])

        product_by_issue: dict[str, dict[str, Any]] = {}
        for product in products:
            for issue_type in product.get("target_issues", []):
                product_by_issue[issue_type] = product

        solution_by_product: dict[str, dict[str, Any]] = {}
        for solution in solutions:
            for product_id in solution.get("supports_products", []):
                solution_by_product[product_id] = solution

        recommendations: list[Recommendation] = []

        for issue in issues:
            product = product_by_issue.get(issue.issue_type)
            if not product:
                continue
            solution = solution_by_product.get(product["id"])
            if not solution:
                continue

            recommendations.append(
                Recommendation(
                    customer_id=issue.customer_id,
                    issue_type=issue.issue_type,
                    product_id=product["id"],
                    solution_id=solution["id"],
                    rationale=(
                        f"Issue '{issue.issue_type}' maps to product '{product['name']}' "
                        f"and solution '{solution['name']}'."
                    ),
                )
            )

        return recommendations


class BusinessValidatorAgent:
    """Validates relevance of findings using governance rules and optional LLM review."""

    def run(
        self,
        issues: list[DetectedIssue],
        impact: ImpactAssessment,
        validation_rules: dict[str, Any],
        llm,
    ) -> BusinessValidationResult:
        """Validate whether analysis findings should be accepted."""

        rejected_reasons: list[str] = []
        governance_notes: list[str] = []

        if not issues:
            rejected_reasons.append("No issues detected. Nothing to prioritize.")

        if (
            validation_rules.get("require_measurable_impact", True)
            and impact.total_monthly_revenue_at_risk_usd <= 0
        ):
            rejected_reasons.append("No measurable financial impact found.")

        confidence = 0.8 if issues else 0.2
        approved = len(rejected_reasons) == 0

        if llm:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are a strict business governance validator. "
                        "Return a concise review in plain English.",
                    ),
                    (
                        "human",
                        "Validation rules: {rules}\n"
                        "Issues: {issues}\n"
                        "Impact: {impact}\n"
                        "Provide governance notes.",
                    ),
                ]
            )
            chain = prompt | llm
            response = chain.invoke(
                {
                    "rules": validation_rules,
                    "issues": [item.model_dump() for item in issues],
                    "impact": impact.model_dump(),
                }
            )
            governance_notes.append(str(response.content))
        else:
            governance_notes.append(
                "LLM validation skipped because Azure/APIM credentials are not configured."
            )

        if approved and confidence < validation_rules.get("relevance_confidence_min", 0.7):
            rejected_reasons.append("Confidence below minimum relevance threshold.")
            approved = False

        return BusinessValidationResult(
            approved=approved,
            confidence=confidence,
            rejected_reasons=rejected_reasons,
            governance_notes=governance_notes,
        )


class ExecutiveSummaryAgent:
    """Creates a concise final summary, optionally enriched by LLM."""

    def run(self, payload: dict[str, Any], llm) -> str:
        """Build executive summary from the final analysis payload."""

        if not llm:
            return (
                "Fallback summary: analysis completed with deterministic logic; "
                "configure Azure/APIM credentials to enable narrative synthesis."
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an analytics consultant writing concise executive summaries.",
                ),
                (
                    "human",
                    "Summarize the analysis output with top issues, impact and recommendations. "
                    "Output in up to 8 bullet points. Payload: {payload}",
                ),
            ]
        )

        chain = prompt | llm
        response = chain.invoke({"payload": payload})
        return str(response.content)
