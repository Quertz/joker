# Joker API - Deployment Guide

Komplexní průvodce nasazením Joker API do produkčního prostředí.

## 📋 Obsah

- [Požadavky](#požadavky)
- [Konfigurace](#konfigurace)
- [Deployment metody](#deployment-metody)
  - [Docker (Doporučeno)](#docker-doporučeno)
  - [Systemd Service](#systemd-service)
  - [Azure App Service](#azure-app-service)
  - [Kubernetes](#kubernetes)
- [Monitoring a Logging](#monitoring-a-logging)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

## Požadavky

### Minimální požadavky
- Python 3.11+
- 512 MB RAM
- 1 CPU core
- 100 MB disk space

### Doporučené pro produkci
- Python 3.11 nebo 3.12
- 1 GB+ RAM
- 2+ CPU cores
- 1 GB disk space (pro logy)

## Konfigurace

### 1. Environment Variables

Zkopíruj `.env.example` do `.env`:

```bash
cp .env.example .env
```

Uprav `.env` podle svých potřeb:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<vygeneruj-silny-klic>

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS je hardcoded v app.py jako plně otevřený (*) - žádná konfigurace není potřeba

# Rate Limiting
RATE_LIMIT=100 per minute

# Redis (volitelné, pro distribuované rate limiting)
# REDIS_URL=redis://localhost:6379/0
```

### 2. Generování Secret Key

```bash
python -c "import os; print(os.urandom(24).hex())"
```

## Deployment metody

### Docker (Doporučeno)

Docker deployment je nejjednodušší a nejbezpečnější metoda.

#### Základní spuštění

```bash
# Build
docker build -t joker-api .

# Spuštění
docker run -d \
  --name joker \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  joker-api
```

#### Docker Compose (Doporučeno)

```bash
# Spuštění
docker-compose up -d

# Sledování logů
docker-compose logs -f

# Zastavení
docker-compose down

# Restart
docker-compose restart
```

#### S Redis (pro lepší rate limiting)

Odkomentuj Redis sekci v `docker-compose.yml` a nastav:

```bash
REDIS_URL=redis://redis:6379/0
```

Pak spusť:

```bash
docker-compose up -d
```

### Systemd Service

Pro deployment na Linux serveru bez Dockeru.

#### 1. Instalace závislostí

```bash
cd /opt/joker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Vytvoř systemd service

`/etc/systemd/system/joker.service`:

```ini
[Unit]
Description=Joker API Service
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/joker
Environment="PATH=/opt/joker/venv/bin"
EnvironmentFile=/opt/joker/.env
ExecStart=/opt/joker/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3. Spuštění

```bash
sudo systemctl daemon-reload
sudo systemctl enable joker
sudo systemctl start joker
sudo systemctl status joker
```

#### 4. Nginx Reverse Proxy

`/etc/nginx/sites-available/joker`:

```nginx
server {
    listen 80;
    server_name joker.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/joker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Azure App Service

Viz původní README.md pro detailní Azure instrukce.

#### Rychlý deployment

1. Vytvoř Web App v Azure Portal
2. Nastav Python 3.11 runtime
3. Deployment Center → GitHub
4. Startup Command:
   ```
   gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
   ```

### Kubernetes

#### Deployment YAML

`k8s/deployment.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: joker-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: joker-api
  template:
    metadata:
      labels:
        app: joker-api
    spec:
      containers:
      - name: joker
        image: joker-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: FLASK_ENV
          value: "production"
        # CORS je hardcoded v app.py jako plně otevřený
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: joker-api-service
spec:
  selector:
    app: joker-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f k8s/deployment.yml
kubectl get pods
kubectl get svc
```

## Monitoring a Logging

### Logy

Logy jsou uloženy v `logs/joker.log` s rotací:
- Max velikost: 10 MB
- Max backupů: 10
- Celkem: ~100 MB

### Monitoring endpointů

```bash
# Health check
curl http://localhost:8000/health

# Statistiky
curl http://localhost:8000/stats
```

### Prometheus metrics (budoucí rozšíření)

Pro produkční monitoring doporučujeme přidat Prometheus exporter.

## Security Best Practices

### 1. CORS Konfigurace

Joker je **záměrně** plně veřejná služba s otevřeným CORS (`origins: "*"`).
CORS je hardcoded v `app.py` pro maximální dostupnost PrintMasterů z celého světa.

Žádná konfigurace není potřeba - služba je přístupná ze všech originů.

### 2. Secret Key

Vždy použij silný, náhodný secret key:

```bash
SECRET_KEY=$(python -c "import os; print(os.urandom(24).hex())")
```

### 3. HTTPS

Vždy použij HTTPS v produkci:
- Azure App Service: automaticky
- Custom server: použij Let's Encrypt + Nginx/Apache

### 4. Rate Limiting

Nastav vhodný rate limit podle očekávaného trafficu:

```bash
# Konzervativní (doporučeno pro start)
RATE_LIMIT=100 per minute

# Pro vyšší traffic
RATE_LIMIT=500 per minute

# Pro development
RATE_LIMIT=1000 per minute
```

### 5. Firewall

Otevři pouze potřebné porty:
- 80 (HTTP - redirect na HTTPS)
- 443 (HTTPS)
- 22 (SSH - pouze z důvěryhodných IP)

## Troubleshooting

### API nereaguje

```bash
# Docker
docker logs joker

# Systemd
sudo journalctl -u joker -f

# Zkontroluj health endpoint
curl http://localhost:8000/health
```

### High CPU/Memory usage

```bash
# Zkontroluj resources
docker stats joker

# Systemd
top -p $(pgrep -f "gunicorn.*app:app")
```

### Rate limit problémy

Pokud dostáváš 429 chyby příliš často:
1. Zvyš `RATE_LIMIT` v `.env`
2. Použij Redis pro distribuované rate limiting
3. Zkontroluj, zda máš správně nakonfigurovaný reverse proxy (X-Forwarded-For)

### CORS chyby

CORS je plně otevřený (`origins: "*"`), takže CORS chyby by se neměly vyskytovat.

Pokud přesto vidíš CORS chyby:
```bash
# Ověř, že server běží a odpovídá
curl -I http://localhost:8000/health

# Test CORS headeru z jakéhokoliv originu
curl -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: GET" \
  -X OPTIONS \
  http://localhost:8000/joke
```

### Žádné vtipy v odpovědích

```bash
# Zkontroluj jokes soubory
ls -la jokes/
cat jokes/cz_normal.txt

# Zkontroluj cache
curl http://localhost:8000/stats
```

## Aktualizace

### Docker

```bash
# Pull nové změny
git pull

# Rebuild a restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Systemd

```bash
# Pull nové změny
cd /opt/joker
git pull

# Aktivuj venv a aktualizuj závislosti
source venv/bin/activate
pip install -r requirements.txt

# Restart
sudo systemctl restart joker
```

## Backup

### Co zálohovat
1. Jokes soubory: `jokes/*.txt`
2. Environment: `.env`
3. Logy (volitelné): `logs/*.log`

### Automatický backup

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/joker"
DATE=$(date +%Y%m%d_%H%M%S)

tar -czf "$BACKUP_DIR/joker_$DATE.tar.gz" \
  jokes/ \
  .env

# Smazání starších než 30 dní
find "$BACKUP_DIR" -name "joker_*.tar.gz" -mtime +30 -delete
```

Přidej do cronu:
```bash
0 2 * * * /opt/joker/backup.sh
```

## Support

Pro problémy nebo dotazy:
- Issues: https://github.com/Quertz/joker/issues
- Dokumentace: README.md, QUICKSTART.md
