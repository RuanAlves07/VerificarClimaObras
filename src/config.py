import os
from dotenv import load_dotenv

load_dotenv()

# Configurações da API de Clima
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "sua_api_key_aqui")

# Configurações do Banco de Dados
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "clima_obras")

# Debug
DEBUG = os.getenv("DEBUG", "False") == "True"
