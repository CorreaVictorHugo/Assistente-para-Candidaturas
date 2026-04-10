"""
Módulo responsável por buscar vagas e padronizar os resultados.

Nesta primeira versão, a busca é simulada para validar o fluxo
da aplicação antes de integrar fontes reais.
"""


def buscar_vagas(palavra_chave="", localizacao=""):
    """
    Retorna uma lista de vagas simuladas com base em filtros simples.

    Parâmetros:
        palavra_chave (str): termo principal da busca
        localizacao (str): cidade, estado ou modalidade

    Retorno:
        list[dict]: lista de vagas padronizadas
    """
    vagas_exemplo = [
        {
            "empresa": "Tech Solutions",
            "cargo": "Analista de Dados Júnior",
            "link": "https://exemplo.com/vaga-analista-dados-jr",
            "localizacao": "São Paulo - SP",
            "fonte": "Busca interna simulada",
            "resumo": (
                "Atuação com análise de dados, criação de relatórios, "
                "Power BI, SQL e apoio à tomada de decisão."
            )
        },
        {
            "empresa": "Data Flow",
            "cargo": "Assistente de Automação",
            "link": "https://exemplo.com/vaga-automacao",
            "localizacao": "Remoto",
            "fonte": "Busca interna simulada",
            "resumo": (
                "Apoio em automação de rotinas, monitoramento operacional, "
                "Python e melhoria de processos."
            )
        },
        {
            "empresa": "Infra Corp",
            "cargo": "Analista de Suporte Operacional",
            "link": "https://exemplo.com/vaga-suporte-operacional",
            "localizacao": "Barueri - SP",
            "fonte": "Busca interna simulada",
            "resumo": (
                "Suporte a processos corporativos, acompanhamento de rotinas, "
                "monitoramento e atuação com ferramentas internas."
            )
        },
        {
            "empresa": "Insight BI",
            "cargo": "Analista de BI Júnior",
            "link": "https://exemplo.com/vaga-bi-jr",
            "localizacao": "São Paulo - SP",
            "fonte": "Busca interna simulada",
            "resumo": (
                "Construção de dashboards, análise de indicadores, SQL, "
                "Power BI e suporte ao negócio."
            )
        }
    ]

    palavra_chave = palavra_chave.strip().lower()
    localizacao = localizacao.strip().lower()

    resultados_filtrados = []

    for vaga in vagas_exemplo:
        texto_busca = " ".join([
            vaga["empresa"],
            vaga["cargo"],
            vaga["localizacao"],
            vaga["resumo"]
        ]).lower()

        atende_palavra = not palavra_chave or palavra_chave in texto_busca
        atende_localizacao = not localizacao or localizacao in texto_busca

        if atende_palavra and atende_localizacao:
            resultados_filtrados.append(vaga)

    return resultados_filtrados