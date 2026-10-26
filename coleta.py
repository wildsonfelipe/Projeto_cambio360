# ETAPA 3 - COLETA DE COTAÇÕES 8 moedas estrangeiras:
# Dólar americano (USD)
# Euro (EUR)
# Libra esterlina (GBP)
# Dólar canadense (CAD)
# Peso argentino (ARS)
# Iene Japonês (JPY)
# Franco Suíço (CHF)
# Yuan Chinês (CNY)
# ==========================================

# Importa a função que consulta a AwesomeAPI.
from cambio import consultar_precos

# Importa as funções do banco SQLite.
from banco import criar_tabela, salvar_cotacao


# Função responsável por coletar as moedas
# e armazenar as cotações no banco.
def coletar_cotacoes():

    # Garante que a tabela exista.
    criar_tabela()

    # Consulta todas as moedas de uma vez.
    dados = consultar_precos()

    # Contador de novos registros.
    total_salvos = 0

    # Percorre as moedas retornadas pela API.
    for codigo, cotacao in dados.items():

        # Obtém o código da moeda.
        # Exemplo: USDBRL -> USD.
        moeda = cotacao["code"]

        # Converte os valores para números.
        compra = float(cotacao["bid"])
        venda = float(cotacao["ask"])
        variacao = float(cotacao["pctChange"])

        # Obtém a data informada pela API.
        data_cotacao = cotacao["create_date"]

        # Salva a cotação no banco SQLite.
        inseridos = salvar_cotacao(
            moeda,
            compra,
            venda,
            variacao,
            data_cotacao
        )

        # Atualiza a quantidade de inserções.
        total_salvos += inseridos

        # Mostra o resultado da coleta.
        print(f"\nMoeda: {moeda}")
        print(f"Compra: R$ {compra:.6f}")
        print(f"Venda: R$ {venda:.6f}")
        print(f"Variação: {variacao:+.4f}%")
        print(f"Data: {data_cotacao}")

        if inseridos:
            print("Nova cotação salva!")
        else:
            print("Cotação já armazenada.")

    # Informa o resultado geral.
    print("\nColeta finalizada!")
    print(f"Novos registros: {total_salvos}")

    # Retorna o total para uso no Streamlit.
    return total_salvos


# Executa a coleta quando o arquivo
# é chamado diretamente pelo terminal.
if __name__ == "__main__":

    try:
        coletar_cotacoes()

    except Exception as erro:
        print("Erro durante a coleta:", erro)
