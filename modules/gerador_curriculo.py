"""
Módulo responsável por gerar um currículo adaptado para a vaga.
"""

def montar_resumo_profissional(vaga, analise):
    """
    Cria um resumo profissional adaptado ao contexto da vaga.
    """
    cargo = vaga.get("cargo", "o cargo desejado")
    habilidades = analise.get("tecnicas_presentes", [])

    if habilidades:
        habilidades_texto = ", ".join(habilidades[:5])
        resumo = (
            f"Profissional com experiência em automação de processos, suporte operacional, "
            f"monitoramento de rotinas e atuação em ambientes corporativos. "
            f"Possui conhecimentos alinhados à vaga de {cargo}, com destaque para {habilidades_texto}. "
            f"Tem perfil analítico, boa comunicação, facilidade de adaptação e interesse em evolução contínua na área de tecnologia e dados."
        )
    else:
        resumo = (
            f"Profissional com experiência em automação de processos, suporte operacional e monitoramento de rotinas corporativas. "
            f"Possui perfil analítico, boa comunicação, facilidade de adaptação e interesse em atuar na posição de {cargo}, "
            f"contribuindo com organização, aprendizado contínuo e apoio a operações e tecnologia."
        )

    return resumo


def montar_competencias_relevantes(vaga, analise):
    """
    Monta a lista de competências mais relevantes para destacar no currículo.
    """
    competencias = []

    competencias.extend(analise.get("tecnicas_presentes", []))
    competencias.extend(analise.get("comportamentais_presentes", []))
    competencias.extend(analise.get("areas_presentes", []))

    # Remove duplicados preservando ordem
    competencias_unicas = []
    for item in competencias:
        if item not in competencias_unicas:
            competencias_unicas.append(item)

    if not competencias_unicas:
        competencias_unicas = [
            "automação de processos",
            "suporte operacional",
            "monitoramento de processos",
            "python",
            "sql",
            "power bi",
            "capacidade analítica",
            "comunicação"
        ]

    return competencias_unicas


def montar_experiencia_direcionada(vaga, analise):
    """
    Gera uma seção textual de experiência/entrega profissional com foco na vaga.
    """
    experiencias = []

    tecnicas = analise.get("tecnicas_presentes", [])
    comportamentais = analise.get("comportamentais_presentes", [])

    experiencias.append(
        "Atuação em rotinas operacionais e corporativas com foco em organização, suporte a processos e acompanhamento de atividades críticas."
    )

    if "automação" in tecnicas or "automacao" in tecnicas:
        experiencias.append(
            "Experiência com automação de processos e otimização de rotinas, buscando ganho de eficiência e redução de tarefas manuais."
        )

    if "python" in tecnicas:
        experiencias.append(
            "Conhecimento em Python para apoio em automações, tratamento de dados e melhoria de processos."
        )

    if "sql" in tecnicas:
        experiencias.append(
            "Conhecimento em SQL para consultas, organização e análise de informações em bases de dados."
        )

    if "power bi" in tecnicas:
        experiencias.append(
            "Conhecimento em Power BI para apoio na construção de relatórios e visualizações de dados."
        )

    if "monitoramento" in tecnicas:
        experiencias.append(
            "Vivência com monitoramento de rotinas e processos, com atenção a falhas, acompanhamento de execução e suporte operacional."
        )

    if "levantamento de requisitos" in tecnicas:
        experiencias.append(
            "Apoio no levantamento de requisitos e entendimento de demandas para melhoria de processos e soluções internas."
        )

    if "comunicação" in comportamentais or "comunicacao" in comportamentais:
        experiencias.append(
            "Boa comunicação para interação com áreas parceiras, entendimento de demandas e suporte no dia a dia operacional."
        )

    if "perfil analítico" in comportamentais or "perfil analitico" in comportamentais:
        experiencias.append(
            "Perfil analítico para identificar problemas, apoiar decisões e propor melhorias em processos."
        )

    if len(experiencias) <= 1:
        experiencias.append(
            "Experiência com suporte operacional, acompanhamento de processos e uso de ferramentas corporativas em ambiente de tecnologia."
        )

    return experiencias


def gerar_curriculo_adaptado(vaga, perfil_base, analise):
    """
    Gera um currículo adaptado em texto com foco ATS-friendly.

    Parâmetros:
        vaga (dict): Dados da vaga
        perfil_base (str): Texto do perfil-base
        analise (dict): Resultado da análise de aderência

    Retorno:
        str: Currículo adaptado em texto
    """
    cargo = vaga.get("cargo", "")
    empresa = vaga.get("empresa", "")

    resumo_profissional = montar_resumo_profissional(vaga, analise)
    competencias = montar_competencias_relevantes(vaga, analise)
    experiencias = montar_experiencia_direcionada(vaga, analise)

    curriculo = f"""
CURRÍCULO ADAPTADO

CARGO-ALVO
{cargo}

EMPRESA-ALVO
{empresa}

OBJETIVO PROFISSIONAL
Atuar em uma oportunidade alinhada ao cargo de {cargo}, contribuindo com conhecimentos em automação, suporte operacional, monitoramento de processos, análise de dados e ferramentas corporativas.

RESUMO PROFISSIONAL
{resumo_profissional}

COMPETÊNCIAS-CHAVE
{chr(10).join([f"- {item}" for item in competencias])}

EXPERIÊNCIA E QUALIFICAÇÕES RELEVANTES
{chr(10).join([f"- {item}" for item in experiencias])}

FERRAMENTAS E CONHECIMENTOS
- Python
- SQL
- Power BI
- Automação de processos
- Monitoramento operacional
- Suporte a processos
- Ferramentas corporativas
- Levantamento de requisitos
- Control-M

DIFERENCIAIS
- Capacidade analítica
- Boa comunicação
- Facilidade de adaptação
- Organização
- Interesse contínuo em desenvolvimento na área de tecnologia e dados
""".strip()

    return curriculo