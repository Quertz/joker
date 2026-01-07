# 📝 Formát TXT souborů s vtipy

## Jak správně zapsat vtipy s odřádkováním

### ✅ Základní pravidla

1. **Jeden vtip = jeden blok textu**
2. **Vtipy jsou oddělené PRÁZDNÝM ŘÁDKEM** (dvojité odřádkování `\n\n`)
3. **Uvnitř vtipu můžete použít odřádkování** (jednoduché `\n`)
4. API automaticky zachová všechna odřádkování uvnitř vtipu

---

## 📖 Příklady

### Jednoduchý vtip (1 řádek)

```
Co je to zelený a skáče po lese? Okurka na dovolené.
```

### Vtip s odřádkováním (2+ řádky)

```
Co je to zelený a skáče po lese?
Okurka na dovolené.
```

### Více vtipů v jednom souboru

```
Co je to zelený a skáče po lese?
Okurka na dovolené.

Proč se hroši neumí dívat nahoru?
Protože mají velké břicho.

Setkají se dva programátoři.
První říká: "Ahoj!"
Druhý odpovídá: "Svět!"
```

**DŮLEŽITÉ:** Mezi vtipy musí být **prázdný řádek**!

---

## 🔧 Jak API zpracovává vtipy

### Načítání

```python
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
    jokes = [joke.strip() for joke in content.split('\n\n') if joke.strip()]
```

### JSON odpověď z API

```json
{
  "success": true,
  "joke": "Co je to zelený a skáče po lese?\nOkurka na dovolené.",
  "language": "cz",
  "category": "normal"
}
```

Znak `\n` v JSON reprezentuje odřádkování, které se zobrazí ve frontendové aplikaci.

---

## ❌ Časté chyby

### ❌ ŠPATNĚ - Vtipy bez prázdného řádku

```
Co je to zelený?
Okurka.
Proč hroši?
Břicho.
```

Toto bude načteno jako **JEDEN** vtip se 4 řádky!

### ✅ SPRÁVNĚ - S prázdným řádkem

```
Co je to zelený?
Okurka.

Proč hroši?
Břicho.
```

Toto bude načteno jako **DVA** samostatné vtipy.

---

## 🎯 Doporučení

1. Pro jednoduché vtipy použijte 1 řádek
2. Pro vtipy s dialogem nebo pointou použijte odřádkování
3. Vždy oddělujte vtipy prázdným řádkem
4. Soubor ukončete prázdným řádkem (není nutné, ale doporučené)
5. Použijte UTF-8 kódování pro správné zobrazení českých znaků

---

## 🧪 Test

Spusťte test script pro ověření formátu:

```bash
python3 test_multiline.py
```

Tento script načte a zobrazí všechny vtipy z testovacího souboru včetně odřádkování.
