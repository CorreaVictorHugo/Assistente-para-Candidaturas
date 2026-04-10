::@echo off → limpa o terminal
::cd /d %~dp0 → vai pra pasta do projeto automaticamente
::streamlit run app.py → roda seu app
::pause → mantém a janela aberta se der erro, para você ver o que aconteceu.

@echo off

:: ===============================
:: Assistente de Candidaturas com IA
:: ===============================

echo Iniciando o app...

:: Vai para a pasta do projeto
cd /d %~dp0

:: Executa o Streamlit
python -m streamlit run app.py

:: Mantém a janela aberta
pause