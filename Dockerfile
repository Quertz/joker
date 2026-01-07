# Použití oficiálního Python runtime jako parent image
FROM python:3.11-slim

# Nastavení working directory v kontejneru
WORKDIR /app

# Kopírování requirements.txt
COPY requirements.txt .

# Instalace závislostí
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování celé aplikace
COPY . .

# Vytvoření adresáře pro logy
RUN mkdir -p logs

# Nastavení práv
RUN chmod +x startup.sh start.sh 2>/dev/null || true

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Spuštění aplikace pomocí gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
