# Base de Conhecimento

## Dados Utilizados

Para este protótipo, utilizei **exclusivamente** os dados mockados fornecidos pela DIO, aplicando uma camada de **Engenharia de Features** em Python para extrair o máximo valor deles. A decisão de não usar datasets externos (Hugging Face) foi estratégica: quero demonstrar que com poucos dados, mas bem interpretados, uma LLM local (Ollama) pode gerar insights extremamente precisos e personalizados.

| Arquivo | Formato | Utilização no Agente (Visão Geral) | Features Derivadas (Pré-processamento) |
|---|---|---|---|
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente | **Taxa de Queima da Meta:** Calcula quanto falta para a meta vs. o prazo. <br><br> **Índice de Gastos Discricionários:** Soma de Lazer + Alimentação fora + Transporte por App. |
| `perfil_investidor.json` | JSON | Personalizar recomendações e metas | **Gap Financeiro:** `patrimonio_total` vs `valor_necessario` da meta 1. <br><br> **Perfil Comportamental:** Cruzamento do `objetivo_principal` com a realidade do CSV. |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil | **Matching Lógico:** Filtro de produtos baseado no `perfil_investidor` ("moderado") e `risco` ("baixo"/"medio"). |
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores | **Memória de Curto Prazo:** Extração da coluna `Tema` para evitar que a IA repita explicações já dadas (ex: se o cliente já perguntou sobre "Tesouro Selic", a IA não explica o básico novamente). |

---

## Adaptações nos Dados

**Não modifiquei os arquivos originais.** Em vez disso, criei um módulo Python (`src/data_enricher.py`) que lê os arquivos brutos e gera um **Dicionário de Contexto Inteligente** em tempo de execução.

**Expansões Lógicas Realizadas pelo Código:**
1.  **Cálculo da Meta Mensal:** Com base no JSON `metas[0]`, calculamos que João precisa economizar **R$ 625,00/mês** para bater a Reserva de Emergência até Jun/2026.
2.  **Análise do Mês Atual:** O CSV de Outubro mostra uma sobra de **R$ 2.511,10**. O código identifica que isso é 4x maior que o necessário. Isso vira um *insight positivo* no prompt.
3.  **Categorização de Risco:** Identificamos que `Restaurante` (R$120) + `Uber` (R$45) + `Netflix` (R$55,90) somam **R$ 220,90** de gastos que podem ser "micro-otimizados" sem impactar a estrutura fixa da casa (Aluguel, Luz).

---

## Estratégia de Integração

### Como os dados são carregados?
Os dados são carregados de forma síncrona no início da sessão do **Streamlit** utilizando `@st.cache_data`. Isso garante que o processamento pesado de leitura de arquivo aconteça apenas uma vez.

1.  `pandas.read_csv()` carrega as transações.
2.  `json.load()` carrega o perfil e produtos.
3.  **Pré-Processamento:** Uma função `generate_behavioral_context()` é chamada imediatamente, cruzando os dados e retornando um objeto `contexto` que fica armazenado em memória (`st.session_state`).

### Como os dados são usados no prompt?
Os dados **NÃO** são enviados crus para a LLM (o que poluiria o contexto e causaria alucinação). Eles são usados de duas formas:

1.  **System Prompt Estático (Regras):** Contém as instruções de segurança e persona.
2.  **Contexto Dinâmico RAG (Injetado a cada pergunta):** Antes de enviar a pergunta do usuário para o Ollama, o código Python insere um bloco de texto estruturado com os resultados do pré-processamento.

### Exemplo de Contexto Montado (Injetado no Prompt)

Quando o usuário pergunta *"Nina, como estou indo?"*, o prompt enviado ao Ollama contém este bloco formatado antes da pergunta:

```text
[BLOCO DE CONTEXTO - DADOS ESTRITAMENTE CONFIDENCIAIS E CALCULADOS AGORA]

DADOS DO CLIENTE (Fonte: perfil_investidor.json):
- Nome: João Silva
- Perfil: Moderado
- Objetivo Atual: Completar Reserva de Emergência (Faltam R$ 5.000,00)

ANÁLISE COMPORTAMENTAL DE OUTUBRO (Fonte: transacoes.csv e cálculos Python):
- Receita Total: R$ 5.000,00
- Gastos Totais: R$ 2.488,90
- **Sobra do Mês: R$ 2.511,10**
- **Gastos Flexíveis (Otimizáveis): R$ 220,90** (Detalhe: Restaurante R$120, Uber R$45, Netflix R$55,90)

HISTÓRICO DE CONHECIMENTO (Fonte: historico_atendimento.csv):
- O cliente JÁ perguntou sobre: Tesouro Selic, Metas financeiras.

PRODUTOS DISPONÍVEIS PARA O PERFIL MODERADO (Fonte: produtos_financeiros.json):
- Tesouro Selic (Risco Baixo)
- CDB Liquidez Diária (Risco Baixo)
- LCI/LCA (Risco Baixo, Isento IR)
- Fundo Multimercado (Risco Medio)

[FIM DO BLOCO DE CONTEXTO]

PERGUNTA DO USUÁRIO: "Nina, como estou indo?"
