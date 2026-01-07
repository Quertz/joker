# 🎭 Joke API - Rychlý Start

## 🚀 Co je to?

Jednoduché REST API, které vrací náhodné vtipy v různých jazycích (CZ, SK, EN-GB, EN-US) a kategoriích (normální, explicitní).

## 📦 Co je v balíčku?

```
joke-api/
├── app.py                    # Hlavní Flask aplikace
├── requirements.txt          # Python závislosti  
├── startup.sh               # Startup pro Azure
├── start.sh                 # Rychlé lokální spuštění
├── test_api.sh              # Bash testy
├── test_local.py            # Python testy
├── test_client.html         # HTML testovací klient
├── README.md                # Kompletní dokumentace
└── jokes/                   # Vtipy (jeden vtip = jeden řádek)
    ├── cz_normal.txt        # České normální
    ├── cz_explicit.txt      # České explicitní
    ├── sk_normal.txt        # Slovenské normální
    ├── sk_explicit.txt      # Slovenské explicitní
    ├── en-gb_normal.txt     # Anglické UK
    ├── en-gb_explicit.txt
    ├── en-us_normal.txt     # Anglické US
    └── en-us_explicit.txt
```

## 🏃 Rychlé lokální spuštění

### Varianta 1: Automatický skript
```bash
chmod +x start.sh
./start.sh
```

### Varianta 2: Manuálně
```bash
# Vytvoř virtuální prostředí
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate     # Windows

# Nainstaluj závislosti
pip install -r requirements.txt

# Spusť aplikaci
python app.py
```

API poběží na `http://localhost:8000`

## 🧪 Testování

### V prohlížeči
Otevři `test_client.html` v prohlížeči - krásný UI pro testování!

### Pomocí curl
```bash
# Základní info
curl http://localhost:8000/

# Český normální vtip
curl http://localhost:8000/joke?lang=cz&category=normal

# Český explicitní vtip  
curl http://localhost:8000/joke?lang=cz&category=explicit

# Slovenský vtip
curl http://localhost:8000/joke?lang=sk

# Anglický vtip
curl http://localhost:8000/joke?lang=en-gb
```

### Python test skript
```bash
pip install requests  # pokud ještě nemáš
python test_local.py
```

### Bash test skript
```bash
chmod +x test_api.sh
./test_api.sh
```

## ☁️ Deployment na Azure (F1 Free Tier)

### Předpoklady
1. Azure účet (zdarma: https://azure.microsoft.com/free/)
2. GitHub/GitLab účet
3. Nahraný kód v repozitáři

### Postup (Azure Portal)

1. **Přihlaš se:** https://portal.azure.com

2. **Vytvoř Web App:**
   - Create a resource → Web App
   - Resource Group: `joke-api-rg` (nová)
   - Name: `{tvuj-nazev}` (musí být unikátní)
   - Publish: Code
   - Runtime: Python 3.11+
   - OS: Linux
   - Region: West Europe (nebo nejbližší)
   - Pricing: F1 (Free) - klikni "Change size" a vyber F1
   - Create

3. **Nastav Git Deployment:**
   - Jdi do tvé Web App → Deployment Center
   - Source: GitHub (nebo GitLab/Bitbucket)
   - Autorizuj Azure
   - Vyber repozitář a branch
   - Save

4. **Nastav Startup Command:**
   - Configuration → General settings
   - Startup Command: 
     ```
     gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
     ```
   - Save

5. **Hotovo!** 🎉
   - Azure automaticky nasadí aplikaci
   - URL: `https://{tvuj-nazev}.azurewebsites.net`
   - Každý push do repozitáře = automatický deployment

### Test po nasazení

```bash
# Základní info
curl https://{tvuj-nazev}.azurewebsites.net/

# Vtip
curl https://{tvuj-nazev}.azurewebsites.net/joke?lang=cz&category=normal
```

## ➕ Přidávání vtipů

Jednoduché! Prostě otevři příslušný soubor v `jokes/` a přidej vtip na nový řádek:

```bash
# Přidej český normální vtip
echo "Proč programátoři neradi chodí ven? Protože venku je moc bugů." >> jokes/cz_normal.txt

# Commit a push (pokud je to v Gitu)
git add jokes/cz_normal.txt
git commit -m "Přidán nový vtip"
git push
```

Na Azure se to automaticky nasadí!

## 🌍 Přidání nového jazyka

1. Vytvoř soubory:
   ```bash
   touch jokes/de_normal.txt      # Němčina normální
   touch jokes/de_explicit.txt    # Němčina explicitní
   ```

2. Přidej vtipy (jeden na řádek)

3. Uprav `app.py`:
   ```python
   SUPPORTED_LANGUAGES = ['cz', 'sk', 'en-gb', 'en-us', 'de']
   ```

4. Commit a push!

## 📊 API Endpointy

| Endpoint | Parametry | Popis |
|----------|-----------|-------|
| `GET /` | - | Info o API |
| `GET /joke` | `lang`, `category` | Náhodný vtip |
| `GET /languages` | - | Seznam jazyků |
| `GET /categories` | - | Seznam kategorií |
| `GET /health` | - | Health check |

### Parametry

- `lang`: `cz`, `sk`, `en-gb`, `en-us` (default: `cz`)
- `category`: `normal`, `explicit` (default: `normal`)

## 💡 Tipy

- **Lokálně:** API běží na `localhost:8000`
- **Azure F1 Free:** 60 min CPU/den, 1 GB RAM - pro vtipové API více než dost!
- **Může "usnout":** Po 20 min neaktivity se může zastavit, první request ji probudí
- **Vtipy:** UTF-8 encoding, jeden vtip = jeden řádek
- **Test klient:** `test_client.html` - krásné UI v prohlížeči!

## 🔧 Troubleshooting

**API neběží lokálně:**
```bash
# Zkontroluj závislosti
pip list | grep Flask

# Reinstaluj
pip install -r requirements.txt

# Zkontroluj port
lsof -i :8000  # pokud je obsazený, změň port v app.py
```

**Azure deployment selhává:**
- Zkontroluj Startup Command v Configuration
- Zkontroluj Application Logs v Log stream
- Ověř, že máš správný Python runtime

**Vtipy se nezobrazují:**
- Zkontroluj encoding souborů (musí být UTF-8)
- Ověř, že soubory nejsou prázdné
- Zkontroluj názvy souborů: `{lang}_{category}.txt`

## 📚 Další info

Kompletní dokumentace je v `README.md`!

---

Vytvořil: František
Verze: 1.0
Licence: MIT
