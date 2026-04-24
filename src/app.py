import streamlit as st
import pandas as pd
import json
from datetime import date
from langchain_community.llms import Ollama
import plotly.express as px

st.set_page_config(page_title="Nina - Coach Financeira", page_icon="🧠", layout="wide")

st.title("🧠 Nina | Navegadora de Intenções e Números Atípicos")
st.caption("Sua coach de micro-otimização financeira")


# ---------------------------------------------------------------------------
# 1. CARREGAMENTO DE DADOS
# ---------------------------------------------------------------------------

@st.cache_data
def carregar_dados():
    df_trans = pd.read_csv("../data/transacoes.csv")
    df_hist = pd.read_csv("../data/historico_atendimento.csv")

    with open("../data/perfil_investidor.json", "r", encoding="utf-8") as f:
        perfil = json.load(f)

    with open("../data/produtos_financeiros.json", "r", encoding="utf-8") as f:
        produtos = json.load(f)

    return df_trans, df_hist, perfil, produtos


df_trans, df_hist, perfil, produtos = carregar_dados()


# ---------------------------------------------------------------------------
# 2. CALCULO DE INSIGHTS
# FIX: tipo sem acento ("saida"/"entrada") para bater com o CSV
# FIX: meses_restantes calculado dinamicamente
# FIX: gastos_flexiveis filtra corretamente por tipo E categoria
# ---------------------------------------------------------------------------

def calcular_insights(df_trans: pd.DataFrame, perfil: dict) -> dict:
    saidas = df_trans[df_trans["tipo"] == "saida"]
    entradas = df_trans[df_trans["tipo"] == "entrada"]

    gasto_total = saidas["valor"].sum()
    receita = entradas["valor"].sum()
    sobra = receita - gasto_total

    meta = perfil["metas"][0]
    meta_restante = meta["valor_necessario"] - perfil["reserva_emergencia_atual"]

    prazo_str = meta.get("prazo", "2026-06-01")
    if len(prazo_str) == 7:
        prazo_str += "-01"
    prazo = date.fromisoformat(prazo_str)
    hoje = date.today()
    meses_restantes = max(
        1,
        (prazo.year - hoje.year) * 12 + (prazo.month - hoje.month),
    )

    meta_mensal = round(meta_restante / meses_restantes, 2)

    categorias_flexiveis = {"lazer", "alimentacao", "transporte"}
    gastos_flexiveis = saidas[
        saidas["categoria"].str.lower().isin(categorias_flexiveis)
    ]["valor"].sum()

    detalhe_gastos = (
        saidas[saidas["categoria"].str.lower().isin(categorias_flexiveis)]
        .groupby("categoria")["valor"]
        .sum()
        .round(2)
        .to_dict()
    )

    return {
        "receita": round(receita, 2),
        "gasto_total": round(gasto_total, 2),
        "sobra": round(sobra, 2),
        "meta_restante": round(meta_restante, 2),
        "meta_mensal": meta_mensal,
        "meses_restantes": meses_restantes,
        "gastos_flexiveis": round(gastos_flexiveis, 2),
        "detalhe_gastos": detalhe_gastos,
    }


insights = calcular_insights(df_trans, perfil)


# ---------------------------------------------------------------------------
# 3. LLM
# ---------------------------------------------------------------------------

@st.cache_resource
def carregar_llm():
    return Ollama(model="phi3", temperature=0.3)


llm = carregar_llm()


# ---------------------------------------------------------------------------
# 4. SYSTEM PROMPT
# FIX: usa f-string direta para evitar KeyError com chaves JSON no .format()
# ---------------------------------------------------------------------------

def montar_system_prompt(nome_cliente: str) -> str:
    return (
        f"Você é a Nina, uma Navegadora de Intenções e Números Atípicos, "
        f"um agente de IA do Bradesco criado para a DIO.\n"
        f"Você é uma Coach de Micro-Otimização de Hábitos Financeiros.\n\n"
        f"SEU OBJETIVO PRINCIPAL:\n"
        f"Cruzar a intenção declarada pelo cliente (metas no JSON) com o comportamento "
        f"real (transações no CSV) para revelar padrões escondidos e sugerir micro-ajustes "
        f"que aceleram metas sem sacrificar qualidade de vida.\n\n"
        f"REGRAS INVARIÁVEIS (ANTI-ALUCINAÇÃO E SEGURANÇA):\n"
        f"1. ANCORAGEM DE DADOS: Você NÃO pode fornecer nenhum número, data ou fato que "
        f"não esteja explicitamente no [BLOCO DE CONTEXTO] ou que não seja resultado de "
        f"cálculo matemático básico.\n"
        f"2. FONTE OBRIGATÓRIA: Toda vez que mencionar um dado do cliente, finalize com "
        f"[Fonte: arquivo]. Ex: [Fonte: transacoes.csv, Outubro].\n"
        f"3. CÁLCULO EXPLÍCITO: Mostre a fórmula usada. "
        f"Ex: [Calculado com: Meta Restante / Meses Restantes].\n"
        f"4. NÃO INVISTA, SUGIRA: Nunca ordene 'Invista em X'. Diga: 'O produto Y parece "
        f"alinhado ao seu perfil. Quer simular?'\n"
        f"5. FALLBACK DE IGNORÂNCIA: Se a pergunta estiver fora dos dados disponíveis, "
        f"responda: 'Isso está fora da minha alçada de Coach de Hábitos. Não tenho bola "
        f"de cristal para o mercado, mas tenho uma lupa para o seu extrato. Quer que eu "
        f"analise seus gastos de Outubro?'\n\n"
        f"TOM DE VOZ: Analítica e acolhedora. Use o nome do cliente: {nome_cliente}.\n"
        f"Seja educativa — explique o porquê dos números. Use metáforas simples.\n\n"
        f"ESTRUTURA DA RESPOSTA:\n"
        f"1. Validação da pergunta.\n"
        f"2. Insight com dado exato do contexto + [Fonte] ou [Calculado com].\n"
        f"3. Micro-sugestão acionável ou oferta de simulação.\n"
    )


# ---------------------------------------------------------------------------
# 5. MONTAGEM DO CONTEXTO RAG
# FIX: campo "meta" no lugar de "descricao" (correto no JSON)
# FIX: campo "indicado_para" no lugar de "liquidez" (que não existe no JSON)
# FIX: inclui Produtos e Histórico que estavam no bloco corrompido da versão anterior
# ---------------------------------------------------------------------------

def montar_contexto(insights: dict, perfil: dict, produtos: list, df_hist: pd.DataFrame, pergunta: str) -> str:
    temas_anteriores = df_hist["tema"].dropna().unique().tolist()

    produtos_perfil = [
        p for p in produtos
        if p.get("risco", "").lower() in {"baixo", "medio", "médio"}
    ]
    produtos_str = "\n".join(
        f"- {p['nome']} | Risco: {p['risco']} | Indicado para: {p.get('indicado_para', 'N/A')}"
        for p in produtos_perfil
    )

    detalhe_str = "\n".join(
        f"  - {cat.capitalize()}: R$ {val:.2f}"
        for cat, val in insights["detalhe_gastos"].items()
    )

    return (
        f"[BLOCO DE CONTEXTO - DADOS CALCULADOS EM TEMPO DE EXECUÇÃO]\n\n"
        f"DADOS DO CLIENTE (Fonte: perfil_investidor.json):\n"
        f"- Nome: {perfil['nome']}\n"
        f"- Perfil: {perfil['perfil_investidor']}\n"
        f"- Objetivo principal: {perfil['objetivo_principal']}\n"
        f"- Meta: {perfil['metas'][0]['meta']} | Valor necessário: R$ {perfil['metas'][0]['valor_necessario']:.2f}\n"
        f"- Já acumulado: R$ {perfil['reserva_emergencia_atual']:.2f}\n"
        f"- Faltam: R$ {insights['meta_restante']:.2f} em {insights['meses_restantes']} meses\n\n"
        f"ANÁLISE DO MÊS (Fonte: transacoes.csv + cálculos Python):\n"
        f"- Receita: R$ {insights['receita']:.2f}\n"
        f"- Gastos totais: R$ {insights['gasto_total']:.2f}\n"
        f"- Sobra do mês: R$ {insights['sobra']:.2f}\n"
        f"- Necessário para a meta: R$ {insights['meta_mensal']:.2f}/mês "
        f"[Calculado com: {insights['meta_restante']} / {insights['meses_restantes']}]\n"
        f"- Gastos flexíveis (otimizáveis): R$ {insights['gastos_flexiveis']:.2f}\n"
        f"{detalhe_str}\n\n"
        f"PRODUTOS DISPONÍVEIS PARA PERFIL {perfil['perfil_investidor'].upper()} "
        f"(Fonte: produtos_financeiros.json):\n"
        f"{produtos_str}\n\n"
        f"HISTÓRICO DE TEMAS JÁ DISCUTIDOS (Fonte: historico_atendimento.csv):\n"
        f"- {', '.join(temas_anteriores) if temas_anteriores else 'Nenhum registro anterior'}\n"
        f"(Se o cliente perguntar sobre um tema já discutido, não explique do zero — "
        f"contextualize com base no histórico.)\n\n"
        f"[FIM DO BLOCO DE CONTEXTO]\n\n"
        f"Responda diretamente à seguinte pergunta: {pergunta}\n"
    )


# ---------------------------------------------------------------------------
# 6. VALIDAÇÃO ANTI-ALUCINAÇÃO
# Verifica se a resposta cita pelo menos uma fonte antes de exibir
# ---------------------------------------------------------------------------

def resposta_tem_fonte(resposta: str) -> bool:
    marcadores = ["[Fonte:", "[Calculado com:", "[Limitação"]
    return any(m in resposta for m in marcadores)


FALLBACK_SEGURO = (
    "⚠️ Nina não conseguiu ancorar essa resposta nos dados disponíveis. "
    "Por segurança, a resposta foi bloqueada.\n\n"
    "Tente reformular a pergunta com foco nos seus gastos de Outubro ou nas suas metas cadastradas."
)


# ---------------------------------------------------------------------------
# 7. INTERFACE
# ---------------------------------------------------------------------------

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Converse com a Nina")

    if "messages" not in st.session_state:
        msg_boas_vindas = (
            f"Olá, {perfil['nome']}! 🌟\n\n"
            f"Já analisei seus dados de Outubro e tenho boas notícias:\n"
            f"- Sua sobra foi de **R$ {insights['sobra']:.2f}** [Fonte: transacoes.csv]\n"
            f"- Para bater sua meta, você precisa de **R$ {insights['meta_mensal']}/mês** "
            f"[Calculado com: {insights['meta_restante']} / {insights['meses_restantes']} meses]\n"
            f"- Você está indo muito bem! 🎉\n\n"
            f"Percebi **R$ {insights['gastos_flexiveis']:.2f}** em gastos flexíveis. "
            f"Que tal o **Desafio dos 15%**? Reduzindo só 15% desses gastos, "
            f"você antecipa sua meta em ~1 mês!\n\n"
            f"Pergunte o que quiser sobre seus gastos, metas ou produtos disponíveis."
        )
        st.session_state.messages = [{"role": "assistant", "content": msg_boas_vindas}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Pergunte sobre suas finanças..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Nina está analisando seus dados..."):
                system_prompt = montar_system_prompt(perfil["nome"])
                contexto = montar_contexto(insights, perfil, produtos, df_hist, prompt)
                full_prompt = system_prompt + "\n\n" + contexto

                resposta = llm.invoke(full_prompt)

                if resposta_tem_fonte(resposta):
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                else:
                    st.warning(FALLBACK_SEGURO)
                    st.session_state.messages.append({"role": "assistant", "content": FALLBACK_SEGURO})

with col2:
    st.subheader(f"📊 Painel de {perfil['nome'].split()[0]}")
    st.metric("Sobra de Outubro", f"R$ {insights['sobra']:.2f}")
    st.metric("Aporte mensal necessário", f"R$ {insights['meta_mensal']:.2f}")
    st.metric(
        "Gastos flexíveis",
        f"R$ {insights['gastos_flexiveis']:.2f}",
        help="Lazer + Alimentação fora + Transporte por app",
    )
    st.metric("Meses restantes para a meta", insights["meses_restantes"])

    # Gráfico de evolução da meta
    st.subheader("📈 Evolução da Meta")
    
    meta_total = perfil['metas'][0]['valor_necessario']
    acumulado = perfil['reserva_emergencia_atual']
    faltante = meta_total - acumulado
    
    fig = px.bar(
        x=["Reserva de Emergência"],
        y=[acumulado],
        title=f"Progresso: R$ {acumulado:.2f} de R$ {meta_total:.2f}",
        labels={"x": "", "y": "Valor (R$)"},
        color_discrete_sequence=["#10B981"],  # Verde
        text=[f"R$ {acumulado:.2f}"]
    )
    
    fig.add_bar(
        x=["Reserva de Emergência"],
        y=[faltante],
        name="Faltante",
        marker_color="#E5E7EB",  # Cinza claro
        text=[f"Falta R$ {faltante:.2f}"]
    )
    
    fig.update_layout(
        barmode="stack",
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    fig.update_traces(
        selector={"name": "Acumulado"},
        textposition="inside",
        textfont=dict(size=12, color="white"),
    )

    fig.update_traces(
        selector={"name": "Faltante"},
        textposition="inside",
        textfont=dict(size=12, color="#6B7280"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Percentual de progresso
    percentual = (acumulado / meta_total) * 100
    st.progress(percentual / 100, text=f"{percentual:.1f}% concluído")

    st.divider()

    st.caption("🔒 Dados processados 100% localmente via Ollama")
    st.caption("Modelo ativo: phi3")
