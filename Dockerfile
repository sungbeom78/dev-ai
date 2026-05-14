FROM python:3.11-slim

WORKDIR /code

COPY pyproject.toml .
# Install basic dependencies right away for faster build during development
RUN pip install --no-cache-dir fastapi uvicorn pydantic psycopg2-binary qdrant-client sqlalchemy openai

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
