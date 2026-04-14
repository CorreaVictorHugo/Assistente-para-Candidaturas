import streamlit as st
import pandas as pd
from modules.leitor_vaga import ler_vaga_do_link
from modules.buscador_vagas import buscar_vagas
from modules.ia_generator import gerar_conteudo_completo_com_ia
from modules.parser_vaga import organizar_vaga
from modules.analisador_fit import analisar_aderencia
from modules.gerador_curriculo import gerar_curriculo_adaptado
from modules.gerador_mensagem import gerar_mensagem_recrutador
from modules.tracker import (
    criar_tabela_candidaturas,
    salvar_candidatura,
    listar_candidaturas,
    deletar_candidatura
)


def carregar_perfil_base(caminho_arquivo):
    """
    Lê o arquivo de perfil-base e retorna seu conteúdo em texto.
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def interpretar_score(score):
    """
    Retorna uma interpretação textual do score.
    """
    if score >= 80:
        return "Alta compatibilidade"
    elif score >= 60:
        return "Compatibilidade moderada"
    return "Compatibilidade baixa"


def mostrar_score_em_destaque(score):
    """
    Mostra o score em formato visual.
    """
    interpretacao = interpretar_score(score)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric("Score de aderência", f"{score}%")

    with col2:
        if score >= 80:
            st.success(interpretacao)
        elif score >= 60:
            st.warning(interpretacao)
        else:
            st.error(interpretacao)


def exibir_lista_titulo_itens(titulo, itens, mensagem_vazia):
    """
    Exibe uma lista simples com título.
    """
    st.subheader(titulo)

    if itens:
        for item in itens:
            st.write(f"- {item}")
    else:
        st.write(mensagem_vazia)


def inicializar_session_state():
    """
    Inicializa as variáveis do session_state.
    """
    if "empresa_input" not in st.session_state:
        st.session_state["empresa_input"] = ""

    if "cargo_input" not in st.session_state:
        st.session_state["cargo_input"] = ""

    if "link_input" not in st.session_state:
        st.session_state["link_input"] = ""

    if "descricao_vaga" not in st.session_state:
        st.session_state["descricao_vaga"] = ""

    if "resultados_busca" not in st.session_state:
        st.session_state["resultados_busca"] = []

    if "busca_palavra_chave" not in st.session_state:
        st.session_state["busca_palavra_chave"] = ""

    if "busca_localizacao" not in st.session_state:
        st.session_state["busca_localizacao"] = ""


def main():
    st.set_page_config(
        page_title="Assistente de Candidaturas com IA",
        layout="wide"
    )

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1500px;
                padding-top: 1.8rem;
                padding-left: 1.5rem;
                padding-right: 1.5rem;
                padding-bottom: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    criar_tabela_candidaturas()
    inicializar_session_state()

    st.title("Assistente de Candidaturas com IA")

    st.markdown(
        """
        Esta aplicação ajuda no processo de candidatura a vagas, permitindo:
        - analisar aderência com base no seu perfil
        - gerar score de compatibilidade
        - montar currículo adaptado
        - criar mensagem para recrutador
        - registrar histórico local de candidaturas
        """
    )

    # =========================================================
    # BUSCA DE VAGAS
    # =========================================================
    st.subheader("Buscar vagas")

    col_busca_input_1, col_busca_input_2 = st.columns(2)

    with col_busca_input_1:
        palavra_chave_busca = st.text_input(
            "Palavra-chave da busca",
            key="busca_palavra_chave"
        )

    with col_busca_input_2:
        localizacao_busca = st.text_input(
            "Localização da busca",
            key="busca_localizacao"
        )

    col_busca_1, col_busca_2 = st.columns(2)

    with col_busca_1:
        if st.button("Buscar vagas", use_container_width=True, key="btn_buscar_vagas"):
            resultados = buscar_vagas(
                palavra_chave=palavra_chave_busca,
                localizacao=localizacao_busca
            )
            st.session_state["resultados_busca"] = resultados
            st.rerun()

    with col_busca_2:
        if st.button("Limpar busca", use_container_width=True, key="btn_limpar_busca"):
            st.session_state["resultados_busca"] = []
            st.session_state["busca_palavra_chave"] = ""
            st.session_state["busca_localizacao"] = ""
            st.rerun()

    if st.session_state["resultados_busca"]:
        st.write("Resultados encontrados:")

        for i, vaga_encontrada in enumerate(st.session_state["resultados_busca"]):
            with st.container():
                st.markdown(f"**Cargo:** {vaga_encontrada['cargo']}")
                st.markdown(f"**Empresa:** {vaga_encontrada['empresa']}")
                st.markdown(f"**Localização:** {vaga_encontrada['localizacao']}")
                st.markdown(f"**Fonte:** {vaga_encontrada['fonte']}")
                st.markdown(f"**Resumo:** {vaga_encontrada['resumo']}")
                st.markdown(f"**Link:** [Abrir vaga]({vaga_encontrada['link']})")

                if st.button("Selecionar vaga", key=f"selecionar_vaga_{i}"):
                    st.session_state["empresa_input"] = vaga_encontrada["empresa"]
                    st.session_state["cargo_input"] = vaga_encontrada["cargo"]
                    st.session_state["link_input"] = vaga_encontrada["link"]
                    st.success("Vaga selecionada e campos preenchidos.")
                    st.rerun()

                st.divider()

    # =========================================================
    # FORMULÁRIO DA VAGA
    # =========================================================
    st.subheader("Preencha os dados da vaga")

    # Container dos campos para aparecer antes visualmente
    container_campos_vaga = st.container()

    # Botões ficam no código antes da renderização real dos campos
    # para evitar erro de session_state, mas visualmente os campos
    # continuam aparecendo primeiro.
    col_btn_1, col_btn_2, col_btn_3, col_btn_4 = st.columns(4)

    with col_btn_1:
        if st.button(
            "Preencher dados pelo link",
            use_container_width=True,
            key="btn_preencher_link"
        ):
            link_atual = st.session_state.get("link_input", "").strip()

            if not link_atual:
                st.warning("Informe um link antes de tentar ler a vaga.")
            else:
                try:
                    dados_vaga = ler_vaga_do_link(link_atual)

                    if dados_vaga.get("empresa"):
                        st.session_state["empresa_input"] = dados_vaga["empresa"]

                    if dados_vaga.get("cargo"):
                        st.session_state["cargo_input"] = dados_vaga["cargo"]

                    if dados_vaga.get("descricao_original"):
                        st.session_state["descricao_vaga"] = dados_vaga["descricao_original"]
                    elif dados_vaga.get("descricao"):
                        st.session_state["descricao_vaga"] = dados_vaga["descricao"]

                    if dados_vaga.get("erro"):
                        st.warning(
                            "A vaga foi lida parcialmente. Revise empresa, cargo e descrição antes de continuar."
                        )
                    else:
                        st.success("Campos preenchidos automaticamente pelo link.")

                    st.rerun()

                except Exception as erro:
                    st.error(f"Não foi possível ler a vaga pelo link. Erro: {erro}")

    with col_btn_2:
        if st.button(
            "Buscar só descrição",
            use_container_width=True,
            key="btn_buscar_descricao"
        ):
            link_atual = st.session_state.get("link_input", "").strip()

            if not link_atual:
                st.warning("Informe um link antes de tentar ler a vaga.")
            else:
                try:
                    dados_vaga = ler_vaga_do_link(link_atual)

                    if dados_vaga.get("descricao_original"):
                        st.session_state["descricao_vaga"] = dados_vaga["descricao_original"]
                    elif dados_vaga.get("descricao"):
                        st.session_state["descricao_vaga"] = dados_vaga["descricao"]

                    if dados_vaga.get("erro"):
                        st.warning("Não foi possível extrair tudo, mas tentei carregar a descrição.")
                    else:
                        st.success("Descrição carregada a partir do link.")

                    st.rerun()

                except Exception as erro:
                    st.error(f"Não foi possível ler a vaga pelo link. Erro: {erro}")

    with col_btn_3:
        if st.button(
            "Limpar descrição",
            use_container_width=True,
            key="btn_limpar_descricao"
        ):
            st.session_state["descricao_vaga"] = ""
            st.rerun()

    with col_btn_4:
        if st.button(
            "Limpar dados da vaga",
            use_container_width=True,
            key="btn_limpar_dados_vaga"
        ):
            st.session_state["empresa_input"] = ""
            st.session_state["cargo_input"] = ""
            st.session_state["link_input"] = ""
            st.session_state["descricao_vaga"] = ""
            st.rerun()

    with container_campos_vaga:
        empresa = st.text_input("Empresa", key="empresa_input")
        cargo = st.text_input("Cargo", key="cargo_input")
        link = st.text_input("Link da vaga", key="link_input")
        descricao = st.text_area(
            "Descrição da vaga",
            height=350,
            key="descricao_vaga"
        )

    st.markdown("---")

    usar_ia = st.checkbox("Usar IA para gerar currículo e mensagem", value=True)

    if st.button("Analisar vaga", use_container_width=True, key="btn_analisar_vaga"):
        empresa = st.session_state.get("empresa_input", "").strip()
        cargo = st.session_state.get("cargo_input", "").strip()
        link = st.session_state.get("link_input", "").strip()
        descricao = st.session_state.get("descricao_vaga", "").strip()

        if not empresa or not cargo or not descricao:
            st.warning("Preencha empresa, cargo e descrição da vaga.")
        else:
            perfil_base = carregar_perfil_base("data/curriculo_base.md")

            vaga = organizar_vaga(empresa, cargo, link, descricao)
            analise = analisar_aderencia(vaga, perfil_base)

            if usar_ia:
                conteudo_ia = gerar_conteudo_completo_com_ia(vaga, perfil_base)

                curriculo = conteudo_ia["curriculo"]
                mensagens = {
                    "mensagem_linkedin": conteudo_ia["mensagem_linkedin"],
                    "texto_curto": conteudo_ia["texto_curto"]
                }
            else:
                curriculo = gerar_curriculo_adaptado(vaga, perfil_base, analise)
                mensagens = gerar_mensagem_recrutador(vaga, analise)

            salvar_candidatura(vaga, analise["score"])

            st.divider()
            st.success("Candidatura registrada com sucesso.")

            st.subheader("Resultado da análise")
            mostrar_score_em_destaque(analise["score"])

            col_pontos, col_lacunas = st.columns(2)

            with col_pontos:
                exibir_lista_titulo_itens(
                    "Pontos fortes",
                    analise["pontos_fortes"],
                    "Nenhum ponto forte identificado até o momento."
                )

            with col_lacunas:
                exibir_lista_titulo_itens(
                    "Lacunas",
                    analise["lacunas"],
                    "Nenhuma lacuna relevante identificada."
                )

            st.subheader("Recomendações")
            if analise["recomendacoes"]:
                for recomendacao in analise["recomendacoes"]:
                    st.write(f"- {recomendacao}")
            else:
                st.write("Nenhuma recomendação adicional no momento.")

            with st.expander("Ver detalhes técnicos da vaga analisada"):
                st.write("Habilidades técnicas:", vaga.get("habilidades_tecnicas", []))
                st.write("Habilidades comportamentais:", vaga.get("habilidades_comportamentais", []))
                st.write("Áreas relacionadas:", vaga.get("areas_interesse", []))
                st.write("Palavras-chave:", vaga.get("palavras_chave", []))

            st.divider()

            aba1, aba2, aba3 = st.tabs([
                "Currículo adaptado",
                "Mensagem para recrutador",
                "Apresentação curta"
            ])

            with aba1:
                st.text_area(
                    "Currículo gerado",
                    curriculo,
                    height=450,
                    key="resultado_curriculo"
                )

            with aba2:
                st.text_area(
                    "Mensagem LinkedIn / e-mail",
                    mensagens["mensagem_linkedin"],
                    height=250,
                    key="resultado_mensagem"
                )

            with aba3:
                st.text_area(
                    "Texto curto",
                    mensagens["texto_curto"],
                    height=150,
                    key="resultado_texto_curto"
                )

    # =========================================================
    # HISTÓRICO
    # =========================================================
    st.divider()
    st.subheader("Histórico de candidaturas")

    historico = listar_candidaturas()

    if historico:
        df_historico = pd.DataFrame(historico)

        for _, row in df_historico.iterrows():
            with st.container():
                st.markdown(f"**Empresa:** {row['empresa']}")
                st.markdown(f"**Cargo:** {row['cargo']}")
                st.markdown(f"**Score:** {row['score']}%")
                st.markdown(f"**Data:** {row['data_candidatura']}")

                if row["link"]:
                    st.markdown(f"**Link da vaga:** [Abrir vaga]({row['link']})")
                else:
                    st.markdown("**Link da vaga:** -")

                if st.button("Excluir candidatura", key=f"del_{row['id']}"):
                    deletar_candidatura(row["id"])
                    st.success(f"Candidatura de {row['empresa']} excluída com sucesso.")
                    st.rerun()

                st.divider()
    else:
        st.info("Nenhuma candidatura registrada até o momento.")


if __name__ == "__main__":
    main()