FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Instala Poetry con pip (queda en /usr/local/bin/ para TODOS los usuarios)
RUN pip install poetry

# Variable de entorno para que Poetry siempre use .venv in-project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
