#!/usr/bin/env python3
"""
Jednoduchý test skript pro lokální testování Joke API
Spusť: python test_local.py
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def print_test(name, result):
    """Vytiskne výsledek testu"""
    print(f"\n{'='*60}")
    print(f"📝 {name}")
    print('='*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))

def test_api():
    """Spustí všechny testy"""
    print("🧪 Testování Joke API...")
    print(f"🌐 Base URL: {BASE_URL}")
    
    try:
        # Test 1: Základní informace
        response = requests.get(f"{BASE_URL}/")
        print_test("Test 1: Základní informace (GET /)", response.json())
        
        sleep(0.5)
        
        # Test 2: Český normální vtip
        response = requests.get(f"{BASE_URL}/joke?lang=cz&category=normal")
        print_test("Test 2: Český normální vtip", response.json())
        
        sleep(0.5)
        
        # Test 3: Český explicitní vtip
        response = requests.get(f"{BASE_URL}/joke?lang=cz&category=explicit")
        print_test("Test 3: Český explicitní vtip", response.json())
        
        sleep(0.5)
        
        # Test 4: Slovenský vtip
        response = requests.get(f"{BASE_URL}/joke?lang=sk&category=normal")
        print_test("Test 4: Slovenský vtip", response.json())
        
        sleep(0.5)
        
        # Test 5: Anglický vtip (UK)
        response = requests.get(f"{BASE_URL}/joke?lang=en-gb&category=normal")
        print_test("Test 5: Anglický vtip (UK)", response.json())
        
        sleep(0.5)
        
        # Test 6: Anglický vtip (US)
        response = requests.get(f"{BASE_URL}/joke?lang=en-us&category=normal")
        print_test("Test 6: Anglický vtip (US)", response.json())
        
        sleep(0.5)
        
        # Test 7: Default parametry (bez specifikace)
        response = requests.get(f"{BASE_URL}/joke")
        print_test("Test 7: Default parametry (cz, normal)", response.json())
        
        sleep(0.5)
        
        # Test 8: Seznam jazyků
        response = requests.get(f"{BASE_URL}/languages")
        print_test("Test 8: Seznam jazyků", response.json())
        
        sleep(0.5)
        
        # Test 9: Seznam kategorií
        response = requests.get(f"{BASE_URL}/categories")
        print_test("Test 9: Seznam kategorií", response.json())
        
        sleep(0.5)
        
        # Test 10: Health check
        response = requests.get(f"{BASE_URL}/health")
        print_test("Test 10: Health check", response.json())
        
        sleep(0.5)
        
        # Test 11: Neplatný jazyk (očekává se error)
        response = requests.get(f"{BASE_URL}/joke?lang=invalid")
        print_test("Test 11: Neplatný jazyk (očekává se error)", response.json())
        
        sleep(0.5)
        
        # Test 12: Neplatná kategorie (očekává se error)
        response = requests.get(f"{BASE_URL}/joke?category=invalid")
        print_test("Test 12: Neplatná kategorie (očekává se error)", response.json())
        
        print(f"\n{'='*60}")
        print("✅ Všechny testy dokončeny!")
        print('='*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ CHYBA: Nelze se připojit k API!")
        print(f"   Ujisti se, že API běží na {BASE_URL}")
        print("   Spusť API pomocí: python app.py")
    except Exception as e:
        print(f"\n❌ CHYBA: {str(e)}")

if __name__ == "__main__":
    test_api()
