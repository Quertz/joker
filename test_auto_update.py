#!/usr/bin/env python3
"""
Test script pro auto-update funkčnost
"""
import sys
import os
from auto_update import AutoUpdater
import logging

# Nastavení loggingu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_auto_updater():
    """Test auto-updater funkcí"""
    print("🧪 Testování Auto-Update služby")
    print("=" * 50)

    # Vytvoření instance
    updater = AutoUpdater()

    # Test 1: Získání aktuálního commitu
    print("\n1. Test: Získání aktuálního commitu")
    current = updater._get_current_commit()
    if current:
        print(f"   ✅ Aktuální commit: {current[:8]}")
    else:
        print("   ❌ Nepodařilo se získat aktuální commit")
        return False

    # Test 2: Fetch aktualizací
    print("\n2. Test: Fetch aktualizací z GitHubu")
    if updater._fetch_updates():
        print("   ✅ Fetch úspěšný")
    else:
        print("   ⚠️  Fetch selhal (může být nedostupná síť)")

    # Test 3: Získání remote commitu
    print("\n3. Test: Získání remote commitu")
    remote = updater._get_remote_commit()
    if remote:
        print(f"   ✅ Remote commit: {remote[:8]}")
    else:
        print("   ⚠️  Nepodařilo se získat remote commit")

    # Test 4: Porovnání verzí
    print("\n4. Test: Porovnání verzí")
    if current and remote:
        if current == remote:
            print(f"   ✅ Aplikace je aktuální ({current[:8]})")
        else:
            print(f"   📦 Nová verze k dispozici!")
            print(f"      Aktuální: {current[:8]}")
            print(f"      Remote:   {remote[:8]}")

    # Test 5: Status
    print("\n5. Test: Získání statusu")
    status = updater.get_status()
    print(f"   ✅ Status:")
    print(f"      - Enabled: {status['enabled']}")
    print(f"      - Running: {status['running']}")
    print(f"      - Current commit: {status['current_commit']}")
    print(f"      - Check interval: {status['check_interval_hours']} hodin")
    print(f"      - Branch: {status['branch']}")

    print("\n" + "=" * 50)
    print("✅ Všechny testy dokončeny!")
    return True

if __name__ == '__main__':
    try:
        success = test_auto_updater()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Chyba při testování: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
