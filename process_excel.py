import pandas as pd
import logging
import sqlite3

def process_excel_file(file_name, expected_columns, validation_rules=None): # validation_rules é um dicionário com as regras de validação para cada coluna
    logging.basicConfig(filename='process_excel.log', level=logging.INFO) # Cria um arquivo de log
    
    try:
        df = pd.read_excel(file_name) # Lê o arquivo Excel e armazena em um DataFrame
        df_original = df.copy(deep=True)   # Cria uma cópia do DataFrame original

        for col in expected_columns: # Verifica se todas as colunas esperadas estão presentes no arquivo
            if col not in df.columns: # Se a coluna não estiver presente, adiciona-a com valores NULL
                df[col] = None
                logging.warning(f"Coluna {col} não encontrada. Adicionada como NULL.")
        
        df.replace(["SEM INFORMAÇÃO", "SEM INFO"], None, inplace=True) # Substitui os valores "SEM INFORMAÇÃO" e "SEM INFO" por NULL
        df['PLACA_ANTIGA'] = df['PLACA_ANTIGA'].str.replace(r'[^a-zA-Z0-9]', '', regex=True) # Remove caracteres especiais da coluna PLACA_ANTIGA
        df.loc[df['PLACA_ANTIGA'].apply(lambda x: len(str(x)) != 7), 'PLACA_ANTIGA'] = None # Substitui valores com menos de 7 caracteres por NULL
        
        if validation_rules:
            for col, rule in validation_rules.items(): # Itera sobre as regras de validação
                df[col] = pd.to_numeric(df[col], errors='coerce') # Converte a coluna para numérica
                df.loc[~df[col].apply(rule), col] = None # Substitui os valores que não atendem a regra por NULL
                logging.info(f"Regras de validação aplicadas na coluna {col}.")

        df_errors = df_original[df.isnull().any(axis=1)] # Cria um DataFrame com as linhas que possuem valores NULL

        conn_test = sqlite3.connect("test_db.sqlite")   # Cria uma conexão com o banco de dados de teste
        df.to_sql("test_table", conn_test, if_exists="replace", index=False)    # Importa o DataFrame para o banco de dados de teste
        conn_test.close()  # Fecha a conexão com o banco de dados de teste
        logging.info("Teste de importação realizado com sucesso.")
        
        conn_prod = sqlite3.connect("prod_db.sqlite")  # Cria uma conexão com o banco de dados de produção
        df.to_sql("prod_table", conn_prod, if_exists="replace", index=False)   # Importa o DataFrame para o banco de dados de produção
        conn_prod.close()  # Fecha a conexão com o banco de dados de produção
        logging.info("Dados importados para o sistema de produção.")
        
        if not df_errors.empty: # Se houver linhas com erros, cria um arquivo Excel com elas
            df_errors.to_excel("linhas_com_erros.xlsx", index=False) # Cria um arquivo Excel com as linhas que possuem valores NULL
            logging.info("Arquivo de erros criado: linhas_com_erros.xlsx")
        
        df_corrected = df.copy(deep=True) # Criar uma cópia do DataFrame antes de remover linhas com erros

        df.dropna(inplace=True) # Remove as linhas que possuem valores NULL

        df_corrected.to_excel("dados_corrigidos.xlsx", index=False) # Cria um arquivo Excel com os dados corrigidos
        logging.info("Arquivo Excel com dados corrigidos criado: dados_corrigidos.xlsx")

        return df # Retorna o DataFrame com os dados corrigidos
    
    except Exception as e: # Se ocorrer algum erro, exibe uma mensagem de erro e retorna None
        logging.error(f"Erro ao processar o arquivo: {e}")
        return None

if __name__ == "__main__":
    expected_columns = ['PLACA_ANTIGA', 'CMT', 'NR_PASSAGEIROS', 'BUSCA'] # Colunas esperadas no arquivo
    validation_rules = { # Regras de validação para cada coluna
        'CMT': lambda x: x >= 0, # Regra para a coluna CMT: valores devem ser maiores ou iguais a 0
        'NR_PASSAGEIROS': lambda x: x >= 0 # Regra para a coluna NR_PASSAGEIROS: valores devem ser maiores ou iguais a 0
    } 
    
    df = process_excel_file("teste-ti-processamento_fornecedor_fora_do_ar.xlsx", expected_columns, validation_rules) # Chama a função process_excel_file e armazena o resultado em um DataFrame
