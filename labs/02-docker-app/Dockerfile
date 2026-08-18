FROM python:3.13-slim

LABEL org.opencontainers.image.title="DevOps Docker Lab"
LABEL org.opencontainers.image.description="Laboratório de containerização com Python, healthcheck e boas práticas básicas de segurança"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN groupadd --system --gid 10001 appgroup \
    && useradd --system --uid 10001 --gid appgroup --no-create-home appuser

COPY --chown=10001:10001 app.py /app/app.py

USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2).read()" || exit 1

CMD ["python", "app.py"]
