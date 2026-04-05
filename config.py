import configparser
import pathlib
import sys


def _base_dir() -> pathlib.Path:
    """Ścieżka bazowa — obsługuje zarówno skrypt, jak i PyInstaller .app."""
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys._MEIPASS)
    return pathlib.Path(__file__).parent


def _config_path() -> pathlib.Path:
    """
    Szuka config.ini w dwóch miejscach (kolejność ma znaczenie):
    1. Obok aplikacji — łatwy dostęp z pendrive'a bez wchodzenia w pakiet
    2. Wewnątrz paczki — domyślny fallback

    macOS: sys.executable → Familiada.app/Contents/MacOS/Familiada
           Trzy poziomy wyżej = katalog zawierający .app
    Windows: sys.executable → Familiada/Familiada.exe
             Jeden poziom wyżej = katalog zawierający folder Familiada
    """
    if getattr(sys, "frozen", False):
        if sys.platform == "darwin":
            external = pathlib.Path(sys.executable).parents[3] / "config.ini"
        else:
            # Windows/Linux: exe jest w Familiada/, config obok tego folderu
            external = pathlib.Path(sys.executable).parent / "config.ini"
        if external.exists():
            return external
    return _base_dir() / "config.ini"

PRESETS: dict[str, tuple[int, int, bool]] = {
    "2560x1440": (2560, 1440, True),
    "1920x1080": (1920, 1080, True),
    "1280x720":  (1280,  720, True),
    "1024x768":  (1024,  768, True),
    "windowed":  (1280,  720, False),
    "windowed_1080p": (1920, 1080, False),
}


def _load() -> tuple[int, int, bool]:
    cfg = configparser.ConfigParser()
    cfg.read(_config_path())
    preset = cfg.get("display", "preset", fallback="1920x1080").strip()
    if preset not in PRESETS:
        print(f"[config] Nieznany preset '{preset}', uzywam 1920x1080")
        preset = "1920x1080"
    return PRESETS[preset]


SCREEN_W, SCREEN_H, FULLSCREEN = _load()
