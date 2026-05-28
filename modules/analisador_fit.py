"""
Módulo responsável por analisar o grau de aderência entre a vaga
e o perfil-base do usuário.
"""

import re


EQUIVALENCIAS = {
    "power bi": ["dashboard", "dashboards", "bi", "business intelligence", "visualização de dados", "visualizacao de dados", "relatórios", "relatorios"],
    "sql": ["postgresql", "postgres", "banco de dados", "sql server", "mysql"],
    "python": ["automação", "automacao", "etl", "pipeline", "pipelines", "tratamento de dados"],
    "etl": ["airflow", "apache airflow", "pipeline", "pipelines", "engenharia de dados"],
    "databricks": ["azure databricks", "spark", "spark sql", "pyspark", "delta lake"],
    "azure": ["azure databricks", "azure data lake", "cloud"],
    "análise de dados": ["analise de dados", "analytics", "indicadores", "kpi", "kpis", "dados"],
}


PESOS_ANALISE = {
    "tecnicas": 0.60,
    "areas": 0.20,
    "comportamentais": 0.10,
    "evidencias": 0.10,
}


def normalizar_texto(texto):
    """
    Coloca o texto em minúsculas e remove espaços extras.
    """
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def termo_presente_no_perfil(item, perfil_normalizado):
    """
    Verifica presença literal e equivalências relevantes para vagas de dados.
    """
    item_normalizado = item.lower()

    if item_normalizado in perfil_normalizado:
        return True

    for termo_base, equivalentes in EQUIVALENCIAS.items():
        grupo = [termo_base] + equivalentes

        if item_normalizado in grupo:
            return any(termo in perfil_normalizado for termo in grupo)

    return False


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
        if termo_presente_no_perfil(item, perfil_normalizado):
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


def calcular_score_categoria(total_itens, total_presentes):
    """
    Calcula score percentual de uma categoria.
    """
    if total_itens == 0:
        return 0

    return total_presentes / total_itens


def calcular_score_ponderado(tecnicas, comportamentais, areas, evidencias):
    """
    Calcula score ponderado para priorizar requisitos técnicos da vaga.
    """
    score_tecnico = calcular_score_categoria(len(tecnicas[0]) + len(tecnicas[1]), len(tecnicas[0]))
    score_comportamental = calcular_score_categoria(
        len(comportamentais[0]) + len(comportamentais[1]),
        len(comportamentais[0])
    )
    score_areas = calcular_score_categoria(len(areas[0]) + len(areas[1]), len(areas[0]))
    score_evidencias = min(len(evidencias) / 2, 1)

    score_final = (
        score_tecnico * PESOS_ANALISE["tecnicas"]
        + score_areas * PESOS_ANALISE["areas"]
        + score_comportamental * PESOS_ANALISE["comportamentais"]
        + score_evidencias * PESOS_ANALISE["evidencias"]
    )

    return round(score_final * 100)


def extrair_projetos_relevantes(vaga, perfil_base):
    """
    Encontra projetos do perfil que tenham relação com termos da vaga.
    """
    projetos = []
    blocos = re.split(r"\n### ", perfil_base)
    termos_vaga = set(
        vaga.get("habilidades_tecnicas", [])
        + vaga.get("areas_interesse", [])
        + vaga.get("palavras_chave", [])
    )

    for bloco in blocos:
        if "Evidência:" not in bloco:
            continue

        bloco_normalizado = normalizar_texto(bloco)
        termos_encontrados = [
            termo for termo in termos_vaga
            if termo and termo.lower() in bloco_normalizado
        ]

        if not termos_encontrados:
            continue

        linhas = [linha.strip() for linha in bloco.strip().splitlines() if linha.strip()]
        titulo = linhas[0].replace("### ", "").strip()
        link = ""

        for linha in linhas:
            if linha.startswith("- Evidência:"):
                link = linha.replace("- Evidência:", "").strip()
                break

        projetos.append({
            "titulo": titulo,
            "link": link,
            "termos": sorted(set(termos_encontrados))
        })

    projetos_ordenados = sorted(
        projetos,
        key=lambda projeto: len(projeto.get("termos", [])),
        reverse=True
    )

    return projetos_ordenados[:3]


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

    projetos_relevantes = extrair_projetos_relevantes(vaga, perfil_base)

    score = calcular_score_ponderado(
        (tecnicas_presentes, tecnicas_ausentes),
        (comport_presentes, comport_ausentes),
        (areas_presentes, areas_ausentes),
        projetos_relevantes
    )

    pontos_fortes = []
    if tecnicas_presentes:
        pontos_fortes.append("Competências técnicas aderentes: " + ", ".join(tecnicas_presentes) + ".")
    if comport_presentes:
        pontos_fortes.append("Competências comportamentais aderentes: " + ", ".join(comport_presentes) + ".")
    if areas_presentes:
        pontos_fortes.append("Áreas de interesse alinhadas: " + ", ".join(areas_presentes) + ".")
    if projetos_relevantes:
        pontos_fortes.append(
            "Projetos que sustentam a candidatura: "
            + ", ".join([projeto["titulo"] for projeto in projetos_relevantes]) + "."
        )

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
        "projetos_relevantes": projetos_relevantes,
        "tipo_vaga": vaga.get("tipo_vaga", "Não classificada"),
        "senioridade": vaga.get("senioridade", "Não classificada"),
        "pontos_fortes": pontos_fortes,
        "lacunas": lacunas,
        "recomendacoes": recomendacoes
    }

    return resultado
