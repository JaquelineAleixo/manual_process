import os
import sqlite3
import pandas as pd

def analyze_db(db_name, table_name):   # Função para analisar o banco de dados
    if not os.path.exists(db_name): # Verifica se o arquivo existe
        print(f"O arquivo de banco de dados {db_name} não foi encontrado.")
        return
    
    try:
        conn = sqlite3.connect(db_name) # Conecta ao banco de dados
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn) # Lê a tabela e armazena em um DataFrame
        conn.close()   # Fecha a conexão com o banco de dados
        
        if df.empty:   # Verifica se o DataFrame está vazio
            print(f"A tabela {table_name} no banco de dados {db_name} está vazia.") # Se estiver vazio, retorna
        else:  # Se não estiver vazio, imprime o DataFrame
            print(f"Dados do banco de dados {db_name}, tabela {table_name}:")
            print(df)  # Imprime o DataFrame
            
    except sqlite3.Error as e: # Se ocorrer um erro, imprime a mensagem de erro
        print(f"Ocorreu um erro ao acessar o banco de dados {db_name}: {e}") # Imprime a mensagem de erro

if __name__ == "__main__": # Se o programa for executado diretamente, executa o código abaixo
    analyze_db("test_db.sqlite", "test_table") # Chama a função para analisar o banco de dados de teste
    analyze_db("prod_db.sqlite", "prod_table") # Chama a função para analisar o banco de dados de produção
