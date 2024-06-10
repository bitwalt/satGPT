FROM python:3.11-buster

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR
COPY . .
EXPOSE 8501
CMD ["poetry", "run", "streamlit", "run", "0_💬_Chat_with_assistant.py"]
