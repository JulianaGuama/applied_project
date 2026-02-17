from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class WebsiteContextAgent:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Você analisa websites B2B para inferir objetivos de experiência com customers."
                    "Sempre conecte com redução de custo, aumento de receita e fidelização.",
                ),
                (
                    "human",
                    "Brand: {brand_name}\n"
                    "Setor informado: {industry}\n"
                    "HTML (resumo):\n{html_snippet}\n\n"
                    "Retorne em 3 linhas: (1) área de atuação inferida, (2) objetivos de experiência,"
                    " (3) riscos se a experiência falhar.",
                ),
            ]
        )

    def fetch_html(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join(soup.get_text(separator=" ").split())
            return text[:2500]
        except Exception:
            return "Website indisponível; usar somente contexto do setor informado."

    def analyze(self, brand_name: str, industry: str, website_url: str) -> str:
        html_snippet = self.fetch_html(website_url)
        chain = self.prompt | self.llm
        result = chain.invoke(
            {
                "brand_name": brand_name,
                "industry": industry,
                "html_snippet": html_snippet,
            }
        )
        return result.content
