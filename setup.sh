#!/bin/bash

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Para Windows, use: venv\Scripts\activate

# Instalar dependências
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "✓ Ambiente virtual criado e dependências instaladas!"
echo "Para ativar o venv:"
echo "  Linux/Mac: source venv/bin/activate"
echo "  Windows: venv\Scripts\activate"
