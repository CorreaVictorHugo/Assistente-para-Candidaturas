import re # Biblioteca para expressões regulares
import requests # Requests biblioteca para fazer requisições HTTP
import trafilatura # Trafilatura biblioteca para extração avançada de texto de páginas web
from bs4 import BeautifulSoup # BS4 biblioteca para extrair texto de HTML


def baixar_html(url):
    """
    Faz o download do HTML da página.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    resposta = requests.get(url, headers=headers, timeout=15)
    resposta.raise_for_status()
    return resposta.text


def extrair_texto_com_trafilatura(html, url):
    """
    Tenta extrair o texto principal da página usando trafilatura.
    """
    texto = trafilatura.extract(html, url=url)

    if texto:
        return texto.strip()

    return ""


def extrair_texto_com_bs4(html):
    """
    Fallback simples com BeautifulSoup, caso trafilatura não consiga.
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    texto = soup.get_text(separator="\n")
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]

    return "\n".join(linhas).strip()


def limpar_texto_extraido(texto):
    """
    Limpa o texto extraído removendo ruídos comuns de páginas.
    """
    palavras_ruido = [
        "cookies", "política de privacidade", "privacy policy",
        "aceitar", "continuar", "cadastre-se", "login",
        "termos de uso", "all rights reserved", "©",
        "clique aqui", "saiba mais", "menu", "home",
        "voltar", "compartilhar", "seguir", "inscreva-se"
    ]

    linhas = texto.split("\n")
    linhas_limpas = []

    for linha in linhas:
        linha = linha.strip()

        if len(linha) < 20:
            continue

        if any(palavra in linha.lower() for palavra in palavras_ruido):
            continue

        linhas_limpas.append(linha)

    linhas_unicas = list(dict.fromkeys(linhas_limpas))

    texto_final = "\n".join(linhas_unicas)
    texto_final = re.sub(r"\n{2,}", "\n\n", texto_final)

    return texto_final.strip()


def separar_secoes_vaga(texto):
    """
    Tenta separar o texto da vaga em seções mais úteis.
    """
    secoes = {
        "descricao": [],
        "responsabilidades": [],
        "requisitos": [],
        "diferenciais": [],
        "beneficios": []
    }

    marcadores = {
        "responsabilidades": [
            "responsabilidades", "atividades", "o que você vai fazer",
            "principais atividades", "atribuições"
        ],
        "requisitos": [
            "requisitos", "qualificações", "o que esperamos",
            "pré-requisitos", "conhecimentos necessários"
        ],
        "diferenciais": [
            "diferenciais", "será um diferencial", "desejável",
            "desejaveis", "desejável ter"
        ],
        "beneficios": [
            "benefícios", "beneficios", "oferecemos",
            "o que oferecemos"
        ]
    }

    secao_atual = "descricao"
    linhas = texto.split("\n")

    for linha in linhas:
        linha_limpa = linha.strip()
        linha_lower = linha_limpa.lower()

        mudou_secao = False

        for nome_secao, palavras_chave in marcadores.items():
            if any(palavra in linha_lower for palavra in palavras_chave):
                secao_atual = nome_secao
                mudou_secao = True
                break

        if mudou_secao:
            continue

        if linha_limpa:
            secoes[secao_atual].append(linha_limpa)

    return {
        chave: "\n".join(valor).strip()
        for chave, valor in secoes.items()
    }


def montar_texto_organizado(secoes):
    """
    Monta um texto final mais organizado a partir das seções.
    """
    partes = []

    if secoes["descricao"]:
        partes.append("DESCRIÇÃO DA VAGA\n" + secoes["descricao"])

    if secoes["responsabilidades"]:
        partes.append("RESPONSABILIDADES\n" + secoes["responsabilidades"])

    if secoes["requisitos"]:
        partes.append("REQUISITOS\n" + secoes["requisitos"])

    if secoes["diferenciais"]:
        partes.append("DIFERENCIAIS\n" + secoes["diferenciais"])

    if secoes["beneficios"]:
        partes.append("BENEFÍCIOS\n" + secoes["beneficios"])

    return "\n\n".join(partes).strip()


def ler_vaga_por_link(url):
    """
    Lê uma vaga a partir de uma URL e retorna o texto extraído e organizado.
    """
    html = baixar_html(url)

    texto = extrair_texto_com_trafilatura(html, url)

    if not texto:
        texto = extrair_texto_com_bs4(html)

    texto = limpar_texto_extraido(texto)
    secoes = separar_secoes_vaga(texto)
    texto_organizado = montar_texto_organizado(secoes)

    return texto_organizado if texto_organizado else texto