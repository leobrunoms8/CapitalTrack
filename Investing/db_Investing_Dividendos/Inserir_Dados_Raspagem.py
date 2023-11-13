from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Raspagem(Base):
    __tablename__ = 'raspagem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    campo = Column(String(255), nullable=False)
    simbolo = Column(String(255), nullable=False)
    nome_da_empresa = Column(String(255), nullable=False)
    data_ex = Column(String(255), nullable=False)
    valor_dividendo = Column(String(255), nullable=False)
    frequencia = Column(String(255), nullable=False)
    data_pagamento = Column(String(255), nullable=False)
    percentual_acao = Column(String(255), nullable=False)

class InsercaoDados:
    def __init__(self, dados):
        self.dados = dados

    def inserir_dados(self):
        # Configurar a conexão com o banco de dados MySQL
        engine = create_engine('mysql+mysqlconnector://developer:Leo140707@localhost/RaspagemPuraDeDados', echo=True)
        
        # Criar uma sessão para interagir com o banco de dados
        Session = sessionmaker(bind=engine)
        session = Session()

        # Iterar sobre a lista de listas e inserir os dados na tabela
        for dados_lista in self.dados:
            # Verificar se a lista tem pelo menos 8 elementos
            if len(dados_lista) >= 8:
                nova_raspagem = Raspagem(
                    campo=dados_lista[0],
                    simbolo=dados_lista[1],
                    nome_da_empresa=dados_lista[2],
                    data_ex=dados_lista[3],
                    valor_dividendo=dados_lista[4],
                    frequencia=dados_lista[5],
                    data_pagamento=dados_lista[6],
                    percentual_acao=dados_lista[7]
                )
                session.add(nova_raspagem)
            else:
                print(f"A lista {dados_lista} não possui todos os elementos necessários.")

        # Commit das alterações no banco de dados
        session.commit()

        # Fechar a sessão
        session.close()