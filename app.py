from flask import Flask, jsonify, request
import random
import os

app = Flask(__name__)

# Podporované jazyky a kategorie
SUPPORTED_LANGUAGES = ['cz', 'sk', 'en-gb', 'en-us']
SUPPORTED_CATEGORIES = ['normal', 'explicit']

def load_jokes(language, category):
    """Načte vtipy ze souboru pro daný jazyk a kategorii"""
    filename = f"jokes/{language}_{category}.txt"
    
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        jokes = [line.strip() for line in f if line.strip()]
    
    return jokes

@app.route('/')
def home():
    """Hlavní stránka s informacemi o API"""
    return jsonify({
        'name': 'Joke API',
        'version': '1.0',
        'description': 'API pro náhodné vtipy v různých jazycích',
        'endpoints': {
            '/': 'Informace o API',
            '/joke': 'Získat náhodný vtip',
            '/languages': 'Seznam podporovaných jazyků',
            '/categories': 'Seznam podporovaných kategorií'
        },
        'parameters': {
            'lang': f"Jazyk vtipu ({', '.join(SUPPORTED_LANGUAGES)}), výchozí: cz",
            'category': f"Kategorie vtipu ({', '.join(SUPPORTED_CATEGORIES)}), výchozí: normal"
        },
        'example': '/joke?lang=cz&category=normal'
    })

@app.route('/joke')
def get_joke():
    """Vrátí náhodný vtip podle parametrů"""
    # Získání parametrů z URL
    language = request.args.get('lang', 'cz').lower()
    category = request.args.get('category', 'normal').lower()
    
    # Validace jazyka
    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            'error': f'Nepodporovaný jazyk. Podporované jazyky: {", ".join(SUPPORTED_LANGUAGES)}'
        }), 400
    
    # Validace kategorie
    if category not in SUPPORTED_CATEGORIES:
        return jsonify({
            'error': f'Nepodporovaná kategorie. Podporované kategorie: {", ".join(SUPPORTED_CATEGORIES)}'
        }), 400
    
    # Načtení vtipů
    jokes = load_jokes(language, category)
    
    if not jokes:
        return jsonify({
            'error': f'Žádné vtipy pro jazyk "{language}" a kategorii "{category}"'
        }), 404
    
    # Výběr náhodného vtipu
    joke = random.choice(jokes)
    
    return jsonify({
        'joke': joke,
        'language': language,
        'category': category
    })

@app.route('/languages')
def get_languages():
    """Vrátí seznam podporovaných jazyků"""
    return jsonify({
        'languages': SUPPORTED_LANGUAGES
    })

@app.route('/categories')
def get_categories():
    """Vrátí seznam podporovaných kategorií"""
    return jsonify({
        'categories': SUPPORTED_CATEGORIES
    })

@app.route('/health')
def health():
    """Health check endpoint pro Azure"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
