"""
Auto-update služba pro Joker API
Pravidelně kontroluje GitHub pro nové verze a automaticky aktualizuje aplikaci
"""
import os
import sys
import subprocess
import time
import threading
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Konfigurace
UPDATE_CHECK_INTERVAL = int(os.getenv('UPDATE_CHECK_INTERVAL', 48 * 3600))  # 48 hodin v sekundách
AUTO_UPDATE_ENABLED = os.getenv('AUTO_UPDATE_ENABLED', 'true').lower() == 'true'
GIT_BRANCH = os.getenv('GIT_BRANCH', 'main')  # Branch pro kontrolu aktualizací


class AutoUpdater:
    """Auto-update služba pro Joker API"""

    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger('auto_updater')
        self.running = False
        self.thread = None
        self.last_check = None
        self.current_commit = self._get_current_commit()

    def _get_current_commit(self):
        """Získá aktuální commit hash"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            commit = result.stdout.strip()
            self.logger.info(f"Aktuální commit: {commit[:8]}")
            return commit
        except Exception as e:
            self.logger.error(f"Chyba při zjišťování aktuálního commitu: {str(e)}")
            return None

    def _fetch_updates(self):
        """Stáhne informace o aktualizacích z GitHubu"""
        try:
            self.logger.info(f"Kontroluji aktualizace z branch '{GIT_BRANCH}'...")
            result = subprocess.run(
                ['git', 'fetch', 'origin', GIT_BRANCH],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            self.logger.debug(f"Git fetch výstup: {result.stdout}")
            return True
        except subprocess.TimeoutExpired:
            self.logger.error("Git fetch timeout (30s)")
            return False
        except Exception as e:
            self.logger.error(f"Chyba při stahování aktualizací: {str(e)}")
            return False

    def _get_remote_commit(self):
        """Získá commit hash z remote branch"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', f'origin/{GIT_BRANCH}'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            commit = result.stdout.strip()
            self.logger.info(f"Remote commit: {commit[:8]}")
            return commit
        except Exception as e:
            self.logger.error(f"Chyba při zjišťování remote commitu: {str(e)}")
            return None

    def _check_for_updates(self):
        """Kontroluje, zda jsou k dispozici aktualizace"""
        if not self._fetch_updates():
            return False

        remote_commit = self._get_remote_commit()
        if not remote_commit or not self.current_commit:
            self.logger.warning("Nelze porovnat commity")
            return False

        if remote_commit != self.current_commit:
            self.logger.info(f"Nalezena nová verze! {self.current_commit[:8]} -> {remote_commit[:8]}")
            return True
        else:
            self.logger.info("Aplikace je aktuální")
            return False

    def _apply_update(self):
        """Aplikuje aktualizaci (git pull)"""
        try:
            self.logger.info("Stahuji aktualizace...")

            # Git pull
            result = subprocess.run(
                ['git', 'pull', 'origin', GIT_BRANCH],
                capture_output=True,
                text=True,
                check=True,
                timeout=60
            )
            self.logger.info(f"Git pull úspěšný: {result.stdout}")

            # Aktualizace Python závislostí (pro případ nových balíčků)
            self.logger.info("Kontroluji Python závislosti...")
            subprocess.run(
                ['pip', 'install', '-q', '-r', 'requirements.txt'],
                capture_output=True,
                text=True,
                check=True,
                timeout=120
            )
            self.logger.info("Závislosti aktualizovány")

            return True
        except subprocess.TimeoutExpired:
            self.logger.error("Aktualizace timeout")
            return False
        except Exception as e:
            self.logger.error(f"Chyba při aplikaci aktualizace: {str(e)}")
            return False

    def _restart_application(self):
        """Restartuje aplikaci"""
        self.logger.info("Restartuji aplikaci...")

        # Pokud běžíme pod gunicorn, posíláme signal pro restart
        # Gunicorn zachytí SIGHUP a provede graceful restart
        if 'gunicorn' in sys.argv[0] or os.getenv('GUNICORN_PROCESS'):
            try:
                # Graceful reload gunicorn workers
                import signal
                os.kill(os.getppid(), signal.SIGHUP)
                self.logger.info("Poslán SIGHUP signal gunicorn master procesu")
            except Exception as e:
                self.logger.error(f"Chyba při restartování gunicorn: {str(e)}")
        else:
            # Pro vývoj - restart přes os.execv
            try:
                self.logger.info("Restartuji Python proces...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            except Exception as e:
                self.logger.error(f"Chyba při restartování procesu: {str(e)}")

    def _update_cycle(self):
        """Hlavní cyklus pro kontrolu aktualizací"""
        self.logger.info(f"Auto-update služba spuštěna (kontrola každých {UPDATE_CHECK_INTERVAL/3600:.1f} hodin)")

        while self.running:
            try:
                self.last_check = datetime.now()
                self.logger.info(f"Kontrola aktualizací: {self.last_check.strftime('%Y-%m-%d %H:%M:%S')}")

                # Kontrola aktualizací
                if self._check_for_updates():
                    self.logger.info("🔄 Zahajuji automatickou aktualizaci...")

                    # Aplikace aktualizace
                    if self._apply_update():
                        self.logger.info("✅ Aktualizace úspěšně stažena")

                        # Krátké čekání před restartem
                        time.sleep(5)

                        # Restart aplikace
                        self._restart_application()
                    else:
                        self.logger.error("❌ Aktualizace selhala")
                else:
                    self.logger.info("✅ Žádné nové aktualizace")

                # Čekání do další kontroly
                next_check = self.last_check + timedelta(seconds=UPDATE_CHECK_INTERVAL)
                self.logger.info(f"Příští kontrola: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")

                # Spíme po částech, abychom mohli rychle ukončit
                sleep_interval = 60  # Kontrola zastavení každou minutu
                total_slept = 0
                while total_slept < UPDATE_CHECK_INTERVAL and self.running:
                    time.sleep(min(sleep_interval, UPDATE_CHECK_INTERVAL - total_slept))
                    total_slept += sleep_interval

            except Exception as e:
                self.logger.error(f"Chyba v update cyklu: {str(e)}")
                # Počkáme minutu a zkusíme znovu
                time.sleep(60)

    def start(self):
        """Spustí auto-update službu v samostatném vlákně"""
        if not AUTO_UPDATE_ENABLED:
            self.logger.info("Auto-update služba je zakázána (AUTO_UPDATE_ENABLED=false)")
            return

        if self.running:
            self.logger.warning("Auto-update služba již běží")
            return

        # Kontrola git repository
        if not os.path.exists('.git'):
            self.logger.warning("Nejsem v git repository - auto-update zakázán")
            return

        self.running = True
        self.thread = threading.Thread(target=self._update_cycle, daemon=True, name="AutoUpdater")
        self.thread.start()
        self.logger.info("Auto-update služba úspěšně spuštěna")

    def stop(self):
        """Zastaví auto-update službu"""
        if not self.running:
            return

        self.logger.info("Zastavuji auto-update službu...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info("Auto-update služba zastavena")

    def get_status(self):
        """Vrátí status auto-update služby"""
        return {
            'enabled': AUTO_UPDATE_ENABLED,
            'running': self.running,
            'current_commit': self.current_commit[:8] if self.current_commit else None,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'check_interval_hours': UPDATE_CHECK_INTERVAL / 3600,
            'branch': GIT_BRANCH
        }


# Globální instance auto-updater
_auto_updater = None


def init_auto_updater(app=None):
    """Inicializuje a spustí auto-updater"""
    global _auto_updater
    if _auto_updater is None:
        _auto_updater = AutoUpdater(app)
        _auto_updater.start()
    return _auto_updater


def get_auto_updater():
    """Vrátí globální instanci auto-updater"""
    return _auto_updater
