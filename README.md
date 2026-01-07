# 🃏 Joker API

**Production-ready REST API pro náhodné vtipy** - Samostatná služba pro PrintMaster

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)

## 📝 Popis

Joker je robustní, production-ready API služba poskytující náhodné vtipy v různých jazycích a kategoriích. Vytvořena jako samostatná služba pro PrintMaster s důrazem na bezpečnost, výkon a škálovatelnost.

## ✨ Vlastnosti

### 🚀 Production-Ready
- ✅ CORS podpora pro integraci s PrintMaster
- ✅ Rate limiting proti zneužití
- ✅ Kompletní logging a error handling
- ✅ Security headers (XSS, CSRF, etc.)
- ✅ Health check endpoint pro monitoring
- ✅ Docker support s health checks
- ✅ CI/CD s GitHub Actions
- ✅ Caching pro optimální výkon

### 🌍 Multi-jazykové
- 🇨🇿 Čeština (cz)
- 🇸🇰 Slovenština (sk)
- 🇬🇧 Angličtina UK (en-gb)
- 🇺🇸 Angličtina US (en-us)

### 📂 Kategorie
- 😊 Normal - Běžné vtipy
- 🔞 Explicit - Explicitní/sprosté vtipy

### 🔧 Technologie
- **Framework**: Flask 3.1.0
- **Server**: Gunicorn 22.0.0
- **Python**: 3.11+
- **CORS**: flask-cors 5.0.0
- **Rate Limiting**: Flask-Limiter 3.8.0
- **Config**: python-dotenv 1.0.1

## 🚀 Quick Start

### Docker (Doporučeno)

```bash
# Clone repository
git clone https://github.com/Quertz/joker.git
cd joker

# Konfigurace
cp .env.example .env
# Uprav .env podle potřeby

# Spuštění
docker-compose up -d

# Test
curl http://localhost:8000/health
```

### Bez Dockeru

```bash
# Clone repository
git clone https://github.com/Quertz/joker.git
cd joker

# Virtuální prostředí
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo: venv\Scripts\activate  # Windows

# Závislosti
pip install -r requirements.txt

# Konfigurace
cp .env.example .env

# Spuštění
python app.py
```

API běží na `http://localhost:8000`

## 📚 API Dokumentace

### Základní informace
```http
GET /
```

Vrací informace o API, dostupných endpointech a konfiguraci.

**Response:**
```json
{
  "name": "Joker API",
  "version": "2.1.0",
  "description": "Production-ready API pro náhodné vtipy - služba pro PrintMaster",
  "service": "Joker - Joke Service for PrintMaster",
  "standalone": true,
  "endpoints": {
    "/": "Informace o API",
    "/joke": "Získat náhodný vtip",
    "/languages": "Seznam podporovaných jazyků",
    "/categories": "Seznam podporovaných kategorií",
    "/health": "Health check endpoint",
    "/stats": "Statistiky vtipů"
  }
}
```

### Získat náhodný vtip
```http
GET /joke?lang=cz&category=normal
```

**Parametry:**
| Parametr | Typ | Popis | Default |
|----------|-----|-------|---------|
| `lang` | string | Jazyk vtipu (`cz`, `sk`, `en-gb`, `en-us`) | `cz` |
| `category` | string | Kategorie (`normal`, `explicit`) | `normal` |

**Response:**
```json
{
  "success": true,
  "joke": "Co je to zelený a skáče po lese? Okurka na dovolené.",
  "language": "cz",
  "category": "normal",
  "timestamp": "2024-01-07T10:30:00Z",
  "service": "Joker"
}
```

**Error Response:**
```json
{
  "error": "Nepodporovaný jazyk",
  "message": "Podporované jazyky: cz, sk, en-gb, en-us",
  "requested": "de"
}
```

### Seznam jazyků
```http
GET /languages
```

**Response:**
```json
{
  "success": true,
  "languages": ["cz", "sk", "en-gb", "en-us"],
  "count": 4
}
```

### Seznam kategorií
```http
GET /categories
```

**Response:**
```json
{
  "success": true,
  "categories": ["normal", "explicit"],
  "count": 2
}
```

### Statistiky
```http
GET /stats
```

**Response:**
```json
{
  "success": true,
  "total_languages": 4,
  "total_categories": 2,
  "total_jokes": 150,
  "jokes_per_language": {
    "cz": {
      "normal": 50,
      "explicit": 30
    },
    "sk": {
      "normal": 20,
      "explicit": 10
    }
  }
}
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Joker",
  "timestamp": "2024-01-07T10:30:00Z",
  "version": "2.1.0",
  "cache_size": 8
}
```

## 🔒 Security Features

- **CORS**: Plně otevřený přístup pro PrintMastery z celého světa
- **Rate Limiting**: Ochrana proti DoS útokům
- **Security Headers**: XSS, CSRF, Clickjacking protection
- **Input Validation**: Validace všech vstupů
- **Error Handling**: Bezpečné error messages bez citlivých dat
- **Logging**: Audit log všech requestů

## ⚙️ Konfigurace

### Environment Variables

Viz `.env.example` pro všechny možnosti:

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key

# Server
HOST=0.0.0.0
PORT=8000

# Rate Limiting
RATE_LIMIT=100 per minute

# Redis (volitelné)
REDIS_URL=redis://localhost:6379/0
```

### CORS pro PrintMaster

Joker je **plně veřejná služba** s otevřeným CORS pro všechny PrintMastery z celého světa.
CORS je hardcoded v `app.py` jako `origins: "*"` a není potřeba žádná konfigurace.

## 📦 Deployment

### Docker Compose (Doporučeno)

```bash
docker-compose up -d
```

### Systemd Service

```bash
sudo systemctl enable joker
sudo systemctl start joker
```

### Azure App Service

1. Vytvoř Web App v Azure Portal
2. Nastav Python 3.11 runtime
3. Deployment Center → GitHub
4. Startup Command: `gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app`

Podrobné deployment instrukce viz [DEPLOYMENT.md](DEPLOYMENT.md)

## 🧪 Testování

### Automatické testy

```bash
# Lokální test
python test_local.py

# Bash test
./test_api.sh

# HTML test client
# Otevři test_client.html v prohlížeči
```

### Manuální testy

```bash
# Health check
curl http://localhost:8000/health

# Český vtip
curl http://localhost:8000/joke?lang=cz&category=normal

# Anglický vtip
curl "http://localhost:8000/joke?lang=en-gb&category=normal"

# Statistiky
curl http://localhost:8000/stats
```

## 📊 Monitoring

### Logy

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u joker -f

# Lokální
tail -f logs/joker.log
```

### Metriky

```bash
# Health status
curl http://localhost:8000/health

# Statistiky vtipů
curl http://localhost:8000/stats
```

## 📝 Přidávání vtipů

Vtipy jsou v `jokes/*.txt` souborech, jeden vtip = jeden řádek.

```bash
# Přidání českého vtipu
echo "Nový vtip zde" >> jokes/cz_normal.txt

# Commit
git add jokes/cz_normal.txt
git commit -m "Přidán nový vtip"
git push

# Docker: automaticky se aktualizuje při restartu
docker-compose restart
```

### Formát souborů

```
jokes/
├── cz_normal.txt       # České normální vtipy
├── cz_explicit.txt     # České explicitní vtipy
├── sk_normal.txt       # Slovenské normální vtipy
├── sk_explicit.txt     # Slovenské explicitní vtipy
├── en-gb_normal.txt    # Anglické UK normální vtipy
├── en-gb_explicit.txt  # Anglické UK explicitní vtipy
├── en-us_normal.txt    # Anglické US normální vtipy
└── en-us_explicit.txt  # Anglické US explicitní vtipy
```

## 🔧 Development

### Přidání nového jazyka

1. Vytvoř soubory:
```bash
touch jokes/de_normal.txt
touch jokes/de_explicit.txt
```

2. Uprav `app.py`:
```python
SUPPORTED_LANGUAGES = ['cz', 'sk', 'en-gb', 'en-us', 'de']
```

3. Přidej vtipy do souborů (jeden vtip na řádek, UTF-8 encoding)

4. Commit a push

### Přidání nové kategorie

1. Vytvoř soubory pro všechny jazyky:
```bash
for lang in cz sk en-gb en-us; do
  touch jokes/${lang}_dad-jokes.txt
done
```

2. Uprav `app.py`:
```python
SUPPORTED_CATEGORIES = ['normal', 'explicit', 'dad-jokes']
```

## 📁 Struktura projektu

```
joker/
├── app.py                  # Hlavní Flask aplikace
├── config.py               # Konfigurace
├── requirements.txt        # Python závislosti
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker Compose konfigurace
├── .env.example            # Příklad konfigurace
├── .dockerignore           # Docker ignore soubor
├── .gitignore              # Git ignore soubor
├── README.md               # Tato dokumentace
├── DEPLOYMENT.md           # Deployment průvodce
├── QUICKSTART.md           # Rychlý start
├── startup.sh              # Azure startup script
├── start.sh                # Lokální quick start
├── test_local.py           # Python testy
├── test_api.sh             # Bash testy
├── test_client.html        # HTML test client
├── jokes/                  # Adresář s vtipy
│   ├── cz_normal.txt
│   ├── cz_explicit.txt
│   ├── sk_normal.txt
│   ├── sk_explicit.txt
│   ├── en-gb_normal.txt
│   ├── en-gb_explicit.txt
│   ├── en-us_normal.txt
│   └── en-us_explicit.txt
├── logs/                   # Logy (git ignored)
└── .github/
    └── workflows/
        └── ci-cd.yml       # GitHub Actions CI/CD
```

## 🐛 Troubleshooting

Viz [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) pro detailní troubleshooting guide.

### Časté problémy

**CORS chyby v PrintMaster:**
- CORS je plně otevřený, chyby by se neměly vyskytovat
- Joker akceptuje requesty z jakéhokoliv původu

**429 Too Many Requests:**
- Zvyš `RATE_LIMIT` v `.env`
- Zvažte použití Redis pro distribuované rate limiting

**Žádné vtipy:**
- Zkontroluj encoding souborů (musí být UTF-8)
- Ověř, že soubory nejsou prázdné: `ls -la jokes/`

## 📄 License

MIT License - viz [LICENSE](LICENSE)

## 👨‍💻 Autor

František - [Quertz](https://github.com/Quertz)

## 🤝 Contributing

Příspěvky jsou vítány! Pro větší změny prosím otevři issue pro diskuzi.

## 📞 Support

- **Issues**: https://github.com/Quertz/joker/issues
- **Dokumentace**: [DEPLOYMENT.md](DEPLOYMENT.md), [QUICKSTART.md](QUICKSTART.md)

---

**Joker API** - Production-ready joke service for PrintMaster 🃏
