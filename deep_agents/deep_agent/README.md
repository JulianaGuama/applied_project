# Deep Data Analyst Agent (Starter Kit)

This folder contains a **production-ready starter structure** for a Deep Agent focused on:

1. Exploring customer data.
2. Analyzing column relationships.
3. Detecting potential business problems.
4. Estimating impact.
5. Recommending solutions based on your company product catalog.
6. Validating if findings are relevant according to business rules (the role you perform today).

## Architecture

The workflow is orchestrated by `DeepAnalysisOrchestrator` and uses five specialist agents:

- `DataExplorerAgent`: profile, quality checks, and correlation analysis.
- `IssueDetectionAgent`: converts statistical findings into business issues.
- `ImpactAssessmentAgent`: estimates impact (financial and operational).
- `SolutionRecommenderAgent`: maps issues to products/solutions in your catalog.
- `BusinessValidatorAgent`: checks if findings are relevant and compliant with business rules.

## Why this structure

- Keeps business logic outside code using YAML (`config/business_rules.yaml`).
- Uses fake data (`data/fake_customer_data.yaml`) so you can replace safely.
- Uses LangChain with Azure OpenAI through APIM (`src/deep_agent/llm_factory.py`).
- Supports deterministic + LLM-assisted analysis.

## Setup

Install additional dependencies:

```bash
pip install -r deep_agent/requirements.txt
```

Set environment variables:

```bash
export AZURE_OPENAI_ENDPOINT="https://<your-apim-domain>/openai"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
export AZURE_OPENAI_API_KEY="<api-key-if-needed>"
export AZURE_APIM_SUBSCRIPTION_KEY="<apim-subscription-key>"
```

## Run the demo

```bash
python deep_agent/examples/run_fake_analysis.py
```

The script generates a final Markdown report under:

- `deep_agent/examples/fake_analysis_report.md`

## Replace fake data with real data

1. Keep YAML schema consistent with `data/fake_customer_data.yaml`.
2. Replace records with real customer records.
3. Update `config/business_rules.yaml` thresholds and rule text.
4. Update `config/product_catalog.yaml` with your official offerings.
5. (Optional) tighten prompts under `prompts/`.

## Notes

- All code comments, prompts, YAML comments, and docstrings are in English as requested.
- If Azure/APIM credentials are missing, the pipeline still runs deterministic stages and marks LLM outputs as fallback.
