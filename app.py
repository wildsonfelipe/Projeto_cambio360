# Bibliotecas para banco de dados e datas.
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

# Bibliotecas para análise e visualização.
import pandas as pd
import streamlit as st

# Função responsável pela coleta de cotações.
from coleta import coletar_cotacoes

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Câmbio 360°",
    page_icon="💱",
    layout="wide"
)

st.title("💱 CÂMBIO 360°")
st.subheader("Dashboard de Monitoramento Cambial")
st.caption(
    "Dólar Americano (USD) | Euro (EUR) |Libra esterlina (GBP)| Dólar canadense (CAD) | Peso argentino (ARS) | Iene Japonês (JPY) | Franco Suíço (CHF) | Yuan Chinês (CNY)"
)
st.caption(
    "Python | Requests | Pandas | SQLite | Streamlit"
)

st.divider()


# ==========================================
# 2. FUNÇÃO PARA CONSULTAR O BANCO
# ==========================================

def carregar_dados():

    # Abre uma conexão com o banco SQLite.
    conexao = sqlite3.connect("cambio360.db")

    try:
        # Consulta os registros armazenados.
        df = pd.read_sql_query(
            """
            SELECT *
            FROM cotacoes
            ORDER BY data_cotacao ASC
            """,
            conexao
        )

    finally:
        # Fecha a conexão após a consulta.
        conexao.close()

    # Converte a coluna de datas.
    if not df.empty:
        df["data_cotacao"] = pd.to_datetime(
            df["data_cotacao"]
        )

    return df


# ==========================================
# FUNÇÃO PARA VERIFICAR A IDADE DA COTAÇÃO
# ==========================================

from datetime import datetime
from zoneinfo import ZoneInfo


def verificar_status(data_cotacao):

    # Obtém o horário atual de Brasília.
    agora = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    )

    # Interpreta a data informada pela API
    # como horário de Brasília.
    data = pd.Timestamp(data_cotacao)

    if data.tzinfo is None:
        data = data.tz_localize(
            "America/Sao_Paulo"
        )
    else:
        data = data.tz_convert(
            "America/Sao_Paulo"
        )

    # Calcula a idade da cotação em horas.
    horas = (agora - data).total_seconds() / 3600

    # Classifica a cotação conforme sua idade.
    if horas < 0:
        return "⚠️ Data futura"

    elif horas <= 1:
        return "🟢 Recente"

    elif horas <= 24:
        return "🟡 Sem atualização recente"

    else:
        return "🔴 Cotação antiga"


# ==========================================
# 3. ATUALIZAÇÃO AUTOMÁTICA
# ==========================================

# Executa esta função automaticamente
# a cada 60 segundos enquanto a sessão
# do dashboard estiver ativa.
@st.fragment(run_every="60s")
def atualizar_dashboard():

    # Consulta a API e tenta salvar
    # novas cotações no banco.
    try:
        novos = coletar_cotacoes()

        st.success(
            f"Consulta realizada! "
            f"Novos registros: {novos}"
        )

    except Exception as erro:

        # Caso a API apresente erro,
        # informa o problema e continua
        # utilizando o histórico salvo.
        st.warning(
            f"Falha na atualização da API: {erro}"
        )

    # Carrega os registros do banco SQLite.
    try:
        df = carregar_dados()

    except (sqlite3.Error, ValueError) as erro:
        st.error(f"Erro ao consultar o banco: {erro}")
        return

    # Verifica se existem registros.
    if df.empty:
        st.warning("Nenhuma cotação armazenada.")
        return

    # ======================================
    # 4. ÚLTIMAS COTAÇÕES
    # ======================================

    st.subheader("📊 Últimas Cotações")

    # Seleciona o registro mais recente
    # de cada moeda.
    ultimas = (
        df.sort_values("data_cotacao")
        .groupby("moeda")
        .tail(1)
        .sort_values("moeda")
    )
# Cria uma coluna com a situação de cada cotação.
    ultimas = ultimas.copy()

    ultimas["status"] = ultimas["data_cotacao"].apply(
    verificar_status
)

    # Cria quatro colunas por linha.
    colunas = st.columns(4)

    for i, (_, linha) in enumerate(
        ultimas.iterrows()
    ):

        # Moedas de baixo valor precisam
        # de mais casas decimais.
        casas = (
            6 if linha["compra"] < 0.1
            else 4
        )

        with colunas[i % 4]:

            st.metric(
                label=f"{linha['moeda']}/BRL",
                value=f"R$ {linha['compra']:.{casas}f}",
                delta=f"{linha['variacao']:+.4f}%"
            )

    st.divider()

    
    
    
    
    # ======================================
    # 5. DIAGNÓSTICO DA TABELA
    # ======================================

    st.subheader("📋 Tabela de Cotações")

    try:
       
        # Seleciona as colunas necessárias.
        tabela = ultimas[
            [
                "moeda",
                "compra",
                "venda",
                "variacao",
                "data_cotacao",
                "status"
            ]
        ].copy()

       
        # Renomeia as colunas.
        tabela.columns = [
            "Moeda",
            "Compra (R$)",
            "Venda (R$)",
            "Variação (%)",
            "Data da Cotação",
            "Situação"
        ]

     
        # Converte os valores para apresentação.
        tabela["Compra (R$)"] = tabela[
            "Compra (R$)"
        ].map(lambda valor: f"{valor:.6f}")

        tabela["Venda (R$)"] = tabela[
            "Venda (R$)"
        ].map(lambda valor: f"{valor:.6f}")

        tabela["Variação (%)"] = tabela[
            "Variação (%)"
        ].map(lambda valor: f"{valor:+.4f}%")

        st.write("ETAPA 4: Valores formatados")

        # Exibe a tabela.
        st.dataframe(
            tabela,
            hide_index=True
        )
    
    except Exception as erro:

        # Exibe o erro completo no dashboard.
        st.exception(erro)

    # ======================================
    # 6. GRÁFICO HISTÓRICO
    # ======================================

    st.subheader("📈 Histórico Cambial")

    # Recupera as moedas disponíveis.
    moedas = sorted(df["moeda"].unique())

    # Permite selecionar uma moeda.
    moeda = st.selectbox(
        "Selecione a moeda:",
        moedas,
        key="moeda_historico"
    )

    # Filtra os dados da moeda selecionada.
    historico = df[
        df["moeda"] == moeda
    ].copy()

    # Organiza as cotações por data.
    historico = historico.sort_values(
        "data_cotacao"
    )

    # Exibe o gráfico somente quando
    # existem pelo menos dois registros.
    if len(historico) >= 2:

        grafico = historico.set_index(
            "data_cotacao"
        )

        st.line_chart(
            grafico["compra"]
        )

    else:
        st.info(
            "Ainda não existem cotações "
            "suficientes para gerar o gráfico."
        )

    st.write(
        f"Registros de {moeda}: {len(historico)}"
    )

    # ======================================
    # 7. HISTÓRICO ARMAZENADO
    # ======================================

    st.subheader("🗄️ Histórico no SQLite")

    st.dataframe(
        historico,
        hide_index=True,
        use_container_width=True
    )

    # ======================================
    # 8. EXPORTAÇÃO CSV
    # ======================================

    # Converte o histórico completo para CSV.
    csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "📥 Baixar histórico completo",
        data=csv,
        file_name="cambio360_historico.csv",
        mime="text/csv"
    )

    st.caption(
        "Consultas automáticas a cada 60 segundos. "
        "As cotações podem permanecer iguais "
        "quando o mercado não publicar novos dados."
    )


# ==========================================
# 9. INICIAR O DASHBOARD
# ==========================================

atualizar_dashboard()
