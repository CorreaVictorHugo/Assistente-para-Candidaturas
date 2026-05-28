# Assistente de Candidaturas com IA

Aplicação local desenvolvida em Python para apoiar candidaturas mais estratégicas para vagas na área de dados.

O app lê ou recebe a descrição de uma vaga, compara os requisitos com um perfil profissional base, calcula aderência, identifica lacunas e gera materiais personalizados para candidatura, como currículo adaptado, mensagem para recrutador, apresentação curta e carta de apresentação.

Além de ser uma ferramenta de uso pessoal, este projeto demonstra competências importantes para trabalhos freelancer e oportunidades profissionais em dados, automação e soluções com IA.

## Objetivo do Projeto

O objetivo é reduzir o trabalho manual e aumentar a precisão no processo de candidatura.

Em vez de usar o mesmo currículo e a mesma mensagem para todas as vagas, o app ajuda a responder:

- A vaga combina com o perfil atual?
- Quais requisitos aparecem no perfil?
- Quais lacunas precisam ser tratadas com honestidade?
- Quais projetos devem ser destacados como evidência?
- Como adaptar a candidatura sem inventar experiência?

## Funcionalidades

- Busca de vagas por palavra-chave e localização.
- Sugestões locais focadas em dados, BI, automação, engenharia de dados e Rio de Janeiro/RJ.
- Atalhos para buscas externas em sites de vagas.
- Integração com API pública da Remotive para vagas remotas.
- Leitura de vagas por link.
- Extração de empresa, cargo e descrição quando possível.
- Classificação provável da vaga por área.
- Identificação de senioridade provável.
- Cálculo de score de aderência.
- Identificação de pontos fortes e lacunas.
- Seleção de projetos relevantes do portfólio como evidência.
- Geração de currículo adaptado.
- Geração de mensagem para recrutador.
- Geração de apresentação profissional curta.
- Geração de carta de apresentação.
- Histórico local de candidaturas em SQLite.
- Atalho de Área de Trabalho para abrir o app como uma aplicação local.

## Tecnologias Utilizadas

- Python
- Streamlit
- SQLite
- Pandas
- Requests
- BeautifulSoup
- Trafilatura
- Google Gemini API
- Python-dotenv

## Competências Demonstradas

Este projeto mostra domínio prático em:

- Desenvolvimento de aplicações com Python.
- Criação de interfaces com Streamlit.
- Automação de fluxos manuais.
- Integração com APIs externas.
- Processamento e limpeza de texto.
- Extração de conteúdo de páginas web.
- Uso de IA generativa em um fluxo real.
- Organização de dados em SQLite.
- Construção de lógica de score e matching.
- Criação de uma ferramenta orientada a produtividade.

## Valor Profissional

Este app pode ser entendido como um exemplo de solução para automação de processos com IA.

Em um contexto freelancer ou corporativo, a mesma lógica pode ser adaptada para:

- triagem de currículos;
- análise de compatibilidade entre candidatos e vagas;
- automação de mensagens comerciais;
- geração de propostas personalizadas;
- classificação de oportunidades;
- priorização de leads;
- análise de textos longos com regras de negócio;
- criação de assistentes internos para equipes.

O projeto demonstra não apenas conhecimento técnico, mas também capacidade de transformar uma dor real em uma ferramenta funcional.

## Projetos Usados como Evidência

O app utiliza projetos cadastrados no perfil base para fortalecer a candidatura.

Exemplos de projetos presentes na base:

- Análise prática da DRE com foco em dados.
- DRE analítica da Magazine Luiza.
- DRE Magazine Luiza 3.0 com Azure e Databricks.
- ETL com Apache Airflow, Python e PostgreSQL.
- Portfólio profissional.

Esses projetos ajudam o app a sugerir evidências mais fortes para vagas que pedem SQL, Power BI, ETL, Airflow, Azure, Databricks, PySpark, Spark SQL, Delta Lake, dashboards, indicadores e análise de dados.

## Como Funciona

1. O usuário informa uma vaga manualmente, por link ou pela busca integrada.
2. O app organiza os dados da vaga.
3. O parser identifica habilidades técnicas, comportamentais, área provável e senioridade.
4. O analisador compara a vaga com o perfil base.
5. O sistema calcula o score de aderência.
6. O app seleciona projetos relevantes como evidência.
7. A IA ou os geradores internos criam os materiais da candidatura.
8. A candidatura é registrada no histórico local.

## Como Usar

Abra o app pelo atalho da Área de Trabalho:

```text
Assistente de Candidaturas
```

Ou execute:

```bash
python -m streamlit run app.py
```

O app roda localmente em:

```text
http://localhost:8501
```

## Fluxo de Uso

1. Busque uma vaga ou preencha os dados manualmente.
2. Informe empresa, cargo, link e descrição da vaga.
3. Escolha se deseja usar IA para gerar os textos.
4. Clique em `Analisar vaga`.
5. Revise score, pontos fortes, lacunas e projetos sugeridos.
6. Use o currículo, mensagem, apresentação e carta gerados.
7. Consulte o histórico para acompanhar candidaturas anteriores.

## Interpretação do Score

- `80% ou mais`: alta compatibilidade.
- `60% a 79%`: compatibilidade moderada.
- `menos de 60%`: compatibilidade baixa.

O score é um apoio à decisão. Ele deve ser analisado junto com as lacunas, os projetos sugeridos e o objetivo profissional.

## Estrutura do Projeto

```text
app.py
```

Interface principal em Streamlit.

```text
data/curriculo_base.md
```

Perfil profissional base, competências e projetos usados como evidência.

```text
modules/buscador_vagas.py
```

Busca de vagas, sugestões locais, API Remotive e atalhos externos.

```text
modules/parser_vaga.py
```

Extração de habilidades, palavras-chave, tipo de vaga e senioridade.

```text
modules/analisador_fit.py
```

Cálculo de aderência, lacunas, pontos fortes e projetos relevantes.

```text
modules/ia_generator.py
```

Geração de conteúdos com Gemini.

```text
modules/gerador_curriculo.py
```

Geração de currículo adaptado sem IA.

```text
modules/gerador_mensagem.py
```

Geração de mensagem, apresentação curta e carta sem IA.

```text
modules/leitor_vaga.py
```

Leitura e extração de conteúdo a partir de links.

```text
modules/tracker.py
```

Histórico local de candidaturas com SQLite.

## Diferenciais

- Foco em transição para dados.
- Uso de projetos reais como evidência.
- Geração de materiais personalizados sem inventar experiência.
- Interface simples para uso diário.
- Possibilidade de funcionar como base para soluções freelancer.
- Combinação de automação, IA generativa e análise de texto.

## Limitações Atuais

- A busca real por vagas depende de fontes externas.
- Sites como LinkedIn e Gupy podem limitar automações.
- A leitura automática por link pode variar conforme a estrutura da página.
- Os textos gerados devem ser revisados antes do envio.

## Próximas Melhorias

- Exportar currículo e carta em `.docx`.
- Criar status de candidatura, como aplicada, mensagem enviada, entrevista e follow-up.
- Adicionar lembretes de follow-up.
- Melhorar integração com fontes reais de vagas.
- Criar uma área para cadastrar novos projetos pela interface.
- Criar filtros mais avançados por localidade, senioridade e modalidade.

## Observação

Este projeto foi desenvolvido para uso local e como demonstração prática de automação aplicada à carreira, dados e IA.

Ele representa uma solução real para uma necessidade concreta: tornar candidaturas mais objetivas, consistentes e alinhadas com evidências profissionais.
