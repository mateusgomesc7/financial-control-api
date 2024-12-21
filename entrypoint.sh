#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia o servidor
poetry run fastapi run app/main.py --host 0.0.0.0