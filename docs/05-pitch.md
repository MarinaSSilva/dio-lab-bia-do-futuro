# Pitch (3 minutos)

## Roteiro Resumido

### 1. O Problema (30 seg)
> Qual dor do cliente você resolve?

O problema abordado é a **Dissonância Comportamental Financeira**: a lacuna entre o que o cliente declara como objetivo (ex: "quero guardar dinheiro para reserva de emergência") e o comportamento real registrado no extrato bancário.

O cliente típico (representado pelo personagem João Silva) sente que o dinheiro "some" sem perceber para onde foi. Os aplicativos bancários tradicionais mostram saldo e extrato, mas não interpretam padrões nem conectam os gastos do dia a dia com as metas de longo prazo. O resultado é ansiedade financeira e sensação de estagnação, mesmo quando os números mostram que há capacidade de sobra.

---

### 2. A Solução (1 min)
> Como seu agente resolve esse problema?

A solução é a **Nina**, um agente de IA Generativa baseado em Ollama (local) e Streamlit, especializado em **Micro-Otimização de Hábitos Financeiros**.

O agente realiza três ações principais:
1. **Cruzamento de Dados:** Lê arquivos JSON (perfil do investidor) e CSV (transações) para comparar a intenção declarada com o comportamento real.
2. **Cálculo Proativo:** Calcula métricas como "Taxa de Queima da Meta" (quanto falta / quantos meses restam) e identifica gastos flexíveis que podem ser otimizados sem cortes radicais.
3. **Sugestões Acionáveis:** Propõe micro-ajustes (ex: "Desafio dos 15%" - reduzir apenas 15% de gastos com delivery/transporte) e mostra o impacto acumulado no longo prazo.

A segurança é garantida por **RAG Estrito**: toda resposta numérica exibe a fonte do dado (ex: `[Fonte: transacoes.csv]`) ou a fórmula de cálculo utilizada, prevenindo alucinações.

---

### 3. Demonstração (1 min)
> O que será mostrado na prática (gravação de tela)

A demonstração exibirá a interface do Streamlit com o chat da Nina em funcionamento, processando os dados mockados do cliente João Silva.

**Cenário 1 - Análise de Progresso:**
- Entrada do usuário: *"Nina, como estou indo esse mês?"*
- Saída do agente: Exibição da sobra de Outubro (R$ 2.511,10), comparação com a meta mensal necessária (R$ 625,00) e confirmação de que o cliente está acima do esperado.

**Cenário 2 - Sugestão de Micro-Otimização:**
- Entrada do usuário: *"Vale a pena cortar a Netflix?"*
- Saída do agente: Em vez de sugerir o corte total, a IA identifica gastos com Restaurante (R$ 120) e Uber (R$ 45) e propõe uma redução de apenas 15% nesses itens, mostrando o impacto positivo na antecipação da meta.

O foco da demonstração é evidenciar que o agente não emite ordens, mas oferece **perspectivas baseadas em dados**, deixando a decisão final com o usuário.

---

### 4. Diferencial e Impacto (30 seg)
> Por que essa solução é inovadora e qual seu impacto?

**Diferenciais competitivos:**
- **Execução 100% Local:** Uso do Ollama garante privacidade total dos dados e custo zero de API.
- **Foco em Micro-Otimização:** Diferente de consultores tradicionais que sugerem cortes radicais (baixa adesão), a Nina propõe ajustes marginais sustentáveis a longo prazo.
- **Anti-Alucinação por Design:** Sistema de validação que exige citação de fonte ou fórmula matemática em todas as respostas numéricas.

**Impacto social esperado:**
Redução da ansiedade financeira por meio da **clareza de dados**. O agente devolve ao usuário a percepção de controle sobre suas finanças, transformando metas distantes (ex: "comprar um apartamento em 2027") em consequências matemáticas de pequenas escolhas diárias. A solução tem potencial para ser integrada a aplicativos bancários como uma camada de **educação financeira comportamental escalável**.

---

## Checklist do Pitch

- [ ] Duração máxima de 3 minutos
- [ ] Problema claramente definido
- [ ] Solução demonstrada na prática (gravação de tela do Streamlit)
- [ ] Diferencial explicado
- [ ] Áudio e vídeo com boa qualidade

---

## Link do Vídeo

> *Cole aqui o link do seu pitch (YouTube, Loom, Google Drive, etc.) após a gravação.*

[Link do vídeo]
