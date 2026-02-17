from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class RootCauseAgent:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Você identifica causa raiz de problemas em atendimento B2B."),
                (
                    "human",
                    "Brand: {brand_name}\n"
                    "Brechas de KPI: {breaches}\n"
                    "Exemplo de diálogo: {dialogue_sample}\n"
                    "Contexto de experiência: {desired_experience}\n"
                    "Contexto de website: {website_context}\n\n"
                    "Descreva em até 4 bullets: causa raiz provável e sinais que suportam.",
                ),
            ]
        )

    def analyze(self, payload: dict) -> str:
        return (self.prompt | self.llm).invoke(payload).content


class ImpactAgent:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Você estima impacto de problemas em operações de suporte B2B."),
                (
                    "human",
                    "Setor: {industry}\n"
                    "% clientes impactados: {affected_pct:.2f}\n"
                    "Desejo de experiência da brand: {desired_experience}\n"
                    "Causa raiz: {root_cause}\n"
                    "Relacione impacto com custo, receita e fidelização em até 5 linhas.",
                ),
            ]
        )

    def analyze(self, payload: dict) -> str:
        return (self.prompt | self.llm).invoke(payload).content


class ImprovementAgent:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Você recomenda melhorias de experiência usando catálogo de serviços disponíveis.",
                ),
                (
                    "human",
                    "Brand: {brand_name}\n"
                    "Causa raiz: {root_cause}\n"
                    "Impacto: {impact_analysis}\n"
                    "Serviços contratados: {contracted_services}\n"
                    "Catálogo de serviços: {services_catalog}\n\n"
                    "Retorne uma lista priorizada com: ação, serviço recomendado, ganho esperado.",
                ),
            ]
        )

    def analyze(self, payload: dict) -> str:
        return (self.prompt | self.llm).invoke(payload).content
