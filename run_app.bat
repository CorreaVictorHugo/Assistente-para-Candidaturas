::@echo off → limpa o terminal
::cd /d %~dp0 → vai pra pasta do projeto automaticamente
::streamlit run app.py → roda seu app
::pause → mantém a janela aberta se der erro, para você ver o que aconteceu.

@echo off

:: ===============================
:: Assistente de Candidaturas com IA
:: ===============================

@echo off 
:: Limpa o terminal

cd /d C:\Carrer_ops
:: Vai para a pasta do projeto automaticamente

python -m streamlit run app.py
:: Roda o app Streamlit

pause
:: Mantém a janela aberta se der erro, para você ver o que aconteceu.