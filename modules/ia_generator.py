import google.generativeai as genai

# Configure sua API KEY aqui (troque depois por variável de ambiente)
genai.configure(api_key="AIzaSyAD8g-7HubkNaBQ38FF2cWw4i1Xh7Y66U8") 


def gerar_texto(prompt):
    """
    Envia um prompt para o Gemini e retorna a resposta.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


def extrair_bloco(texto, inicio, fim=None):
    """
    Extrai um bloco entre marcadores de início e fim.
    """
    try:
        parte = texto.split(inicio, 1)[1]
        if fim:
            parte = parte.split(fim, 1)[0]
        return parte.strip()
    except IndexError:
        return ""


def gerar_conteudo_completo_com_ia(vaga, perfil_base):
    """
    Gera currículo, mensagem e apresentação curta em uma única chamada.
    """
    prompt = f"""
Você é um especialista em recrutamento.

IMPORTANTE:
- Não invente experiências.
- Não exagere habilidades.
- Use apenas o perfil real fornecido.
- Adapte a linguagem à vaga, mas sem alterar a veracidade.
- Se alguma habilidade da vaga não estiver no perfil, não afirme experiência nela.

PERFIL REAL:
{perfil_base}

VAGA:
Empresa: {vaga["empresa"]}
Cargo: {vaga["cargo"]}
Descrição: {vaga["descricao_original"]}

TAREFA:
Gere os 3 conteúdos abaixo, exatamente nesta estrutura:

[CURRICULO]
Escreva um currículo adaptado, profissional, claro, direto e realista.

[MENSAGEM]
Escreva uma mensagem curta e profissional para recrutador no LinkedIn ou e-mail.

[APRESENTACAO]
Escreva uma apresentação curta, objetiva e profissional.
"""

    resposta = gerar_texto(prompt)

    curriculo = extrair_bloco(resposta, "[CURRICULO]", "[MENSAGEM]")
    mensagem = extrair_bloco(resposta, "[MENSAGEM]", "[APRESENTACAO]")
    apresentacao = extrair_bloco(resposta, "[APRESENTACAO]")

    return {
        "curriculo": curriculo,
        "mensagem_linkedin": mensagem,
        "texto_curto": apresentacao
    }