"""
Módulo responsável por gerar mensagens de apresentação para recrutadores.
"""

def resumir_pontos_fortes(analise, limite=3):
    """
    Junta os principais pontos fortes técnicos e comportamentais
    em uma lista curta para usar na mensagem.
    """
    destaques = []

    destaques.extend(analise.get("tecnicas_presentes", []))
    destaques.extend(analise.get("comportamentais_presentes", []))

    # Remove duplicados preservando ordem
    destaques_unicos = []
    for item in destaques:
        if item not in destaques_unicos:
            destaques_unicos.append(item)

    return destaques_unicos[:limite]


def definir_tom_mensagem(score):
    """
    Define o tom da mensagem com base no score.
    """
    if score >= 80:
        return "alta"
    elif score >= 60:
        return "moderada"
    return "baixa"


def gerar_mensagem_linkedin(vaga, analise):
    """
    Gera uma mensagem para contato com recrutador no LinkedIn.
    """
    empresa = vaga.get("empresa", "empresa")
    cargo = vaga.get("cargo", "cargo")
    score = analise.get("score", 0)

    destaques = resumir_pontos_fortes(analise)
    tom = definir_tom_mensagem(score)

    if destaques:
        texto_destaques = ", ".join(destaques)
    else:
        texto_destaques = "automação de processos, suporte operacional e capacidade analítica"

    if tom == "alta":
        mensagem = f"""
Olá! Tudo bem?

Vi a oportunidade para {cargo} na {empresa} e identifiquei uma boa aderência entre os requisitos da vaga e minha experiência profissional.

Tenho atuação em rotinas operacionais, automação de processos e suporte a ambientes corporativos, com conhecimentos em {texto_destaques}. Acredito que meu perfil pode contribuir de forma positiva para a posição.

Gostaria de me colocar à disposição para conversar e apresentar melhor minha experiência.

Obrigado pela atenção!
""".strip()

    elif tom == "moderada":
        mensagem = f"""
Olá! Tudo bem?

Vi a vaga para {cargo} na {empresa} e gostei bastante da proposta da oportunidade.

Minha experiência está relacionada a automação de processos, monitoramento operacional, suporte a rotinas corporativas e conhecimentos em {texto_destaques}. Acredito que meu perfil tem boa proximidade com a posição e que posso agregar valor com aprendizado rápido e dedicação.

Fico à disposição para conversar, caso faça sentido para vocês.

Obrigado pela atenção!
""".strip()

    else:
        mensagem = f"""
Olá! Tudo bem?

Vi a oportunidade para {cargo} na {empresa} e gostaria de demonstrar meu interesse na posição.

Tenho experiência em automação de processos, suporte operacional e atividades corporativas, além de conhecimentos em {texto_destaques}. Mesmo que eu ainda esteja em desenvolvimento em alguns pontos da vaga, acredito que meu perfil analítico, minha adaptação e minha vontade de aprender podem ser diferenciais.

Fico à disposição para me apresentar melhor.

Obrigado pela atenção!
""".strip()

    return mensagem


def gerar_texto_apresentacao_curta(vaga, analise):
    """
    Gera um texto curto de apresentação profissional.
    """
    cargo = vaga.get("cargo", "a vaga")
    destaques = resumir_pontos_fortes(analise)

    if destaques:
        texto_destaques = ", ".join(destaques)
    else:
        texto_destaques = "automação, suporte operacional e análise de processos"

    texto_curto = (
        f"Profissional com experiência em automação de processos, monitoramento operacional e suporte corporativo, "
        f"com conhecimentos em {texto_destaques}. Tenho interesse em atuar na posição de {cargo}, "
        f"contribuindo com organização, capacidade analítica e evolução contínua."
    )

    return texto_curto


def gerar_mensagem_recrutador(vaga, analise):
    """
    Retorna os dois formatos de mensagem:
    - mensagem principal para LinkedIn/e-mail
    - apresentação curta
    """
    return {
        "mensagem_linkedin": gerar_mensagem_linkedin(vaga, analise),
        "texto_curto": gerar_texto_apresentacao_curta(vaga, analise)
    }