"""
Módulo responsável por analisar o grau de aderência entre a vaga
e o perfil-base do usuário.
"""

import re


def normalizar_texto(texto):
    """
    Coloca o texto em minúsculas e remove espaços extras.
    """
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def verificar_itens_presentes(itens_vaga, perfil_base):
    """
    Verifica quais itens da vaga aparecem no perfil-base.

    Parâmetros:
        itens_vaga (list): Lista de itens encontrados na vaga
        perfil_base (str): Texto do perfil-base

    Retorno:
        tuple:
            - presentes (list)
            - ausentes (list)
    """
    presentes = []
    ausentes = []

    perfil_normalizado = normalizar_texto(perfil_base)

    for item in itens_vaga:
        if item.lower() in perfil_normalizado:
            presentes.append(item)
        else:
            ausentes.append(item)

    return presentes, ausentes


def calcular_score(total_itens, total_presentes):
    """
    Calcula um score percentual simples.
    """
    if total_itens == 0:
        return 0

    score = (total_presentes / total_itens) * 100
    return round(score)


def gerar_recomendacoes(lacunas_tecnicas, lacunas_comportamentais, lacunas_areas):
    """
    Gera recomendações simples com base nas lacunas encontradas.
    """
    recomendacoes = []

    if lacunas_tecnicas:
        recomendacoes.append(
            "Vale reforçar ou estudar as competências técnicas mencionadas na vaga: "
            + ", ".join(lacunas_tecnicas) + "."
        )

    if lacunas_comportamentais:
        recomendacoes.append(
            "Na candidatura, destaque exemplos práticos ligados a competências comportamentais como: "
            + ", ".join(lacunas_comportamentais) + "."
        )

    if lacunas_areas:
        recomendacoes.append(
            "Adapte o currículo para mostrar maior proximidade com estas áreas da vaga: "
            + ", ".join(lacunas_areas) + "."
        )

    if not recomendacoes:
        recomendacoes.append(
            "Seu perfil tem boa aderência à vaga. Foque em personalizar o currículo e a mensagem de apresentação."
        )

    return recomendacoes


def analisar_aderencia(vaga, perfil_base):
    """
    Analisa a aderência entre a vaga e o perfil-base.

    Parâmetros:
        vaga (dict): Dados organizados da vaga
        perfil_base (str): Conteúdo do perfil-base

    Retorno:
        dict: Resultado da análise
    """
    tecnicas_vaga = vaga.get("habilidades_tecnicas", [])
    comportamentais_vaga = vaga.get("habilidades_comportamentais", [])
    areas_vaga = vaga.get("areas_interesse", [])

    tecnicas_presentes, tecnicas_ausentes = verificar_itens_presentes(tecnicas_vaga, perfil_base)
    comport_presentes, comport_ausentes = verificar_itens_presentes(comportamentais_vaga, perfil_base)
    areas_presentes, areas_ausentes = verificar_itens_presentes(areas_vaga, perfil_base)

    total_itens_vaga = len(tecnicas_vaga) + len(comportamentais_vaga) + len(areas_vaga)
    total_presentes = len(tecnicas_presentes) + len(comport_presentes) + len(areas_presentes)

    score = calcular_score(total_itens_vaga, total_presentes)

    pontos_fortes = []
    if tecnicas_presentes:
        pontos_fortes.append("Competências técnicas aderentes: " + ", ".join(tecnicas_presentes) + ".")
    if comport_presentes:
        pontos_fortes.append("Competências comportamentais aderentes: " + ", ".join(comport_presentes) + ".")
    if areas_presentes:
        pontos_fortes.append("Áreas de interesse alinhadas: " + ", ".join(areas_presentes) + ".")

    lacunas = []
    if tecnicas_ausentes:
        lacunas.append("Competências técnicas a desenvolver: " + ", ".join(tecnicas_ausentes) + ".")
    if comport_ausentes:
        lacunas.append("Competências comportamentais pouco evidentes no perfil-base: " + ", ".join(comport_ausentes) + ".")
    if areas_ausentes:
        lacunas.append("Áreas da vaga pouco representadas no perfil-base: " + ", ".join(areas_ausentes) + ".")

    recomendacoes = gerar_recomendacoes(
        tecnicas_ausentes,
        comport_ausentes,
        areas_ausentes
    )

    resultado = {
        "score": score,
        "tecnicas_presentes": tecnicas_presentes,
        "tecnicas_ausentes": tecnicas_ausentes,
        "comportamentais_presentes": comport_presentes,
        "comportamentais_ausentes": comport_ausentes,
        "areas_presentes": areas_presentes,
        "areas_ausentes": areas_ausentes,
        "pontos_fortes": pontos_fortes,
        "lacunas": lacunas,
        "recomendacoes": recomendacoes
    }

    return resultado