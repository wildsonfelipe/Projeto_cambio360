
# Importa a biblioteca requests, utilizada para realizar requisições HTTP e consumir APIs.
import requests


# Função responsável por consultar o preço de uma moeda estrangeira em relação ao real.

# ==========================================
# CÂMBIO 360°
# CONEXÃO COM A AWESOMEAPI
# ==========================================

# Biblioteca utilizada para consultar APIs.
import requests


# Lista das moedas que serão monitoradas.
MOEDAS = [
    "USD", "EUR", "GBP", "CAD",
    "ARS", "JPY", "CHF", "CNY"
]


# Função responsável por consultar todas
# as moedas em uma única requisição HTTP.
def consultar_precos():

    # Monta os pares cambiais.
    # Exemplo: USD-BRL,EUR-BRL,GBP-BRL.
    pares = ",".join(
        f"{moeda}-BRL" for moeda in MOEDAS
    )

    # Monta a URL completa da AwesomeAPI.
    url = (
        "https://economia.awesomeapi.com.br/"
        f"json/last/{pares}"
    )

    # Envia uma única requisição GET.
    resposta = requests.get(
        url,
        timeout=15
    )

    # Identifica erros HTTP, incluindo 429.
    resposta.raise_for_status()

    # Converte a resposta JSON em dicionário.
    dados = resposta.json()

    # Retorna as cotações para coleta.py.
    return dados


# Executa um teste quando este arquivo
# é iniciado diretamente no terminal.
if __name__ == "__main__":

    try:
        dados = consultar_precos()

        # Exibe os preços recebidos da API.
        for codigo, cotacao in dados.items():
            print(
                f"{codigo}: "
                f"R$ {float(cotacao['bid']):.6f}"
            )

        print("\nConsulta concluída!")

    except requests.RequestException as erro:
        print("Erro ao consultar a API:", erro)
