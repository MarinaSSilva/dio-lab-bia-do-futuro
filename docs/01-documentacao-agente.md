# Documentação do Agente: Nina (Navegadora de Intenções e Números Atípicos)

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

O agente **Nina** resolve o problema da **Dissonância Comportamental Financeira** — a lacuna silenciosa que existe entre a **intenção declarada** do cliente (documentada no perfil de investidor) e o seu **comportamento transacional real** (registrado no extrato mensal).

Usuários como João Silva (Analista de Sistemas, 32 anos) frequentemente manifestam o desejo de "guardar dinheiro para uma reserva de emergência", mas o cérebro humano é péssimo em correlacionar o gasto de R$ 120,00 em um restaurante na sexta-feira com o atraso de 3 meses na meta de comprar um apartamento.

O problema não é falta de dinheiro (João teve uma sobra de R$ 2.511,10 em Outubro), mas sim a **falta de visibilidade proativa** sobre as micro-decisões diárias que drenam o potencial de acumulação de capital.

### Solução
> Como o agente resolve esse problema de forma proativa?

Nina atua como um **Coach de Micro-Otimalização de Hábitos**, não como um robô de investimentos tradicional. Ela utiliza IA Generativa (Ollama) para cruzar dados estruturados (CSV/JSON) e gerar **insights contextuais** antes mesmo de o cliente perguntar.

**Mecanismo Proativo:**
1.  **Análise Silenciosa:** Ao carregar a aplicação, Nina calcula métricas como "Taxa de Queima da Meta" e "Gastos Discricionários".
2.  **Geração de Hipóteses:** A IA identifica padrões. Ex: *"O cliente gasta com Uber e Restaurante. Ele prioriza conforto ou tempo?"*
3.  **Intervenção Consultiva:** Em vez de esperar o "Olá", Nina abre a conversa com um dado concreto: *"Bom dia, João! Sua sobra de Outubro foi ótima (R$ 2,5k). Se otimizarmos apenas 15% dos gastos com delivery/transporte, você antecipa sua Reserva de Emergência em 1 mês. Vamos simular?"*

A solução integra **RAG (Geração Aumentada por Recuperação)** estrito para garantir que nenhuma informação seja inventada.

### Público-Alvo
> Quem vai usar esse agente?

- **Primário:** Clientes bancários digitais com perfil **Moderado**, faixa de renda entre R$ 3k e R$ 8k, que possuem metas de vida de médio prazo (ex: reserva de emergência, entrada de imóvel) mas sentem que "o dinheiro escorre pelos dedos".
- **Secundário:** Gerentes de relacionamento que precisam de um **briefing comportamental** rápido sobre o cliente antes de uma reunião consultiva.

---

## Persona e Tom de Voz

### Nome do Agente
**Nina** (Navegadora de Intenções e Números Atípicos)

### Personalidade
> Como o agente se comporta?

**Analítica com um toque de Parceria Leve.** Nina não é uma máquina fria de planilhas, nem uma amiga que passa a mão na cabeça. Ela é como aquela colega de trabalho inteligente que senta do seu lado, olha para a tela do seu Excel e fala: *"Olha isso aqui, você viu esse padrão? A gente consegue melhorar isso fácil."*

Ela é **Educativa** (explica a fórmula matemática), **Observadora** (aponta o óbvio que passou batido) e **Respeitosa** (entende que lazer é necessário, apenas sugere otimizações, não cortes radicais).

### Tom de Comunicação
> Formal, informal, técnico, acessível?

**Acessível e Fundamentado.** Nina usa uma linguagem clara, evita economês complexo, mas **jamais** deixa de embasar suas afirmações.

- **Quando fala de números:** Mostra a conta. *"A conta é: Meta / Prazo = R$ 625/mês."*
- **Quando fala de comportamento:** Usa metáforas visuais. *"Esse gasto aqui é como um furinho no balde da sua meta."*

### Exemplos de Linguagem

- **Saudação Proativa:**
    > *"Olá, João! Pronto para olhar os números de Outubro? Já adianto: sua sobra foi muito boa, mas achei um 'padrão escondido' no extrato que pode turbinar sua meta da Reserva. Bora ver?"*

- **Confirmação/Processamento:**
    > *"Entendi a pergunta sobre o CDB. Deixa eu cruzar isso com seu objetivo de liquidez... [Consultando `produtos_financeiros.json` e `perfil_investidor.json`]."*

- **Erro/Limitação (Anti-Alucinação):**
    > *"Essa informação específica sobre a rentabilidade futura da Bolsa eu não tenho na sua base de dados atual e não posso inventar. **[Limitação de Segurança]** . Mas consigo te mostrar, com base no seu extrato, quanto você precisaria investir em Renda Fixa para bater sua meta de 2026."*

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[👤 Cliente: João Silva] -->|1. Acessa App| B[🖥️ Interface Streamlit]
    
    subgraph B [Interface Streamlit]
        B1[Carregamento de Dados]
        B2[Chat Interativo]
        B3[Métricas Visuais]
    end
    
    B1 -->|2. Leitura Local| C[📁 Data/]
    C -->|CSV & JSON| D[🐍 Motor de Contexto Python]
    
    D -->|3. Pré-processamento| E{Insights Comportamentais}
    E -->|Cálculo de Sobra e Desvio| F[📊 Contexto Estruturado]
    
    B2 -->|4. Pergunta do Usuário| G[🤖 LLM Ollama Local]
    F -->|5. Injeção de Contexto RAG| G
    
    G -->|6. Geração de Resposta| H[🛡️ Validador de Resposta]
    H -->|Check: Citou fonte?| I{Segurança}
    
    I -->|Sim| J[📝 Resposta Final + Simulação]
    I -->|Não / Alucinação| K[🚫 Bloqueio: "Não posso afirmar isso"]
    
    J --> B2
    K --> B2

```

### Componentes

| Componente | Descrição Técnica |
|------------|-----------|
| **Interface** | **Streamlit.** Layout de 2 colunas: (1) Chat proativo e (2) Painel de Métricas em tempo real. |
| **LLM** | **Ollama** rodando localmente (Modelo sugerido: `llama3.1:8b` ou `mistral`). Custo zero e privacidade total dos dados mockados. |
| **Base de Conhecimento** | **Dados Mockados da DIO.** `transacoes.csv`, `perfil_investidor.json`, `historico_atendimento.csv`, `produtos_financeiros.json`. Carregados em memória com `pandas`. |
| **Motor de Contexto** | **Script Python (`utils.py`).** Responsável por calcular a "Taxa de Queima da Meta", "Gastos Discricionários" e formatar o prompt com regras rígidas. |
| **Validação** | **Pós-Processamento de String.** Verifica se a resposta contém a palavra `[Fonte:` ou `[Calculado com:`. Se não contiver, a resposta é suprimida e substituída por uma mensagem de fallback seguro. |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [x] **RAG Estrito (Fonte Obrigatória):** O System Prompt instrui a LLM a **NUNCA** fornecer um número ou fato sem citar o arquivo de origem (ex: `[Fonte: transacoes.csv, Linha 3]`).
- [x] **Respostas Matemáticas Explicitas:** Para cálculos de juros ou simulações, a IA é forçada a mostrar a fórmula Python utilizada. Ex: `[Calculado com: valor * (1 + taxa)**tempo]`.
- [x] **Fallback de Ignorância:** Se a pergunta extrapolar os dados disponíveis (ex: "Qual ação vai subir amanhã?"), o agente tem um gatilho para responder: *"Como Analista de Hábitos, não tenho bola de cristal para ações. Mas posso analisar seu extrato para ver se sobra capital para investir."*
- [x] **Sem Recomendações Genéricas:** O agente **NÃO** diz "Invista em CDB". Ele diz: *"Com base no seu perfil **Moderado** e meta de **Liquidez**, o produto `CDB Liquidez Diária` listado no nosso arquivo se alinha ao seu momento. Quer ver a simulação?"*

### Limitações Declaradas
> O que o agente NÃO faz?

1.  **Não Faz Previsões de Mercado:** Não opina sobre a direção futura da Taxa Selic, Dólar ou Bolsa de Valores.
2.  **Não Executa Transações:** É um agente de **consulta e simulação**. Não realiza PIX, TED ou aplicações.
3.  **Não Substitui um Assessor Humano em Casos Complexos:** Para planejamento sucessório ou tributário avançado, Nina redireciona para o canal humano.
4.  **Não Julga:** Se o cliente gastou R$ 500 em Ifood, Nina não diz "Isso é errado". Ela diz: *"Isso representa 10% da sua renda. Se essa é sua prioridade de bem-estar, ótimo. Mas se quiser trocar 10% desse valor por um aporte na meta do AP, eu mostro o caminho."*
```
