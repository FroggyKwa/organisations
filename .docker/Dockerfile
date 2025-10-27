FROM python:3.13-slim

WORKDIR /app

COPY ./requirements/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

#COPY src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini


ENV PYTHONPATH=/app


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]