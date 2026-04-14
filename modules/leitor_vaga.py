import re
import requests
import trafilatura
from bs4 import BeautifulSoup


def limpar_texto(texto):
    """
    Faz uma limpeza simples no texto extraído.
    """
    if not texto:
        return ""

    texto = texto.replace("\xa0", " ")
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    return texto.strip()


def extrair_empresa_e_cargo_do_titulo(titulo):
    """
    Tenta identificar cargo e empresa a partir do título da página.
    Exemplo:
    'Analista de Dados - Empresa X'
    """
    empresa = ""
    cargo = ""

    if not titulo:
        return empresa, cargo

    separadores = [" - ", " | ", " — ", " – "]

    for separador in separadores:
        if separador in titulo:
            partes = titulo.split(separador)
            if len(partes) >= 2:
                cargo = partes[0].strip()
                empresa = partes[1].strip()
                return empresa, cargo

    cargo = titulo.strip()
    return empresa, cargo


def extrair_metadados(soup):
    """
    Tenta extrair informações da página por metatags.
    """
    dados = {
        "empresa": "",
        "cargo": "",
        "descricao": ""
    }

    titulo = ""
    if soup.title and soup.title.string:
        titulo = soup.title.string.strip()

    empresa_titulo, cargo_titulo = extrair_empresa_e_cargo_do_titulo(titulo)

    if cargo_titulo:
        dados["cargo"] = cargo_titulo

    if empresa_titulo:
        dados["empresa"] = empresa_titulo

    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description and meta_description.get("content"):
        dados["descricao"] = meta_description.get("content").strip()

    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        og_texto = og_title.get("content").strip()
        empresa_og, cargo_og = extrair_empresa_e_cargo_do_titulo(og_texto)

        if not dados["cargo"] and cargo_og:
            dados["cargo"] = cargo_og

        if not dados["empresa"] and empresa_og:
            dados["empresa"] = empresa_og

    og_description = soup.find("meta", attrs={"property": "og:description"})
    if og_description and og_description.get("content") and not dados["descricao"]:
        dados["descricao"] = og_description.get("content").strip()

    return dados


def ler_vaga_do_link(url):
    """
    Lê o conteúdo de uma vaga a partir de uma URL e tenta extrair:
    - empresa
    - cargo
    - descrição
    """
    dados = {
        "empresa": "",
        "cargo": "",
        "descricao": "",
        "descricao_original": "",
        "link": url
    }

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

        resposta = requests.get(url, headers=headers, timeout=15)
        resposta.raise_for_status()

        html = resposta.text
        soup = BeautifulSoup(html, "html.parser")

        metadados = extrair_metadados(soup)

        if metadados["empresa"]:
            dados["empresa"] = metadados["empresa"]

        if metadados["cargo"]:
            dados["cargo"] = metadados["cargo"]

        texto_extraido = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        if texto_extraido:
            texto_extraido = limpar_texto(texto_extraido)
            dados["descricao"] = texto_extraido
            dados["descricao_original"] = texto_extraido
        else:
            texto_fallback = soup.get_text(separator="\n")
            texto_fallback = limpar_texto(texto_fallback)
            dados["descricao"] = texto_fallback[:8000]
            dados["descricao_original"] = texto_fallback[:8000]

        if not dados["descricao"] and metadados["descricao"]:
            dados["descricao"] = limpar_texto(metadados["descricao"])
            dados["descricao_original"] = limpar_texto(metadados["descricao"])

        return dados

    except Exception as erro:
        return {
            "empresa": "",
            "cargo": "",
            "descricao": "",
            "descricao_original": "",
            "link": url,
            "erro": str(erro)
        }