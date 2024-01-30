import mysql.connector

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="developer",
        password="Leo140707",
        database="RaspagemPuraDeDados"
    )

    cursor = conexao.cursor()
    cursor.execute("SHOW TABLES")
    tabelas = [tabela[0] for tabela in cursor.fetchall()]

    for tabela in tabelas:
        try:
            cursor = conexao.cursor()
            query = f"ALTER TABLE `{tabela}` ADD COLUMN `dividendo_acao` FLOAT"
            cursor.execute(query)
            conexao.commit()
            print(f"Coluna 'moeda' adicionada com sucesso à tabela '{tabela}'.")
        except mysql.connector.Error as erro:
            print("Erro ao adicionar coluna:", erro)
finally:
    if conexao:
        conexao.close()
