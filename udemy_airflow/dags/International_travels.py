from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator

from include.international_travels.tasks import _calcular_periodo_mandatos, _extrair_dados_api

qtd_mandatos = 5
serie_id = 22760

@dag(
    start_date=datetime(2025,4,1),
    schedule='@daily',
    catchup=False,
    tags=['Viagens Internacionais Gov Br']
)
def Viagens_Internacionais():
    retorna_mandatos = PythonOperator(
        task_id='retorna_mandatos',
        python_callable=_calcular_periodo_mandatos,
        op_kwargs={'qtd_mandatos': qtd_mandatos}        
    )   
    
    busca_viagens = PythonOperator(
        task_id='busca_viagens',
        python_callable=_extrair_dados_api,
        op_kwargs={'serie_id': serie_id, 'data_inicial': '{{ti.xcom_pull(task_ids="retorna_mandatos")[0]}}', 'data_final':'{{ti.xcom_pull(task_ids="retorna_mandatos")[1]}}'}
    )


    retorna_mandatos >> busca_viagens

Viagens_Internacionais()