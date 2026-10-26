# ETAPA 2 - BANCO DE DADOS SQLITE
# ==========================================

#Importa a biblioteca sqlite3. Ela permite criar e manipular bancos SQLite.
import sqlite3

# Importa datetime para registrar a data e a hora em que cada cotação foi coletada.
from datetime import datetime, timezone

# Nome do arquivo do banco de dados.
NOME_BANCO = "cambio360.db"


# Função responsável por criar a tabela onde serão armazenadas as cotações.
def criar_tabela():

    # Abre uma conexão com o banco. Se o arquivo não existir, será criado.
    conexao = sqlite3.connect(NOME_BANCO)

    # Cria um cursor para executar SQL.
    cursor = conexao.cursor()

    # Cria a tabela somente se ela não existir.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            moeda TEXT NOT NULL,
            compra REAL NOT NULL,
            venda REAL NOT NULL,
            variacao REAL,
            data_cotacao TEXT NOT NULL,
            data_coleta TEXT NOT NULL,
            UNIQUE(moeda, data_cotacao)
        )
    """)

    # Confirma as alterações no banco.
    conexao.commit()

    # Encerra a conexão.
    conexao.close()


# Função responsável por salvar uma cotação.
def salvar_cotacao(
    moeda, compra, venda, variacao, data_cotacao
):

    # Registra a data e a hora da coleta em UTC.
    data_coleta = datetime.now(
        timezone.utc
    ).isoformat()

    # Conecta ao banco de dados.
    conexao = sqlite3.connect(NOME_BANCO)

    cursor = conexao.cursor()

    # Insere a cotação no banco. OR IGNORE evita duplicar uma cotação com a mesma moeda e data_cotacao.
    
    cursor.execute("""
        INSERT OR IGNORE INTO cotacoes (
            moeda,
            compra,
            venda,
            variacao,
            data_cotacao,
            data_coleta
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        moeda,
        compra,
        venda,
        variacao,
        data_cotacao,
        data_coleta
    ))

    # Verifica se um novo registro foi inserido.
    inseridos = cursor.rowcount

    # Salva a alteração.
    conexao.commit()

    # Fecha a conexão.
    conexao.close()

    return inseridos


# Executa a criação da tabela quando
# este arquivo é chamado diretamente.
if __name__ == "__main__":

    criar_tabela()

    print("Banco de dados criado com sucesso!")
    print("Tabela cotacoes pronta para uso.")
