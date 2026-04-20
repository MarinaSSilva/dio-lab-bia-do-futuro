import streamlit as st
import pandas as pd
import json
from langchain_community.llms import Ollama

# Configuração da página
st.set_page_config(page_title="Nina - Coach Financeira", page_icon="🧠", layout="wide")

st.title("🧠 Nina | Navegadora de Intenções e Números Atípicos")
st.caption("Sua coach de micro-otimização financeira")

# Carregar dados mockados
@st.cache_data
def carregar_dados():
    df_trans = pd.read_csv('../data/transacoes.csv')
    df_hist = pd.read_csv('../data/historico_atendimento.csv')
    
    with open('../data/perfil_investidor.json', 'r', encoding='utf-8') as f:
        perfil = json.load(f)
    
    with open('../data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
        produtos = json.load(f)
    
    return df_trans, df_hist, perfil, produtos

df_trans, df_hist, perfil, produtos = carregar_dados()

# Calcular insights
def calcular_insights(df_trans, perfil):
    gasto_total = df_trans[df_trans['tipo'] == 'saída']['valor'].sum()
    receita = df_trans[df_trans['tipo'] == 'entrada']['valor'].sum()
    sobra = receita - gasto_total
    
    meta_restante = perfil['metas'][0]['valor_necessario'] - perfil['reserva_emergencia_atual']
    meses_restantes = 8  # Até Jun/2026
    meta_mensal = meta_restante / meses_restantes
    
    gastos_flexiveis = df_trans[df_trans['categoria'].isin(['lazer', 'alimentacao', 'transporte']) & (df_trans['tipo'] == 'saída')]['valor'].sum()
    
    return {
        'sobra': sobra,
        'meta_restante': meta_restante,
        'meta_mensal': round(meta_mensal, 2),
        'gastos_flexiveis': gastos_flexiveis
    }

insights = calcular_insights(df_trans, perfil)

# Inicializar LLM Ollama
@st.cache_resource
def carregar_llm():
    return Ollama(model="llama3.1:8b", temperature=0.3)

llm = carregar_llm()

# System Prompt
SYSTEM_PROMPT = """
Você é a Nina, uma Navegadora de Intenções e Números Atípicos, um agente de IA do Bradesco criado para a DIO.
Você é uma Coach de Micro-Otimização de Hábitos Financeiros.

REGRAS INVARIÁVEIS (ANTI-ALUCINAÇÃO E SEGURANÇA):
1. ANCORAGEM DE DADOS: Você NÃO pode fornecer nenhum número, data ou fato que não esteja no CONTEXTO abaixo.
2. FONTE OBRIGATÓRIA: Toda vez que mencionar um dado do cliente, finalize com [Fonte: arquivo].
3. CÁLCULO EXPLÍCITO: Mostre a fórmula usada. Ex: [Calculado com: Meta / Meses].
4. NÃO INVISTA, SUGIRA: Nunca ordene "Invista em X". Diga "O produto Y parece alinhado".
5. FALLBACK DE IGNORÂNCIA: Se perguntarem algo fora dos dados, responda que não tem essa informação.

TOM DE VOZ:
- Analítica, mas acolhedora.
- Educativa: explique o porquê dos números.
- Use o nome do cliente: {nome_cliente}.
"""

# Interface do chat
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Converse com a Nina")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensagem de boas-vindas proativa
        msg_boas_vindas = f"""Olá, {perfil['nome']}! 🌟

Já analisei seus dados de Outubro e tenho boas notícias:
- Sua sobra foi de R$ {insights['sobra']:.2f} [Fonte: transacoes.csv]
- Para bater sua meta de reserva, você precisa de R$ {insights['meta_mensal']} por mês [Calculado com: {insights['meta_restante']} / 8 meses]
- Você está INDO MUITO BEM! 🎉

Percebi que você tem R$ {insights['gastos_flexiveis']:.2f} em gastos flexíveis. Que tal fazermos o 'Desafio dos 15%'? Reduzindo só 15% disso, você antecipa sua meta em 1 mês!

Pergunte o que quiser sobre seus gastos, metas ou investimentos!"""
        st.session_state.messages.append({"role": "assistant", "content": msg_boas_vindas})
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Pergunte sobre suas finanças..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Nina está analisando seus dados..."):
                # Montar contexto
                contexto = f"""
CONTEXTO DO CLIENTE:
Nome: {perfil['nome']}
Perfil: {perfil['perfil_investidor']}
Objetivo: {perfil['objetivo_principal']}
Sobra do mês: R$ {insights['sobra']:.2f}
Meta mensal necessária: R$ {insights['meta_mensal']}
Gastos flexíveis (Restaurante/Uber/Netflix): R$ {insights['gastos_flexiveis']:.2f}

Produtos disponíveis para perfil moderado:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

Histórico de atendimentos anteriores:
{df_hist['Tema'].unique().tolist()}

PERGUNTA DO CLIENTE: {prompt}
"""
                
                full_prompt = SYSTEM_PROMPT.format(nome_cliente=perfil['nome']) + "\n\n" + contexto
                
                resposta = llm.invoke(full_prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})

with col2:
    st.subheader("📊 Painel do João")
    st.metric("Sobra de Outubro", f"R$ {insights['sobra']:.2f}")
    st.metric("Meta Mensal Necessária", f"R$ {insights['meta_mensal']}")
    st.metric("Gastos Flexíveis", f"R$ {insights['gastos_flexiveis']:.2f}")
    
    st.divider()
    st.caption("🔒 Dados processados 100% localmente via Ollama")
