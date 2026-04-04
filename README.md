# Familiada

Polska wersja teleturnieju Family Feud. Plansza dla prowadzącego (host), obsługa wyłącznie myszą.

---

## Uruchomienie na Mac (bez instalacji)

### 1. Pobierz gotową aplikację

1. Wejdź na [github.com/sochiera/Familiada](https://github.com/sochiera/Familiada) → zakładka **Actions**
2. Kliknij ostatni udany run „Build macOS .app"
3. Na dole strony, sekcja **Artifacts** → pobierz `Familiada-macOS`
4. Wypakuj ZIP — otrzymasz plik `Familiada.app`

### 2. Pierwsze uruchomienie (ominięcie Gatekeepera)

macOS zablokuje aplikację, bo nie jest podpisana cyfrowo. Wystarczy zrobić to **raz**:

1. **Prawy przycisk myszy** na `Familiada.app` → **Otwórz**
2. W oknie ostrzeżenia kliknij **Otwórz**

Jeśli przycisk „Otwórz" nie pojawia się w oknie, otwórz Terminal i wpisz:
```
xattr -cr /path/to/Familiada.app
```
(zastąp `/path/to/` rzeczywistą ścieżką do pliku)

### 3. Rozdzielczość

Aplikacja uruchamia się w trybie **pełnoekranowym**. Domyślna rozdzielczość to **2560×1440** (2K).

Jeśli monitor nie jest 2K, zmień preset **przed** uruchomieniem:

1. Prawy przycisk na `Familiada.app` → **Pokaż zawartość pakietu**
2. Przejdź do `Contents/MacOS/`
3. Otwórz plik `config.ini` dowolnym edytorem tekstu
4. Zmień wartość `preset` na odpowiednią dla monitora:

| preset | rozdzielczość |
|--------|--------------|
| `2560x1440` | fullscreen 2K |
| `1920x1080` | fullscreen Full HD |
| `1280x720` | fullscreen HD |
| `1024x768` | fullscreen 4:3 |
| `windowed` | okno 1280×720 |

### 4. Wyjście z gry

Naciśnij **Escape** lub zamknij okno aplikacji.