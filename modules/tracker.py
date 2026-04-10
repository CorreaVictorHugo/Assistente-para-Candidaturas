"""
Módulo responsável pelo controle e histórico de candidaturas.
"""

import sqlite3
from datetime import datetime


CAMINHO_BANCO = "data/vagas.db"


def conectar_banco():
    """
    Cria a conexão com o banco SQLite.
    """
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela_candidaturas():
    """
    Cria a tabela de candidaturas caso ela ainda não exista.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            cargo TEXT NOT NULL,
            link TEXT,
            score INTEGER,
            data_candidatura TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_candidatura(vaga, score):
    """
    Salva uma candidatura no banco de dados.

    Parâmetros:
        vaga (dict): Dados organizados da vaga
        score (int): Score de aderência
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    data_candidatura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO candidaturas (empresa, cargo, link, score, data_candidatura)
        VALUES (?, ?, ?, ?, ?)
    """, (
        vaga["empresa"],
        vaga["cargo"],
        vaga["link"],
        score,
        data_candidatura
    ))

    conexao.commit()
    conexao.close()


def listar_candidaturas():
    """
    Retorna todas as candidaturas salvas, da mais recente para a mais antiga.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, empresa, cargo, link, score, data_candidatura
        FROM candidaturas
        ORDER BY id DESC
    """)

    resultados = cursor.fetchall()
    conexao.close()

    candidaturas = []
    for item in resultados:
        candidaturas.append({
            "id": item[0],
            "empresa": item[1],
            "cargo": item[2],
            "link": item[3],
            "score": item[4],
            "data_candidatura": item[5]
        })

    return candidaturas

def deletar_candidatura(id_candidatura):
    """
    Remove uma candidatura do banco pelo ID.

    Parâmetros:
        id_candidatura (int): ID da candidatura
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM candidaturas
        WHERE id = ?
    """, (id_candidatura,))

    conexao.commit()
    conexao.close()