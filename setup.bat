@echo off
REM Criar ambiente virtual
python -m venv venv

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Instalar dependências
pip install --upgrade pip
pip install -r backend\requirements.txt

echo.
echo ✓ Ambiente virtual criado e dependências instaladas!
echo Para ativar o venv no futuro:
echo   venv\Scripts\activate.bat
pause
