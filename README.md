# 🧠 Nina | Agente de Micro-Otimização Financeira com IA Generativa

![Badge](https://img.shields.io/badge/Status-Desafio%20DIO%20Concluído-green)
![Badge](https://img.shields.io/badge/LLM-Ollama%20(Local)-blue)
![Badge](https://img.shields.io/badge/Framework-Streamlit-red)
![Badge](https://img.shields.io/badge/Parceria-Bradesco%20%7C%20DIO-orange)

## 📌 Contexto

Os assistentes virtuais no setor financeiro estão evoluindo de simples chatbots reativos para **agentes inteligentes e proativos**. Neste desafio, desenvolvemos a **Nina**, um agente que utiliza IA Generativa para resolver a **Dissonância Comportamental Financeira** — a lacuna entre o que o cliente planeja e o que realmente gasta.

A Nina atua como uma **Coach de Micro-Otimização de Hábitos**, focada em:
- **Antecipar padrões** de comportamento nos dados de transações
- **Personalizar sugestões** com base no perfil do investidor
- **Cocriar micro-estratégias** de economia sustentável (ex: "Desafio dos 15%")
- **Garantir segurança** absoluta via RAG Estrito e citação obrigatória de fontes

> 💡 **Diferencial:** 100% local com **Ollama** + **Streamlit**. Custo zero, privacidade total.

---

## 📋 O Que Entregamos

### 1. Documentação do Agente

Defini a persona, o tom de voz e a arquitetura de segurança da Nina.

- **Caso de Uso:** Micro-Otimização de Hábitos para acelerar metas de médio prazo (ex: Reserva de Emergência).
- **Persona:** Nina (Navegadora de Intenções e Números Atípicos) — Analítica, acolhedora e educativa.
- **Segurança:** Sistema de `[Fonte: arquivo]` obrigatório e bloqueio de respostas sem embasamento nos dados mockados.

📄 **Documento:** [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md)

---

### 2. Base de Conhecimento

Utilizei e **enriqueci** os dados mockados da DIO com um motor de contexto Python.

| Arquivo | Utilização Estratégica |
|---------|------------------------|
| `transacoes.csv` | Cálculo da **Sobra Mensal** e **Índice de Gastos Discricionários** |
| `perfil_investidor.json` | Extração do **Gap Financeiro** e **Taxa de Queima da Meta** |
| `produtos_financeiros.json` | Matching de produtos com o perfil **Moderado** |
| `historico_atendimento.csv` | **Memória de Curto Prazo** para evitar repetições |

📄 **Documento:** [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md)

---

### 3. Prompts do Agente

O coração da Nina. Desenvolvi um System Prompt rigoroso para garantir respostas úteis e seguras.

- **System Prompt:** Define regras de anti-alucinação, tom de voz e estrutura de resposta (Few-Shot implícito).
- **Exemplos de Interação:** Cenários reais com João Silva, mostrando a sugestão do "Desafio dos 15%".
- **Edge Cases:** Tratamento para perguntas sobre clima, senhas e "como ficar rico rápido".

📄 **Documento:** [`docs/03-prompts.md`](./docs/03-prompts.md)

---

### 4. Aplicação Funcional

Protótipo interativo desenvolvido com **Streamlit** e **Ollama** (Modelo `llama3.1:8b` ou `mistral`).

- **Interface:** Layout de duas colunas (Chat proativo + Painel de Métricas).
- **Backend:** `pandas` para processamento de CSV/JSON e `langchain` para orquestração do prompt.
- **Execução:** Roda 100% offline na máquina local.

📁 **Código Fonte:** [`src/app.py`](./src/app.py)

---

### 5. Avaliação e Métricas

Validei a qualidade do agente com uma matriz focada em **Assertividade Contextual**, **Segurança (Anti-Alucinação)** e **Coerência Comportamental**.

- **Teste 1:** Cálculo correto da meta mensal (R$ 625,00).
- **Teste 2:** Sugestão de produtos de Baixo Risco para o perfil Moderado.
- **Teste 3:** Fallback seguro para perguntas fora do escopo ("Cotação do Dólar").

📄 **Documento:** [`docs/04-metricas.md`](./docs/04-metricas.md)

---

### 6. Pitch

Roteiro de 3 minutos focado em:
1.  **Problema:** A ansiedade de não ver o progresso financeiro.
2.  **Solução:** Nina cruzando intenção vs. realidade.
3.  **Inovação:** IA local que sugere micro-ajustes, não cortes radicais.

📄 **Documento:** [`docs/05-pitch.md`](./docs/05-pitch.md)

---

## 🛠️ Ferramentas Utilizadas

| Categoria | Ferramenta | Justificativa no Projeto |
|-----------|------------|--------------------------|
| **LLM** | Ollama (`llama3.1:8b`) | Execução local, sem custo de API e garantia de privacidade dos dados mockados. |
| **Desenvolvimento** | Streamlit | Prototipagem rápida e visualização limpa das métricas comportamentais. |
| **Orquestração** | LangChain | Gerenciamento eficiente do Prompt Template com injeção dinâmica de contexto. |
| **Dados** | Pandas | Leitura e cálculo de métricas derivadas (Taxa de Queima) em memória. |

---

## 📁 Estrutura do Repositório

```
📁 dio-lab-bia-do-futuro/
│
├── 📄 README.md # Você está aqui
│
├── 📁 data/ # Dados mockados fornecidos pela DIO
│ ├── historico_atendimento.csv
│ ├── perfil_investidor.json
│ ├── produtos_financeiros.json
│ └── transacoes.csv
│
├── 📁 docs/ # Documentação completa do desafio
│ ├── 01-documentacao-agente.md
│ ├── 02-base-conhecimento.md
│ ├── 03-prompts.md
│ ├── 04-metricas.md
│ └── 05-pitch.md
│
├── 📁 src/ # Código executável da Nina
│ ├── app.py              # Aplicação principal com todas as funções integradas
│ ├── requirements.txt    # Dependências do projeto
│ └── README.md           # Instruções de execução
│
└── 📁 assets/ # Diagrama Mermaid e Logo da Nina
└── arquitetura.png
```
