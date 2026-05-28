"""
Módulo responsável por buscar vagas e padronizar os resultados.

A busca local usa uma lista simulada para apoiar o fluxo do app.
Quando não houver vaga local suficiente, o módulo também gera atalhos
para buscas externas em sites de emprego.
"""

import re
import unicodedata
from urllib.parse import quote_plus

import requests


REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"


VAGAS_EXEMPLO = [
    {
        "empresa": "Tech Solutions",
        "cargo": "Analista de Dados Júnior",
        "link": "",
        "localizacao": "São Paulo - SP",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Atuação com análise de dados, criação de relatórios, "
            "Power BI, SQL e apoio à tomada de decisão."
        )
    },
    {
        "empresa": "Data Flow",
        "cargo": "Assistente de Automação de Dados",
        "link": "",
        "localizacao": "Remoto",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Apoio em automação de rotinas, tratamento de dados, "
            "Python, SQL e melhoria de processos."
        )
    },
    {
        "empresa": "Infra Corp",
        "cargo": "Analista de Suporte Operacional com Dados",
        "link": "",
        "localizacao": "Barueri - SP",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Suporte a processos corporativos, acompanhamento de rotinas, "
            "monitoramento, SQL e atuação com ferramentas internas."
        )
    },
    {
        "empresa": "Insight BI",
        "cargo": "Analista de BI Júnior",
        "link": "",
        "localizacao": "São Paulo - SP",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Construção de dashboards, análise de indicadores, SQL, "
            "Power BI, DAX e suporte ao negócio."
        )
    },
    {
        "empresa": "Cloud Data Lab",
        "cargo": "Engenheiro de Dados Júnior",
        "link": "",
        "localizacao": "Remoto",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Projetos com ETL, Python, SQL, Azure, Databricks, PySpark, "
            "Spark SQL e Delta Lake."
        )
    },
    {
        "empresa": "Finance Analytics",
        "cargo": "Analista de Dados Financeiros",
        "link": "",
        "localizacao": "Híbrido - São Paulo",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Análise de DRE, indicadores financeiros, Power BI, SQL, "
            "modelagem analítica e comunicação com áreas de negócio."
        )
    },
    {
        "empresa": "Rio Data Hub",
        "cargo": "Analista de Dados Júnior",
        "link": "",
        "localizacao": "Rio de Janeiro - RJ",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Análise de dados, SQL, Power BI, construção de dashboards, "
            "indicadores operacionais e apoio a áreas de negócio."
        )
    },
    {
        "empresa": "Carioca BI",
        "cargo": "Analista de BI Júnior",
        "link": "",
        "localizacao": "Híbrido - Rio de Janeiro",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Desenvolvimento de relatórios, dashboards em Power BI, DAX, "
            "Power Query, análise de indicadores e apresentações executivas."
        )
    },
    {
        "empresa": "RJ Analytics Finance",
        "cargo": "Analista de Dados Financeiros",
        "link": "",
        "localizacao": "Rio de Janeiro - RJ",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Atuação com DRE, indicadores financeiros, SQL, Power BI, "
            "tratamento de dados e suporte à tomada de decisão."
        )
    },
    {
        "empresa": "DataOps Rio",
        "cargo": "Assistente de Dados e Automação",
        "link": "",
        "localizacao": "Rio de Janeiro - RJ",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Automação de processos com Python, manipulação de dados, "
            "consultas SQL, monitoramento de rotinas e melhoria operacional."
        )
    },
    {
        "empresa": "Cloud Rio Tech",
        "cargo": "Engenheiro de Dados Júnior",
        "link": "",
        "localizacao": "Híbrido - Rio de Janeiro",
        "fonte": "Busca interna simulada",
        "resumo": (
            "Projetos de dados com Azure, Databricks, PySpark, Spark SQL, "
            "Delta Lake, ETL e pipelines de dados."
        )
    }
]


SINONIMOS = {
    "dados": ["analytics", "data", "bi", "indicadores", "relatorios", "dashboards"],
    "analista": ["assistente", "junior", "jr"],
    "bi": ["business intelligence", "power bi", "dashboard", "dashboards"],
    "engenharia": ["engenheiro", "engineer", "etl", "pipeline", "pipelines"],
    "automacao": ["automação", "python", "processos", "rotinas"],
    "remoto": ["home office", "remote", "teletrabalho"],
    "sao paulo": ["sp", "são paulo"],
    "rio de janeiro": ["rio", "rj", "rio janeiro"],
    "rj": ["rio", "rio de janeiro", "rio janeiro"],
    "hibrido": ["híbrido", "hybrid"],
    "presencial": ["onsite", "escritorio", "escritório"],
    "databricks": ["azure databricks", "pyspark", "spark", "spark sql", "delta lake"],
}


TRADUCOES_BUSCA_REMOTIVE = {
    "analista dados": "data analyst",
    "analista de dados": "data analyst",
    "engenheiro dados": "data engineer",
    "engenheiro de dados": "data engineer",
    "engenharia dados": "data engineer",
    "engenharia de dados": "data engineer",
    "cientista dados": "data scientist",
    "cientista de dados": "data scientist",
    "dados": "data",
    "remoto": "remote",
}


TERMOS_DADOS = [
    "data", "dados", "analytics", "analyst", "engineer", "bi",
    "business intelligence", "sql", "python", "etl", "pipeline",
    "power bi", "databricks", "spark", "pyspark", "delta lake",
    "dashboard", "reporting", "visualization"
]


FONTES_EXTERNAS = [
    {
        "empresa": "LinkedIn",
        "fonte": "Busca externa",
        "url": "https://www.linkedin.com/jobs/search/?keywords={query}&location={location}"
    },
    {
        "empresa": "Indeed",
        "fonte": "Busca externa",
        "url": "https://br.indeed.com/jobs?q={query}&l={location}"
    },
    {
        "empresa": "Glassdoor",
        "fonte": "Busca externa",
        "url": "https://www.glassdoor.com.br/Vaga/jobs.htm?sc.keyword={query}&locT=N&locId=36"
    },
    {
        "empresa": "Gupy",
        "fonte": "Busca externa",
        "url": "https://portal.gupy.io/job-search/term={query}"
    },
    {
        "empresa": "Remotar",
        "fonte": "Busca externa",
        "url": "https://remotar.com.br/search/jobs?q={query}"
    },
]


def limpar_html(texto):
    """
    Remove tags HTML simples da descrição retornada por APIs de vaga.
    """
    texto = texto or ""
    texto = re.sub(r"<br\s*/?>", "\n", texto, flags=re.IGNORECASE)
    texto = re.sub(r"</p>", "\n", texto, flags=re.IGNORECASE)
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = re.sub(r"&nbsp;", " ", texto)
    texto = re.sub(r"&amp;", "&", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def normalizar_texto(texto):
    """
    Remove acentos, deixa minúsculo e normaliza espaços.
    """
    texto = texto or ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def tokenizar(texto):
    """
    Quebra um texto em tokens úteis para busca.
    """
    texto = normalizar_texto(texto)
    return [token for token in re.findall(r"\b[\w\-]+\b", texto) if len(token) > 1]


def expandir_termos(termos):
    """
    Expande termos digitados com sinônimos comuns no contexto de vagas.
    """
    termos_expandidos = set(termos)
    texto_termos = " ".join(termos)

    for termo_base, equivalentes in SINONIMOS.items():
        termo_base_normalizado = normalizar_texto(termo_base)
        equivalentes_normalizados = [normalizar_texto(item) for item in equivalentes]

        if termo_base_normalizado in texto_termos or any(item in texto_termos for item in equivalentes_normalizados):
            termos_expandidos.add(termo_base_normalizado)
            termos_expandidos.update(tokenizar(" ".join(equivalentes)))

    return termos_expandidos


def traduzir_busca_remotive(palavra_chave):
    """
    Traduz buscas comuns em português para termos melhores na API da Remotive.
    """
    texto = normalizar_texto(palavra_chave)

    if texto in TRADUCOES_BUSCA_REMOTIVE:
        return TRADUCOES_BUSCA_REMOTIVE[texto]

    return palavra_chave.strip() or "data analyst"


def pontuar_resultado_api(resultado, palavra_chave):
    """
    Pontua resultados reais para reduzir vagas fora do alvo.
    """
    titulo = normalizar_texto(resultado.get("cargo", ""))
    corpo = normalizar_texto(" ".join([
        resultado.get("empresa", ""),
        resultado.get("localizacao", ""),
        resultado.get("resumo", ""),
        resultado.get("descricao", "")
    ]))
    texto_completo = f"{titulo} {corpo}"

    if not any(termo in texto_completo for termo in TERMOS_DADOS):
        return 0

    termos_originais = tokenizar(palavra_chave)
    termos_expandidos = expandir_termos(termos_originais)

    busca_normalizada = normalizar_texto(palavra_chave)

    if "data analyst" in busca_normalizada:
        termos_titulo = ["data", "analyst", "analytics", "bi", "reporting", "business intelligence"]
        if not any(termo in titulo for termo in termos_titulo):
            return 0

    if "data engineer" in busca_normalizada:
        termos_titulo = [
            "data engineer", "data engineering", "etl", "analytics engineer",
            "bi engineer", "databricks", "spark", "pipeline"
        ]
        if not any(termo in titulo for termo in termos_titulo):
            return 0

    if "data scientist" in busca_normalizada:
        termos_titulo = ["data", "scientist", "machine learning", "ml", "ai"]
        if not any(termo in titulo for termo in termos_titulo):
            return 0

    pontuacao = 0

    for termo in termos_originais:
        if termo in titulo:
            pontuacao += 4
        elif termo in corpo:
            pontuacao += 1

    for termo in termos_expandidos:
        if termo in termos_originais:
            continue

        if termo in titulo:
            pontuacao += 2
        elif termo in corpo:
            pontuacao += 0.5

    return pontuacao


def pontuar_vaga(vaga, palavra_chave, localizacao):
    """
    Calcula uma pontuação simples por termos encontrados.
    """
    texto_vaga = normalizar_texto(" ".join([
        vaga["empresa"],
        vaga["cargo"],
        vaga["localizacao"],
        vaga["resumo"]
    ]))

    termos_busca = expandir_termos(tokenizar(palavra_chave))
    termos_localizacao = expandir_termos(tokenizar(localizacao))

    if not termos_busca and not termos_localizacao:
        return 1

    pontos_busca = sum(1 for termo in termos_busca if termo in texto_vaga)

    if termos_busca and pontos_busca == 0:
        return 0

    if termos_localizacao and not localizacao_compativel(texto_vaga, localizacao):
        return 0

    pontos_localizacao = 1 if termos_localizacao else 0

    return pontos_busca + pontos_localizacao


def gerar_buscas_externas(palavra_chave, localizacao):
    """
    Gera atalhos para o usuário abrir buscas reais em sites de vagas.
    """
    query = palavra_chave.strip() or "analista de dados junior"
    location = localizacao.strip() or "Rio de Janeiro"

    query_url = quote_plus(query)
    location_url = quote_plus(location)

    resultados = []

    for fonte in FONTES_EXTERNAS:
        resultados.append({
            "empresa": fonte["empresa"],
            "cargo": f"Buscar: {query}",
            "link": fonte["url"].format(query=query_url, location=location_url),
            "localizacao": location,
            "fonte": fonte["fonte"],
            "resumo": (
                "Atalho para busca real. Abra o link, escolha uma vaga e cole "
                "o link ou a descrição no formulário do app."
            )
        })

    return resultados


def localizacao_pede_remoto(localizacao):
    """
    Verifica se a busca faz sentido para fontes remotas.
    """
    if not localizacao.strip():
        return True

    texto = normalizar_texto(localizacao)
    termos_remotos = ["remoto", "remote", "home office", "teletrabalho", "brasil"]
    return any(termo in texto for termo in termos_remotos)


def localizacao_compativel(texto_vaga, localizacao):
    """
    Filtra localização evitando que RJ traga SP e vice-versa.
    """
    texto_local = normalizar_texto(localizacao)

    if not texto_local:
        return True

    if any(termo in texto_local for termo in ["rio", "rj", "rio de janeiro", "rio janeiro"]):
        return any(termo in texto_vaga for termo in ["rio de janeiro", " rj", "remoto", "hibrido - rio"])

    if any(termo in texto_local for termo in ["sao paulo", "são paulo", "sp"]):
        return any(termo in texto_vaga for termo in ["sao paulo", " sp", "remoto", "hibrido - sao paulo"])

    termos_localizacao = expandir_termos(tokenizar(localizacao))
    return any(termo in texto_vaga for termo in termos_localizacao)


def buscar_vagas_remotive(palavra_chave="", localizacao="", limite=12):
    """
    Busca vagas reais na API pública da Remotive.

    A Remotive retorna vagas remotas e exige que o link original seja mantido.
    """
    if not localizacao_pede_remoto(localizacao):
        return []

    termo_busca = traduzir_busca_remotive(palavra_chave)

    try:
        resposta = requests.get(
            REMOTIVE_API_URL,
            params={
                "search": termo_busca,
                "limit": limite
            },
            timeout=12
        )
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception:
        return []

    resultados = []

    for vaga in dados.get("jobs", []):
        descricao_limpa = limpar_html(vaga.get("description", ""))
        localizacao_vaga = vaga.get("candidate_required_location") or "Remoto"
        salario = vaga.get("salary") or ""
        categoria = vaga.get("category") or ""

        resumo_partes = []
        if categoria:
            resumo_partes.append(f"Categoria: {categoria}.")
        if salario:
            resumo_partes.append(f"Salário: {salario}.")
        if descricao_limpa:
            resumo_partes.append(descricao_limpa[:350] + ("..." if len(descricao_limpa) > 350 else ""))

        resultado = {
            "empresa": vaga.get("company_name", "Empresa não informada"),
            "cargo": vaga.get("title", "Cargo não informado"),
            "link": vaga.get("url", ""),
            "localizacao": localizacao_vaga,
            "fonte": "Remotive API",
            "resumo": " ".join(resumo_partes).strip() or "Vaga remota encontrada na Remotive.",
            "descricao": descricao_limpa[:8000],
        }

        pontuacao = pontuar_resultado_api(resultado, termo_busca)

        if pontuacao >= 2:
            resultado["pontuacao_busca"] = pontuacao
            resultados.append(resultado)

    resultados = sorted(
        resultados,
        key=lambda resultado: resultado["pontuacao_busca"],
        reverse=True
    )

    for resultado in resultados:
        resultado.pop("pontuacao_busca", None)

    return resultados


def gerar_link_busca_vaga(cargo, localizacao):
    """
    Gera um link de busca real para uma sugestão local simulada.
    """
    query_url = quote_plus(cargo)
    location_url = quote_plus(localizacao or "Brasil")
    return f"https://www.linkedin.com/jobs/search/?keywords={query_url}&location={location_url}"


def buscar_vagas(palavra_chave="", localizacao=""):
    """
    Retorna vagas reais, sugestões locais compatíveis e atalhos externos.
    """
    vagas_reais = buscar_vagas_remotive(palavra_chave, localizacao)
    vagas_pontuadas = []

    for vaga in VAGAS_EXEMPLO:
        pontuacao = pontuar_vaga(vaga, palavra_chave, localizacao)

        if pontuacao > 0:
            vaga_com_score = vaga.copy()
            vaga_com_score["pontuacao_busca"] = pontuacao
            vaga_com_score["link"] = gerar_link_busca_vaga(
                vaga_com_score["cargo"],
                vaga_com_score["localizacao"]
            )
            vagas_pontuadas.append(vaga_com_score)

    vagas_pontuadas = sorted(
        vagas_pontuadas,
        key=lambda vaga: vaga["pontuacao_busca"],
        reverse=True
    )

    for vaga in vagas_pontuadas:
        vaga.pop("pontuacao_busca", None)

    return vagas_reais + vagas_pontuadas + gerar_buscas_externas(palavra_chave, localizacao)
