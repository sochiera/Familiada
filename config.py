import configparser

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
    cfg.read("config.ini")
    preset = cfg.get("display", "preset", fallback="1920x1080").strip()
    if preset not in PRESETS:
        print(f"[config] Nieznany preset '{preset}', uzywam 1920x1080")
        preset = "1920x1080"
    return PRESETS[preset]


SCREEN_W, SCREEN_H, FULLSCREEN = _load()
