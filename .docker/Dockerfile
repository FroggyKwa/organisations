FROM python:3.13-slim

WORKDIR /app

COPY ./requirements/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY .docker/entrypoint.sh /app/entrypoint.sh


ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/.docker/entrypoint.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]