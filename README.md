# 💱 CÂMBIO 360°

### Dashboard de Monitoramento Cambial

Projeto acadêmico desenvolvido em Python para consultar, armazenar e visualizar cotações de moedas estrangeiras em relação ao real brasileiro (BRL).

O sistema utiliza uma API pública para obter os dados cambiais, grava as cotações em um banco de dados SQLite e apresenta as informações em um dashboard interativo construído com Streamlit.

## 🎯 Objetivo

Aplicar conceitos de **consumo de API REST, tratamento de dados, persistência em banco de dados e visualização de informações**, integrando diferentes ferramentas estudadas no curso de Ciência de Dados.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Requests:** requisições HTTP para consultar a API.
- **Pandas:** organização, seleção e tratamento dos dados.
- **SQLite:** armazenamento local do histórico de cotações.
- **Streamlit:** desenvolvimento do dashboard interativo.
- **AwesomeAPI:** fonte das cotações cambiais.

## 💰 Moedas monitoradas

| Código | Moeda |
|---|---|
| USD | Dólar americano |
| EUR | Euro |
| GBP | Libra esterlina |
| CAD | Dólar canadense |
| ARS | Peso argentino |
| JPY | Iene japonês |
| CHF | Franco suíço |
| CNY | Yuan chinês |

Todas as cotações são apresentadas em relação ao **real brasileiro (BRL)**.

## 📁 Estrutura do projeto

```text
cambio360/
├── app.py              # Dashboard Streamlit
├── cambio.py           # Consulta à API de câmbio
├── coleta.py           # Processamento e coleta das cotações
├── banco.py            # Criação do banco e gravação dos dados
├── cambio360.db        # Banco SQLite (gerado pela aplicação)
└── README.md           # Documentação do projeto
```

## ⚙️ Como o sistema funciona

1. **Consulta:** `cambio.py` faz uma requisição à AwesomeAPI para obter as cotações das oito moedas.
2. **Coleta:** `coleta.py` extrai e organiza os valores de compra, venda, variação percentual e data da cotação.
3. **Armazenamento:** `banco.py` salva os registros no SQLite, evitando duplicações conforme a lógica implementada.
4. **Visualização:** `app.py` lê os registros com Pandas e exibe os resultados no Streamlit.
5. **Atualização:** o dashboard realiza novas consultas automaticamente em intervalos de aproximadamente 60 segundos enquanto estiver em execução.

> **Observação:** uma nova consulta não significa necessariamente um novo registro. Se a API ainda não publicou uma cotação diferente, a aplicação pode informar `Novos registros: 0`.

## 📊 Funcionalidades

- Consulta de cotações de oito moedas em relação ao real.
- Exibição da última cotação disponível para cada moeda.
- Indicadores de compra e variação percentual informada pela API.
- Tabela consolidada com valores de compra, venda, variação, data e situação da cotação.
- Identificação de cotações recentes ou antigas com base no horário registrado.
- Filtro para consultar o histórico de uma moeda específica.
- Gráfico de evolução cambial quando há registros suficientes.
- Consulta ao histórico armazenado no SQLite.
- Exportação dos dados históricos em arquivo CSV.

## 🚀 Como executar

### 1. Pré-requisitos

- Python instalado.
- VS Code ou outro editor de código.
- Conexão com a internet para consultar a API.

### 2. Abrir a pasta do projeto

No terminal, acesse a pasta que contém os arquivos Python.

### 3. Criar e ativar um ambiente virtual (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as bibliotecas

```powershell
python -m pip install requests pandas streamlit
```

O módulo `sqlite3` faz parte da biblioteca padrão do Python e não precisa ser instalado separadamente.

### 5. Iniciar o dashboard

```powershell
python -m streamlit run app.py
```

Abra o endereço local indicado pelo Streamlit no terminal (normalmente `http://localhost:8501`).

## 🗄️ Banco de dados

O projeto utiliza um banco SQLite chamado `cambio360.db`, com a tabela `cotacoes`.

| Campo | Descrição |
|---|---|
| `id` | Identificador do registro |
| `moeda` | Código da moeda consultada |
| `compra` | Cotação de compra |
| `venda` | Cotação de venda |
| `variacao` | Variação percentual informada pela API |
| `data_cotacao` | Data e horário da cotação na fonte |
| `data_coleta` | Data e horário em que o sistema registrou a coleta |

## 🌐 Fonte dos dados

As cotações são obtidas por meio da **AwesomeAPI – API de Moedas**.

- Documentação: https://docs.awesomeapi.com.br/api-de-moedas
- Exemplo de consulta: https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL

As informações dependem da disponibilidade e da frequência de atualização da fonte. A aplicação **não prevê taxas de câmbio** e **não realiza operações financeiras**.

## 📚 Conhecimentos aplicados

- Requisições HTTP e leitura de respostas JSON.
- Organização do código em módulos Python.
- Conversão e tratamento de tipos de dados.
- Inserção e consulta de registros em SQLite.
- Manipulação de DataFrames com Pandas.
- Construção de indicadores, tabelas e gráficos com Streamlit.
- Tratamento de exceções e atualização periódica de dados.

## 📝 Considerações finais

O **CÂMBIO 360°** integra as etapas de obtenção, processamento, armazenamento e apresentação de dados em uma aplicação prática. O projeto demonstra como ferramentas de Python podem ser utilizadas para acompanhar informações cambiais e construir um histórico para análise.

**Projeto desenvolvido para fins acadêmicos.**
