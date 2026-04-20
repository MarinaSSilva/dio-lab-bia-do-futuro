# Código da Aplicação - Nina

Esta pasta contém o código-fonte do agente financeiro **Nina**, uma aplicação de Micro-Otimização de Hábitos desenvolvida com Streamlit e Ollama.

---

## Estrutura do Código

```
src/
├── app.py # Aplicação principal (Interface Streamlit)
├── utils.py # Motor de contexto e pré-processamento de dados
├── prompts.py # System Prompt e templates (opcional)
└── requirements.txt # Dependências do projeto
```

### Descrição dos Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Interface do usuário em Streamlit. Gerencia o estado da sessão, carrega os dados mockados e faz a comunicação com o Ollama. |
| `utils.py` | Funções auxiliares: `carregar_dados()`, `calcular_insights()` e `formatar_contexto()`. Responsável por cruzar CSV e JSON para gerar o "Contexto Estruturado" enviado à LLM. |
| `prompts.py` | (Opcional) Armazena o System Prompt e exemplos de Few-Shot separados do código principal para melhor organização. |
| `requirements.txt` | Lista de bibliotecas Python necessárias para execução. |

---

## 📦 Dependências (`requirements.txt`)

```
text
streamlit>=1.28.0
pandas>=2.0.0
ollama>=0.1.0
langchain>=0.1.0
langchain-community>=0.1.0
```
---

## Explicação de cada dependência:

streamlit: Framework para interface web interativa.

pandas: Leitura e manipulação dos arquivos CSV/JSON.

ollama: Cliente Python para comunicação com o modelo local.

langchain: Orquestração de prompts e templates dinâmicos.

langchain-community: Integração específica com Ollama.

---

## 🚀 Como Rodar a Aplicação

### Pré-requisitos

1. Python 3.9+ instalado.
2. Ollama instalado e rodando localmente.
* Download: https://ollama.ai
* Após instalar, baixe o modelo recomendado:

```
ollama pull llama3.1:8b
```

* Verifique se o serviço está ativo:

```
ollama serve
```

---

## Passo a Passo
1. Navegue até a pasta src/:

```
cd dio-lab-bia-do-futuro/src
```

2. Crie um ambiente virtual (recomendado):

```
python -m venv venv

# Ativação (Windows)
venv\Scripts\activate

# Ativação (Linux/Mac)
source venv/bin/activate
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Execute a aplicação:

```
streamlit run app.py
```

5. Acesse no navegador:

O Streamlit abrirá automaticamente em http://localhost:8501

---

## 🧪 Testando a Aplicação
Após iniciar, você verá a interface da Nina com:

Coluna Esquerda: Chat interativo para conversar com o agente.

Coluna Direita: Painel com métricas em tempo real (Sobra do Mês, Meta Mensal, etc.)

Sugestões de perguntas para teste:

"Nina, como estou indo esse mês?"

"Quanto falta para minha reserva de emergência?"

"O que você acha dos meus gastos com delivery?"

"Qual investimento combina mais comigo?"

"Qual a previsão do tempo?" (Teste de Edge Case)

---

## 🔧 Personalização
Trocar o Modelo Ollama
No arquivo app.py, localize a linha:

```
llm = Ollama(model="llama3.1:8b")
```

### Substitua por qualquer modelo disponível localmente:

```
llm = Ollama(model="mistral")      # Mais rápido
llm = Ollama(model="phi3")          # Mais leve
llm = Ollama(model="llama3.1:70b") # Mais potente (requer mais RAM)
```

### Alterar os Dados Mockados
Os dados são carregados da pasta ../data/. Para testar com outros dados:

Substitua os arquivos CSV/JSON mantendo os mesmos nomes.

Certifique-se de que as colunas do CSV mantêm a mesma estrutura.

---

## 📊 Fluxo de Execução (Visão Geral)

```
1. streamlit run app.py
         ↓
2. @st.cache_data carrega CSV/JSON da pasta ../data/
         ↓
3. utils.calcular_insights() processa os dados brutos
         ↓
4. Interface Streamlit renderiza chat e métricas
         ↓
5. Usuário digita pergunta no chat_input
         ↓
6. utils.formatar_contexto() injeta dados no System Prompt
         ↓
7. Ollama gera resposta baseada no contexto
         ↓
8. Validador verifica presença de [Fonte: ...]
         ↓
9. Resposta é exibida no chat
```

---

## 🐛 Solução de Problemas Comuns

```
Erro	Causa Provável	Solução
ConnectionError: Ollama not running	Serviço Ollama parado	Execute ollama serve em outro terminal
Model not found: llama3.1:8b	Modelo não baixado	Execute ollama pull llama3.1:8b
FileNotFoundError: ../data/transacoes.csv	Caminho relativo incorreto	Execute de dentro da pasta src/
Respostas muito lentas	Modelo pesado para seu hardware	Troque para phi3 ou tinyllama
ModuleNotFoundError	Dependência faltando	Execute pip install -r requirements.txt
```

---

## 📝 Observações
Privacidade: Toda a execução é local. Nenhum dado é enviado para APIs externas.

Custo: Zero. Ollama é gratuito e open-source.

Desempenho: Recomenda-se mínimo de 8GB RAM para llama3.1:8b.

```
Esse `README.md` dentro da pasta `src/` complementa o README principal, fornecendo todas as instruções técnicas para quem quiser rodar o código. 🚀
```
















