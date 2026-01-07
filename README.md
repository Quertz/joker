# Joke API

Jednoduché REST API pro náhodné vtipy v různých jazycích a kategoriích.

## Funkce

- 🎭 Více kategorií: normální a explicitní (sprosté) vtipy
- 🌍 Více jazyků: čeština (cz), slovenština (sk), angličtina (en-gb, en-us)
- 🎲 Náhodný výběr vtipů
- 📝 Jednoduché přidávání nových vtipů do textových souborů
- ⚡ Optimalizováno pro Azure App Service F1 Free Plan

## API Endpointy

### Základní informace
```
GET /
```
Vrátí informace o API a dostupných endpointech.

### Získat náhodný vtip
```
GET /joke?lang=cz&category=normal
```

**Parametry:**
- `lang` (volitelné): Jazyk vtipu - `cz`, `sk`, `en-gb`, `en-us` (výchozí: `cz`)
- `category` (volitelné): Kategorie vtipu - `normal`, `explicit` (výchozí: `normal`)

**Příklad odpovědi:**
```json
{
  "joke": "Co je to zelený a skáče po lese? Okurka na dovolené.",
  "language": "cz",
  "category": "normal"
}
```

### Seznam jazyků
```
GET /languages
```

### Seznam kategorií
```
GET /categories
```

### Health Check
```
GET /health
```

## Lokální vývoj

### Instalace

1. Klonuj repozitář
2. Vytvoř virtuální prostředí:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate  # Windows
```

3. Nainstaluj závislosti:
```bash
pip install -r requirements.txt
```

### Spuštění

```bash
python app.py
```

API poběží na `http://localhost:8000`

### Testování

```bash
# Základní informace
curl http://localhost:8000/

# Český normální vtip
curl http://localhost:8000/joke?lang=cz&category=normal

# Český explicitní vtip
curl http://localhost:8000/joke?lang=cz&category=explicit

# Slovenský vtip
curl http://localhost:8000/joke?lang=sk&category=normal

# Anglický vtip (UK)
curl http://localhost:8000/joke?lang=en-gb&category=normal
```

## Přidávání vtipů

Vtipy jsou uloženy v souborech v adresáři `jokes/` podle formátu:
```
jokes/{jazyk}_{kategorie}.txt
```

Například:
- `jokes/cz_normal.txt` - české normální vtipy
- `jokes/cz_explicit.txt` - české explicitní vtipy
- `jokes/sk_normal.txt` - slovenské normální vtipy

**Jeden vtip = jeden řádek v souboru**

Pro přidání nového vtipu stačí:
1. Otevřít příslušný soubor
2. Přidat vtip na nový řádek
3. Uložit soubor
4. Restartovat aplikaci (na Azure se automaticky restartuje při push do repozitáře)

## Deployment na Azure App Service (F1 Free Plan)

### Předpoklady
- Azure účet (můžeš vytvořit zdarma na https://azure.microsoft.com/free/)
- Git repozitář s tímto kódem (GitHub, GitLab, Bitbucket)
- Azure CLI nainstalované (volitelné, lze použít i Azure Portal)

### Postup přes Azure Portal

1. **Přihlas se na Azure Portal** (https://portal.azure.com)

2. **Vytvoř Web App:**
   - Klikni na "Create a resource"
   - Hledej "Web App" a vyber ji
   - Vyplň:
     - **Resource Group**: vytvoř novou (např. `joke-api-rg`)
     - **Name**: jedinečný název (např. `moje-joke-api`)
     - **Publish**: Code
     - **Runtime stack**: Python 3.11 (nebo novější)
     - **Operating System**: Linux
     - **Region**: Europe West (nebo nejbližší region)
     - **Pricing Plan**: F1 (Free) - klikni na "Change size" a vyber F1

3. **Nastav Deployment:**
   - Po vytvoření Web App jdi do "Deployment Center"
   - Vyber svůj Git provider (GitHub/GitLab/Bitbucket)
   - Autorizuj Azure přístup k tvému účtu
   - Vyber repozitář a branch
   - Ulož nastavení

4. **Nastav Startup Command:**
   - Jdi do "Configuration" → "General settings"
   - V poli "Startup Command" zadej:
     ```
     gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
     ```
   - Ulož změny

5. **Deploy:**
   - Azure automaticky nasadí aplikaci z tvého repozitáře
   - Každý push do repozitáře spustí nový deployment
   - URL tvého API bude: `https://{tvuj-nazev}.azurewebsites.net`

### Postup přes Azure CLI

1. **Přihlaš se:**
```bash
az login
```

2. **Vytvoř Resource Group:**
```bash
az group create --name joke-api-rg --location westeurope
```

3. **Vytvoř App Service Plan (F1 Free):**
```bash
az appservice plan create \
  --name joke-api-plan \
  --resource-group joke-api-rg \
  --sku F1 \
  --is-linux
```

4. **Vytvoř Web App:**
```bash
az webapp create \
  --resource-group joke-api-rg \
  --plan joke-api-plan \
  --name moje-joke-api \
  --runtime "PYTHON:3.11"
```

5. **Nastav Startup Command:**
```bash
az webapp config set \
  --resource-group joke-api-rg \
  --name moje-joke-api \
  --startup-file "gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app"
```

6. **Nastav Git deployment:**
```bash
az webapp deployment source config \
  --name moje-joke-api \
  --resource-group joke-api-rg \
  --repo-url https://github.com/{username}/{repo} \
  --branch main \
  --manual-integration
```

### Ověření

Po úspěšném nasazení:

```bash
# Test API
curl https://moje-joke-api.azurewebsites.net/

# Získej vtip
curl https://moje-joke-api.azurewebsites.net/joke?lang=cz&category=normal
```

### Monitorování a logy

- **Azure Portal** → tvoje Web App → "Log stream" - živé logy
- **Azure Portal** → tvoje Web App → "Metrics" - metriky využití

## Struktura projektu

```
joke-api/
├── app.py              # Hlavní Flask aplikace
├── requirements.txt    # Python závislosti
├── startup.sh          # Startup skript pro Azure
├── .gitignore         # Git ignore soubor
├── README.md          # Dokumentace
└── jokes/             # Adresář s vtipy
    ├── cz_normal.txt      # České normální vtipy
    ├── cz_explicit.txt    # České explicitní vtipy
    ├── sk_normal.txt      # Slovenské normální vtipy
    ├── sk_explicit.txt    # Slovenské explicitní vtipy
    ├── en-gb_normal.txt   # Anglické (UK) normální vtipy
    ├── en-gb_explicit.txt # Anglické (UK) explicitní vtipy
    ├── en-us_normal.txt   # Anglické (US) normální vtipy
    └── en-us_explicit.txt # Anglické (US) explicitní vtipy
```

## Technické detaily

- **Framework**: Flask 3.0.0
- **Server**: Gunicorn 21.2.0
- **Python**: 3.11+
- **Kódování**: UTF-8 pro všechny soubory s vtipy

## Omezení Azure F1 Free Tier

- 60 minut CPU času denně
- 1 GB RAM
- 1 GB úložiště
- Žádné custom domény
- Žádné automatické škálování
- Aplikace může "usnout" po 20 minutách neaktivity

Pro tvůj případ s jednoduchým API na vtipy je toto naprosto dostačující!

## Rozšíření

### Přidání nového jazyka

1. Vytvoř nové soubory v `jokes/`:
   - `{jazyk_kod}_normal.txt`
   - `{jazyk_kod}_explicit.txt`

2. Přidej jazykový kód do `SUPPORTED_LANGUAGES` v `app.py`:
```python
SUPPORTED_LANGUAGES = ['cz', 'sk', 'en-gb', 'en-us', 'de', 'fr']
```

3. Commit a push změny

### Přidání nové kategorie

1. Vytvoř nové soubory pro všechny jazyky:
   - `{jazyk}_{nova_kategorie}.txt`

2. Přidej kategorii do `SUPPORTED_CATEGORIES` v `app.py`:
```python
SUPPORTED_CATEGORIES = ['normal', 'explicit', 'dark', 'dad-jokes']
```

## License

MIT

## Autor

František - https://github.com/Quertz/joke-api
