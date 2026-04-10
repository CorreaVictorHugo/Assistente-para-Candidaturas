"""
Módulo responsável por exportações futuras do projeto.
"""

def exportar_texto(conteudo, caminho_arquivo):
    """
    Salva um conteúdo de texto em arquivo.

    Parâmetros:
        conteudo (str): Texto a ser salvo
        caminho_arquivo (str): Caminho do arquivo
    """
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)