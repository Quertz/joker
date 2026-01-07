#!/bin/bash

echo "🚀 Joke API - Quick Start"
echo ""

# Kontrola Pythonu
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 není nainstalován!"
    exit 1
fi

echo "✅ Python3 nalezen: $(python3 --version)"
echo ""

# Vytvoření virtuálního prostředí
if [ ! -d "venv" ]; then
    echo "📦 Vytvářím virtuální prostředí..."
    python3 -m venv venv
    echo "✅ Virtuální prostředí vytvořeno"
else
    echo "✅ Virtuální prostředí již existuje"
fi
echo ""

# Aktivace virtuálního prostředí
echo "🔌 Aktivuji virtuální prostředí..."
source venv/bin/activate
echo "✅ Virtuální prostředí aktivováno"
echo ""

# Instalace závislostí
echo "📚 Instaluji závislosti..."
pip install -q -r requirements.txt
echo "✅ Závislosti nainstalovány"
echo ""

# Spuštění aplikace
echo "🎉 Spouštím API..."
echo ""
echo "API poběží na: http://localhost:8000"
echo "Pro zastavení stiskni Ctrl+C"
echo ""
echo "Dostupné endpointy:"
echo "  - http://localhost:8000/           (informace o API)"
echo "  - http://localhost:8000/joke       (náhodný vtip)"
echo "  - http://localhost:8000/languages  (seznam jazyků)"
echo "  - http://localhost:8000/categories (seznam kategorií)"
echo ""
echo "Příklady:"
echo "  curl http://localhost:8000/joke?lang=cz&category=normal"
echo "  curl http://localhost:8000/joke?lang=cz&category=explicit"
echo ""

python app.py
