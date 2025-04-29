import requests
from datetime import datetime



def _calcular_periodo_mandatos(qtd_mandatos):
    """
    Calcula a data inicial e final considerando os últimos 'qtd_mandatos' mandatos presidenciais.
    
    Retorna:
        (data_inicial: str, data_final: str) no formato 'dd/mm/yyyy'
    """
    ano_atual = datetime.today().year
    ano_mandato_atual = ano_atual - (ano_atual % 4) + 3  # Último ano de mandato vigente

    ano_final = ano_mandato_atual + 1  # Mandato termina em 31/12 do último ano
    ano_inicial = ano_final - (qtd_mandatos * 4)

    data_inicial = f"01/01/{ano_inicial}"
    data_final = f"31/12/{ano_final}"
    return data_inicial, data_final

def _extrair_dados_api(serie_id, data_inicial, data_final):
    """
    Extrai dados da API do Banco Central do Brasil no intervalo informado.
    
    Parâmetros:
        serie_id: int ou str - ID da série
        data_inicial: str - data inicial no formato dd/mm/yyyy
        data_final: str - data final no formato dd/mm/yyyy
        
    Retorna:
        Lista de registros extraídos (formato JSON)
    """
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados"
        f"?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    )
    resposta = requests.get(url)
    resposta.raise_for_status()  # Lança erro se a requisição falhar
    return resposta.json()

# def inserir_dados_postgres(dados, conexao_params, nome_tabela, schema):
#     """
#     Insere uma lista de registros no banco de dados PostgreSQL.

#     Parâmetros:
#         dados (list): Lista de dicionários com os dados extraídos da API.
#         conexao_params (dict): Parâmetros de conexão com o banco de dados, contendo:
#             - host (str)
#             - port (int)
#             - database (str)
#             - user (str)
#             - password (str)
#         nome_tabela (str): Nome da tabela de destino no banco de dados.

#     Retorna:
#         None
#     """
#     if not dados:
#         print("Nenhum dado para inserir.")
#         return

#     # Conectando ao banco de dados
#     conexao = Postgres(**conexao_params)

#     try:
#         # Criação da tabela (se necessário)
#         create_table_query = f"""
#             CREATE TABLE IF NOT EXISTS {schema}.{nome_tabela} (
#                 data DATE,
#                 valor NUMERIC
#             );
#         """
#         aql.run(create_table_query, conn_id='postgres_conn_id')

#         # Preparar dados para inserção
#         registros = [
#             (registro['data'], float(registro['valor'].replace(',', '.')))
#             for registro in dados
#         ]

#         # Inserir os dados em lote utilizando o comando de inserção SQL
#         insert_query = f"""
#             INSERT INTO {schema}.{nome_tabela} (data, valor)
#             VALUES (%s, %s)
#         """

#         aql.run(insert_query, parameters=registros, conn_id='postgres_conn_id')
#         print(f"{len(registros)} registros inseridos na tabela '{nome_tabela}'.")

#     except Exception as e:
#         print(f"Erro ao inserir dados: {e}")

#     finally:
#         # A conexão é gerenciada automaticamente pelo Astro, então não há necessidade de fechá-la explicitamente.
#         pass



# if __name__ == "__main__":
#     conexao_params_Postgres = {
#     "host": "localhost",
#     "port": 5432,
#     "database": "postgres",
#     "user": "postgres",
#     "password": "postgres"
#     }

#     serie_id = 22760  # Série desejada
#     data_inicial, data_final = calcular_periodo_mandatos()

#     print(f"Extraindo dados do período de {data_inicial} até {data_final}...")

#     dados = extrair_dados_api(serie_id, data_inicial, data_final)

#     # Exemplo de saída
#     print(f"{len(dados)} registros extraídos.")
#     print(dados[:5])  # Imprime apenas os 5 primeiros registros

#     # Inserção no banco
#     inserir_dados_postgres(dados, conexao_params_Postgres, "serie_temporal", "gov_br")
