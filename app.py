
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial do app
st.set_page_config(page_title="Controle Financeiro", layout="wide")

# Dados iniciais
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor", "Status", "Mês"])

# Título
st.title("App de Controle Financeiro")

# Aba de navegação
tab1, tab2, tab3 = st.tabs(["📊 Dados", "📈 Resumo", "🔮 Projeções"])

# Aba 1: Cadastro de Dados
with tab1:
    st.subheader("Cadastro de Transações")
    with st.form("cadastro_form"):
        data = st.date_input("Data")
        categoria = st.selectbox("Categoria", ["A Pagar", "A Receber"])
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, step=0.01)
        status = st.selectbox("Status", ["Pendente", "Pago", "Vencido"])
        mes = st.text_input("Mês", value=str(data.month))
        submit = st.form_submit_button("Adicionar Transação")

        if submit:
            nova_linha = pd.DataFrame([[data, categoria, descricao, valor, status, mes]],
                                       columns=["Data", "Categoria", "Descrição", "Valor", "Status", "Mês"])
            st.session_state.data = pd.concat([st.session_state.data, nova_linha], ignore_index=True)
            st.success("Transação adicionada com sucesso!")

    # Mostrar tabela de dados
    st.dataframe(st.session_state.data)

# Aba 2: Resumo Financeiro
with tab2:
    st.subheader("Resumo Financeiro")
    dados = st.session_state.data

    if not dados.empty:
        total_a_pagar = dados[dados["Categoria"] == "A Pagar"]["Valor"].sum()
        total_a_receber = dados[dados["Categoria"] == "A Receber"]["Valor"].sum()
        saldo_atual = total_a_receber - total_a_pagar
        contas_vencidas = len(dados[dados["Status"] == "Vencido"])

        # KPIs
        st.metric("Total a Pagar", f"R$ {total_a_pagar:,.2f}")
        st.metric("Total a Receber", f"R$ {total_a_receber:,.2f}")
        st.metric("Saldo Atual", f"R$ {saldo_atual:,.2f}")
        st.metric("Contas Vencidas", contas_vencidas)

        # Gráficos
        st.subheader("Gráficos")
        grafico_fluxo = px.line(dados, x="Mês", y="Valor", color="Categoria", title="Fluxo de Caixa Mensal")
        st.plotly_chart(grafico_fluxo, use_container_width=True)

        grafico_pizza = px.pie(dados, names="Categoria", values="Valor", title="Proporção de Categorias")
        st.plotly_chart(grafico_pizza, use_container_width=True)
    else:
        st.warning("Nenhuma transação cadastrada.")

# Aba 3: Projeções
with tab3:
    st.subheader("Simulações de Projeções")
    st.write("Funcionalidade em desenvolvimento...")

# Exportação
st.download_button("Baixar Dados em Excel", data=dados.to_csv(index=False), file_name="controle_financeiro.csv")
