# 🚀 Assistente de Candidaturas com IA

Aplicação em Python desenvolvida para otimizar e automatizar o processo de candidatura a vagas de emprego.

O sistema permite analisar vagas, gerar currículo personalizado, criar mensagens para recrutadores e organizar candidaturas de forma estruturada.

---

# 🎯 Objetivo

Facilitar e acelerar o processo de candidatura, tornando-o mais estratégico, organizado e eficiente.

A aplicação foi projetada para rodar localmente e fornecer suporte completo ao usuário durante a candidatura.

---

# 🧠 Funcionalidades

## 📥 Entrada de dados
- preenchimento de empresa, cargo e link
- inserção manual da descrição da vaga
- leitura automática da vaga por link

## 🔍 Busca de vagas
- busca por palavra-chave
- filtro por localização
- seleção de vagas diretamente na interface

## 📊 Análise de aderência
- comparação com perfil-base
- score de compatibilidade
- identificação de:
  - pontos fortes
  - lacunas
  - recomendações

## 🤖 Uso de IA (opcional)
- geração de currículo com IA (Gemini)
- geração de mensagem para recrutador
- geração de apresentação curta
- otimização de tokens com chamada única

## 📄 Geração de conteúdo
- currículo adaptado (ATS-friendly)
- mensagem para recrutador (LinkedIn/e-mail)
- resumo profissional

## 🧹 Tratamento de dados
- limpeza do texto extraído de páginas web
- remoção de ruído (cookies, menus, etc.)

## 🗂️ Histórico de candidaturas
- armazenamento em SQLite
- listagem de candidaturas
- exclusão diretamente pela interface

## ⚡ Usabilidade
- botões de limpeza:
  - limpar busca
  - limpar formulário
  - limpar descrição

---

# 🛠️ Tecnologias utilizadas

- Python
- Streamlit
- SQLite
- pandas
- requests
- BeautifulSoup
- trafilatura
- Google Gemini API (IA)

---

# 📁 Estrutura do projeto

```bash
assistente_candidaturas_ia/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── curriculo_base.md
│   └── vagas.db
│
├── modules/
│   ├── parser_vaga.py
│   ├── analisador_fit.py
│   ├── gerador_curriculo.py
│   ├── gerador_mensagem.py
│   ├── ia_generator.py
│   ├── leitor_vaga.py
│   ├── buscador_vagas.py
│   ├── tracker.py
│   └── exportador.py
│
├── outputs/
│   ├── curriculos/
│   ├── mensagens/
│   └── relatorios/
│
└── templates/

⚙️ Papel dos módulos

app.py

Interface principal da aplicação (Streamlit)

- parser_vaga.py

Processa e organiza os dados da vaga

- analisador_fit.py

Calcula aderência e gera score

- gerador_curriculo.py

Gera currículo sem IA

- gerador_mensagem.py

Gera mensagens sem IA

- ia_generator.py

Integração com IA (Gemini)

- leitor_vaga.py

Extrai conteúdo de vagas a partir de links

- buscador_vagas.py

Busca vagas (versão inicial simulada)

- tracker.py

Gerencia o banco SQLite

- exportador.py

Preparado para exportações futuras

