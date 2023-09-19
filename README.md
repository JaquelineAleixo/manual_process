# Processamento de Arquivos Excel e Análise de Banco de Dados

Este repositório contém scripts para processar arquivos Excel e analisar bancos de dados SQLite gerados a partir desses arquivos.

## Requisitos

- **Python 3.x**
- **Pandas**
- **SQLite3**

## Uso

### Processamento de Arquivos Excel
   
1. Execute o script `process_excel.py` para processar o arquivo e gerar o banco de dados.

    ```bash
    python process_excel.py
    ```

    Isso irá gerar dois bancos de dados SQLite (`test_db.sqlite` e `prod_db.sqlite`) e dois arquivos Excel (`linhas_com_erros.xlsx` e `dados_corrigidos.xlsx`).

### Análise de Banco de Dados

> **Nota**: Execute este script somente após ter executado `process_excel.py`.

1. Execute o script `analyze_dbs.py` para analisar os bancos de dados gerados.

    ```bash
    python analyze_dbs.py
    ```

