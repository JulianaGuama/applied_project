# agents_chain

Projeto de exemplo para análise de qualidade de diálogos B2B com **LangChain + OpenAI + Python**.

## O que este projeto faz

1. Lê datasets locais em formato CSV/TSV (`\t`).
2. Analisa website da brand (HTML) para inferir contexto de atuação e objetivos de experiência.
3. Avalia se há problema com base em métricas e limiares definidos em arquivo.
4. Se **não** houver problema: retorna `sem ação mapeada`.
5. Se houver problema:
   - identifica causa raiz;
   - mede impacto (% de clientes afetados + relação com o setor);
   - recomenda melhorias com base no catálogo de serviços e serviços já contratados.

## Estrutura

- `main.py`: **somente orquestração da execução**.
- `src/agents_chain/pipeline.py`: fluxo da pipeline.
- `src/agents_chain/problem_evaluator.py`: regra de decisão de problema com limiares.
- `src/agents_chain/website_context.py`: agente de contexto do website.
- `src/agents_chain/analysis_agents.py`: agentes de causa raiz, impacto e recomendação.
- `config/problem_definition.yaml`: definição do que é problema.
- `data/*.tsv`: datasets de exemplo.

## Datasets de exemplo

- `data/brand_dialogs.tsv`
  - métricas por brand + trecho de diálogo.
- `data/brand_context.tsv`
  - expectativa de experiência da brand + serviços contratados.
- `data/services_catalog.tsv`
  - catálogo de serviços/features disponíveis.

## Como rodar

### 1) Criar ambiente e instalar dependências

```bash
cd agents_chain
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2) Configurar chave OpenAI

```bash
export OPENAI_API_KEY="sua_chave"
```

### 3) Executar

```bash
python main.py
```

Saída: JSON com status por brand, causa raiz, impacto e recomendações quando aplicável.

## Execução com caminhos customizados

```bash
python main.py \
  --dialogs data/brand_dialogs.tsv \
  --services data/services_catalog.tsv \
  --brand-context data/brand_context.tsv \
  --definition config/problem_definition.yaml
```
