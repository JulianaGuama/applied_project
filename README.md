# applied_project

Este repositório agora está organizado como um **multi-projeto**:

- `deep_agents/`: projeto original, preservado com a estrutura antiga.
- `agents_chain/`: novo projeto com pipeline de agentes para análise de qualidade de diálogos entre customers e brands.

## Projetos

### 1) deep_agents
Projeto legado movido integralmente para esta pasta.

### 2) agents_chain
Projeto novo em Python + LangChain + OpenAI para:
- ler dataset em CSV com separador `\t`;
- avaliar se há problema com base em métricas e limiares;
- quando houver problema, identificar causa raiz;
- medir impacto de negócio;
- recomendar melhorias com base no catálogo de serviços.

Consulte `agents_chain/README.md` para instruções completas.
