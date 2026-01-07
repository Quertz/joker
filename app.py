from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import random
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import atexit
from auto_update import init_auto_updater, get_auto_updater

# Načtení environment variables
load_dotenv()

app = Flask(__name__)

# Konfigurace z environment variables
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())

# CORS konfigurace - plně otevřená služba pro PrintMastery z celého světa
# Joker je veřejná služba bez omezení původu požadavků
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False,
        "max_age": 3600
    }
})

# Rate limiting - ochrana proti zneužití
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[os.getenv('RATE_LIMIT', '100 per minute')],
    storage_uri=os.getenv('REDIS_URL', 'memory://')
)

# Logging konfigurace
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/joker.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Joker API startup')

# Podporované jazyky a kategorie
SUPPORTED_LANGUAGES = ['cz', 'sk', 'en-gb', 'en-us']
SUPPORTED_CATEGORIES = ['normal', 'explicit']

# Cache pro vtipy (načte se při startu)
jokes_cache = {}

def load_jokes(language, category):
    """Načte vtipy ze souboru pro daný jazyk a kategorii"""
    cache_key = f"{language}_{category}"

    # Použití cache pokud existuje
    if cache_key in jokes_cache:
        return jokes_cache[cache_key]

    filename = f"jokes/{language}_{category}.txt"

    if not os.path.exists(filename):
        app.logger.warning(f"Soubor s vtipy nenalezen: {filename}")
        return []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Čtení celého obsahu a rozdělení podle dvojitého odřádkování
            # To umožňuje víceřádkové vtipy oddělené prázdným řádkem
            content = f.read()
            jokes = [joke.strip() for joke in content.split('\n\n') if joke.strip()]

        # Uložení do cache
        jokes_cache[cache_key] = jokes
        app.logger.info(f"Načteno {len(jokes)} vtipů z {filename}")

        return jokes
    except Exception as e:
        app.logger.error(f"Chyba při načítání vtipů z {filename}: {str(e)}")
        return []

def preload_jokes():
    """Předčasné načtení všech vtipů do cache při startu"""
    app.logger.info("Předčasné načítání vtipů do cache...")
    for lang in SUPPORTED_LANGUAGES:
        for cat in SUPPORTED_CATEGORIES:
            load_jokes(lang, cat)
    app.logger.info(f"Cache naplněna, celkem klíčů: {len(jokes_cache)}")

# Předčasné načtení při importu modulu (pro gunicorn)
preload_jokes()

# Inicializace auto-update při importu (pro gunicorn)
init_auto_updater(app)

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Přidá bezpečnostní hlavičky do všech odpovědí"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/')
@limiter.limit("50 per minute")
def home():
    """Hlavní stránka s informacemi o API"""
    return jsonify({
        'name': 'Joker API',
        'version': '2.1.0',
        'description': 'Production-ready API pro náhodné vtipy - služba pro PrintMaster',
        'service': 'Joker - Joke Service for PrintMaster',
        'standalone': True,
        'endpoints': {
            '/': 'Informace o API',
            '/joke': 'Získat náhodný vtip',
            '/languages': 'Seznam podporovaných jazyků',
            '/categories': 'Seznam podporovaných kategorií',
            '/health': 'Health check endpoint',
            '/stats': 'Statistiky vtipů',
            '/update-status': 'Status auto-update služby'
        },
        'parameters': {
            'lang': f"Jazyk vtipu ({', '.join(SUPPORTED_LANGUAGES)}), výchozí: cz",
            'category': f"Kategorie vtipu ({', '.join(SUPPORTED_CATEGORIES)}), výchozí: normal"
        },
        'examples': {
            'czech_normal': '/joke?lang=cz&category=normal',
            'czech_explicit': '/joke?lang=cz&category=explicit',
            'slovak': '/joke?lang=sk&category=normal',
            'english_uk': '/joke?lang=en-gb&category=normal'
        },
        'rate_limit': os.getenv('RATE_LIMIT', '100 per minute')
    })

@app.route('/joke')
@limiter.limit("200 per minute")
def get_joke():
    """Vrátí náhodný vtip podle parametrů"""
    try:
        # Získání parametrů z URL
        language = request.args.get('lang', 'cz').lower()
        category = request.args.get('category', 'normal').lower()

        # Validace jazyka
        if language not in SUPPORTED_LANGUAGES:
            app.logger.warning(f"Neplatný jazyk požadavek: {language} z IP: {get_remote_address()}")
            return jsonify({
                'error': 'Nepodporovaný jazyk',
                'message': f'Podporované jazyky: {", ".join(SUPPORTED_LANGUAGES)}',
                'requested': language
            }), 400

        # Validace kategorie
        if category not in SUPPORTED_CATEGORIES:
            app.logger.warning(f"Neplatná kategorie požadavek: {category} z IP: {get_remote_address()}")
            return jsonify({
                'error': 'Nepodporovaná kategorie',
                'message': f'Podporované kategorie: {", ".join(SUPPORTED_CATEGORIES)}',
                'requested': category
            }), 400

        # Načtení vtipů
        jokes = load_jokes(language, category)

        if not jokes:
            app.logger.error(f'Žádné vtipy pro jazyk "{language}" a kategorii "{category}"')
            return jsonify({
                'error': 'Žádné vtipy k dispozici',
                'message': f'Pro jazyk "{language}" a kategorii "{category}" nejsou dostupné žádné vtipy.',
                'language': language,
                'category': category
            }), 404

        # Výběr náhodného vtipu
        joke = random.choice(jokes)

        return jsonify({
            'success': True,
            'joke': joke,
            'language': language,
            'category': category,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'service': 'Joker'
        })
    except Exception as e:
        app.logger.error(f"Neočekávaná chyba v get_joke: {str(e)}")
        return jsonify({
            'error': 'Interní chyba serveru',
            'message': 'Něco se pokazilo. Kontaktujte administrátora.'
        }), 500

@app.route('/languages')
@limiter.limit("50 per minute")
def get_languages():
    """Vrátí seznam podporovaných jazyků"""
    return jsonify({
        'success': True,
        'languages': SUPPORTED_LANGUAGES,
        'count': len(SUPPORTED_LANGUAGES)
    })

@app.route('/categories')
@limiter.limit("50 per minute")
def get_categories():
    """Vrátí seznam podporovaných kategorií"""
    return jsonify({
        'success': True,
        'categories': SUPPORTED_CATEGORIES,
        'count': len(SUPPORTED_CATEGORIES)
    })

@app.route('/stats')
@limiter.limit("30 per minute")
def get_stats():
    """Vrátí statistiky o dostupných vtipech"""
    stats = {
        'success': True,
        'total_languages': len(SUPPORTED_LANGUAGES),
        'total_categories': len(SUPPORTED_CATEGORIES),
        'jokes_per_language': {},
        'total_jokes': 0
    }

    for lang in SUPPORTED_LANGUAGES:
        stats['jokes_per_language'][lang] = {}
        for cat in SUPPORTED_CATEGORIES:
            jokes = load_jokes(lang, cat)
            count = len(jokes)
            stats['jokes_per_language'][lang][cat] = count
            stats['total_jokes'] += count

    return jsonify(stats)

@app.route('/health')
@limiter.exempt
def health():
    """Health check endpoint - bez rate limitu pro monitoring"""
    try:
        # Kontrola dostupnosti vtipů
        test_jokes = load_jokes('cz', 'normal')
        healthy = len(test_jokes) > 0

        if healthy:
            return jsonify({
                'status': 'healthy',
                'service': 'Joker',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'version': '2.1.0',
                'cache_size': len(jokes_cache)
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'service': 'Joker',
                'error': 'Žádné vtipy k dispozici'
            }), 503
    except Exception as e:
        app.logger.error(f"Health check selhala: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'Joker',
            'error': str(e)
        }), 503

@app.route('/update-status')
@limiter.limit("10 per minute")
def update_status():
    """Vrátí status auto-update služby"""
    try:
        updater = get_auto_updater()
        if updater:
            status = updater.get_status()
            return jsonify({
                'success': True,
                'auto_update': status,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Auto-update služba není inicializována',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 200
    except Exception as e:
        app.logger.error(f"Chyba při zjišťování update status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handler pro 404 chyby"""
    return jsonify({
        'error': 'Endpoint nenalezen',
        'message': 'Požadovaný endpoint neexistuje. Použijte GET / pro seznam dostupných endpointů.'
    }), 404

@app.errorhandler(429)
def ratelimit_handler(error):
    """Handler pro rate limit překročení"""
    app.logger.warning(f"Rate limit překročen z IP: {get_remote_address()}")
    return jsonify({
        'error': 'Příliš mnoho požadavků',
        'message': 'Překročili jste limit požadavků. Zkuste to později.'
    }), 429

@app.errorhandler(500)
def internal_error(error):
    """Handler pro 500 chyby"""
    app.logger.error(f"Interní chyba serveru: {str(error)}")
    return jsonify({
        'error': 'Interní chyba serveru',
        'message': 'Něco se pokazilo. Kontaktujte administrátora.'
    }), 500

if __name__ == '__main__':
    # Konfigurace serveru
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')

    app.logger.info(f"Spouštím Joker API na {host}:{port}")
    app.run(host=host, port=port, debug=app.config['DEBUG'])
