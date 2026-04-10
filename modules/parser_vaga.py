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
    "excel",
    "automação",
    "automacao",
    "etl",
    "dashboard",
    "dados",
    "análise de dados",
    "analise de dados",
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
    "bi"
]


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
        "areas_interesse": identificar_termos(descricao_limpa, AREAS_INTERESSE_MAPA)
    }

    return vaga