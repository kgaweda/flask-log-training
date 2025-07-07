FROM python:3.13-slim

WORKDIR /app

COPY app.py .

RUN pip install Flask gunicorn

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

