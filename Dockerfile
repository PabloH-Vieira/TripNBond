FROM python:3.12-slim

# Definição do diretório
WORKDIR /app

# Instalação do poetry
RUN pip install poetry

# Copia os arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Configura o poetry para não criar um ambiente virtual, já que o container já é um
RUN poetry config virtualenvs.create false

# Instala as dependências
RUN poetry install --no-root --no-interaction --no-ansi

# Copia todo o código do projeto para o container
COPY . .

# Inicia o servidor escutando todas as redes do container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]