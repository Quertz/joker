#!/usr/bin/env python3
"""
Test script pro kontrolu víceřádkových vtipů
"""

def test_multiline_jokes():
    """Otestuje načítání víceřádkových vtipů"""
    filename = "jokes/cz_normal_test.txt"

    print(f"📖 Načítám vtipy z: {filename}\n")

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        jokes = [joke.strip() for joke in content.split('\n\n') if joke.strip()]

    print(f"✅ Načteno celkem {len(jokes)} vtipů\n")
    print("=" * 60)

    for i, joke in enumerate(jokes, 1):
        print(f"\n🎭 Vtip #{i}:")
        print("-" * 60)
        print(joke)
        print("-" * 60)
        print(f"Počet řádků: {joke.count(chr(10)) + 1}")
        print(f"Délka: {len(joke)} znaků")

    print("\n" + "=" * 60)
    print("\n✨ Test dokončen!")

    # Ukázka JSON výstupu (jako z API)
    print("\n📡 Simulace JSON odpovědi z API:")
    print("-" * 60)
    import json
    if jokes:
        sample_joke = jokes[0]
        response = {
            'success': True,
            'joke': sample_joke,
            'language': 'cz',
            'category': 'normal'
        }
        print(json.dumps(response, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    test_multiline_jokes()
