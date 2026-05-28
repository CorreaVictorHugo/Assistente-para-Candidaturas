"""
Módulo responsável por receber e organizar as informações da vaga.
Nesta etapa, além de organizar os campos básicos, ele também:
- limpa o texto
- extrai palavras-chave
- identifica competências técnicas e comportamentais
"""

import re


# Lista simples de palavras irrelevantes para não poluir as palavras-chave
PALAVRAS_IGNORADAS = {
    "a", "o", "e", "de", "da", "do", "das", "dos", "em", "para", "com", "sem",
    "um", "uma", "uns", "umas", "no", "na", "nos", "nas", "por", "ou", "ao",
    "aos", "às", "as", "os", "que", "ser", "ter", "como", "mais", "menos",
    "se", "sua", "seu", "suas", "seus", "sobre", "até", "entre", "não"
}


# Palavras e termos técnicos que fazem sentido para o seu perfil-alvo
HABILIDADES_TECNICAS_MAPA = [
    "python",
    "sql",
    "power bi",
    "power query",
    "dax",
    "excel",
    "automação",
    "automacao",
    "etl",
    "elt",
    "airflow",
    "apache airflow",
    "postgresql",
    "postgres",
    "mysql",
    "sql server",
    "dashboard",
    "dashboards",
    "relatório",
    "relatorios",
    "relatórios",
    "kpi",
    "kpis",
    "indicadores",
    "visualização de dados",
    "visualizacao de dados",
    "data visualization",
    "dados",
    "análise de dados",
    "analise de dados",
    "analytics",
    "business intelligence",
    "bi",
    "engenharia de dados",
    "pipeline",
    "pipelines",
    "pipeline de dados",
    "pipelines de dados",
    "tratamento de dados",
    "modelagem de dados",
    "data warehouse",
    "databricks",
    "spark",
    "spark sql",
    "pyspark",
    "delta lake",
    "azure databricks",
    "azure data lake",
    "git",
    "github",
    "suporte técnico",
    "suporte tecnico",
    "monitoramento",
    "infraestrutura",
    "control-m",
    "api",
    "cloud",
    "aws",
    "azure",
    "linux",
    "windows server",
    "banco de dados",
    "processos",
    "levantamento de requisitos",
    "service now",
    "jira"
]


HABILIDADES_COMPORTAMENTAIS_MAPA = [
    "comunicação",
    "comunicacao",
    "proatividade",
    "organização",
    "organizacao",
    "trabalho em equipe",
    "perfil analítico",
    "perfil analitico",
    "capacidade analítica",
    "capacidade analitica",
    "adaptabilidade",
    "flexibilidade",
    "atenção aos detalhes",
    "atencao aos detalhes",
    "resolução de problemas",
    "resolucao de problemas"
]


AREAS_INTERESSE_MAPA = [
    "dados",
    "automação",
    "automacao",
    "suporte",
    "infraestrutura",
    "operações",
    "operacoes",
    "tecnologia",
    "analytics",
    "bi",
    "business intelligence",
    "engenharia de dados",
    "inteligência de negócios",
    "inteligencia de negocios"
]


TIPOS_VAGA_MAPA = {
    "Analista de Dados": [
        "analista de dados", "data analyst", "análise de dados", "analise de dados",
        "sql", "power bi", "dashboard", "indicadores", "kpi"
    ],
    "BI": [
        "bi", "business intelligence", "power bi", "dax", "power query",
        "dashboard", "relatórios", "relatorios", "indicadores"
    ],
    "Engenharia de Dados": [
        "engenharia de dados", "data engineer", "etl", "elt", "airflow",
        "pipeline", "pipelines", "postgresql", "spark", "databricks"
    ],
    "Automação e Processos": [
        "automação", "automacao", "processos", "python", "rotinas",
        "monitoramento", "control-m"
    ],
    "Suporte com Dados": [
        "suporte", "suporte técnico", "suporte tecnico", "monitoramento",
        "operações", "operacoes", "dados", "sql"
    ]
}


SENIORIDADE_MAPA = {
    "Estágio": ["estágio", "estagio", "intern", "trainee"],
    "Júnior": ["júnior", "junior", "jr", "assistente", "auxiliar"],
    "Pleno": ["pleno", "mid-level", "analista pleno"],
    "Sênior": ["sênior", "senior", "sr", "especialista", "lead"]
}


def limpar_texto(texto):
    """
    Limpa e padroniza o texto:
    - converte para minúsculas
    - remove espaços extras
    - mantém letras, números, hífen e acentos
    """
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def tokenizar_texto(texto):
    """
    Separa o texto em palavras simples.
    """
    return re.findall(r"\b[\w\-]+\b", texto.lower())


def extrair_palavras_chave(texto, limite=20):
    """
    Extrai palavras mais relevantes do texto, ignorando termos muito comuns.
    """
    tokens = tokenizar_texto(texto)
    frequencia = {}

    for token in tokens:
        if token in PALAVRAS_IGNORADAS:
            continue
        if len(token) <= 2:
            continue
        frequencia[token] = frequencia.get(token, 0) + 1

    palavras_ordenadas = sorted(
        frequencia.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [palavra for palavra, _ in palavras_ordenadas[:limite]]


def identificar_termos(texto, mapa_termos):
    """
    Procura termos relevantes dentro do texto.
    """
    encontrados = []

    for termo in mapa_termos:
        if termo in texto:
            encontrados.append(termo)

    return sorted(list(set(encontrados)))


def classificar_por_mapa(texto, mapa):
    """
    Classifica o texto usando contagem simples de termos por categoria.
    """
    pontuacoes = {}

    for categoria, termos in mapa.items():
        pontuacoes[categoria] = sum(1 for termo in termos if termo in texto)

    categoria_mais_provavel = max(pontuacoes, key=pontuacoes.get)

    if pontuacoes[categoria_mais_provavel] == 0:
        return "Não classificada"

    return categoria_mais_provavel


def organizar_vaga(empresa, cargo, link, descricao):
    """
    Organiza e enriquece os dados da vaga.

    Parâmetros:
        empresa (str): Nome da empresa
        cargo (str): Nome do cargo
        link (str): Link da vaga
        descricao (str): Texto completo da vaga

    Retorno:
        dict: Dados organizados e enriquecidos
    """
    descricao_limpa = limpar_texto(descricao)

    vaga = {
        "empresa": empresa.strip(),
        "cargo": cargo.strip(),
        "link": link.strip(),
        "descricao_original": descricao.strip(),
        "descricao_limpa": descricao_limpa,
        "palavras_chave": extrair_palavras_chave(descricao_limpa),
        "habilidades_tecnicas": identificar_termos(descricao_limpa, HABILIDADES_TECNICAS_MAPA),
        "habilidades_comportamentais": identificar_termos(descricao_limpa, HABILIDADES_COMPORTAMENTAIS_MAPA),
        "areas_interesse": identificar_termos(descricao_limpa, AREAS_INTERESSE_MAPA),
        "tipo_vaga": classificar_por_mapa(descricao_limpa + " " + cargo.lower(), TIPOS_VAGA_MAPA),
        "senioridade": classificar_por_mapa(descricao_limpa + " " + cargo.lower(), SENIORIDADE_MAPA)
    }

    return vaga
