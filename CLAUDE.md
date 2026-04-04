# Familiada — instrukcje dla Claude Code

## Zasada nr 1: aktualizacja memory banku
**Po każdej zmianie w kodzie lub architekturze zaktualizuj odpowiedni plik w memory banku:**
`/home/jan/.claude/projects/-home-jan-Sources-Familiada/memory/`
Sprawdź MEMORY.md, znajdź właściwy plik i uaktualnij go. Jeśli zmiana nie pasuje do żadnego, stwórz nowy wpis i dodaj go do MEMORY.md.

---

## Projekt

**Familiada** — polska wersja teleturnieju Family Feud. Plansza na Python/pygame do użycia przez prowadzącego (host) podczas realnej gry przed publicznością / rzutnikiem.

- Tylko obsługa myszą (host klika, gracze tylko patrzą)
- Fullscreen 1920×1080
- Retro grafika: zielony na czarnym, czcionka VT323
- Undo (cofnij) na każdą akcję

---

## Architektura (pliki)

| Plik | Odpowiedzialność |
|------|-----------------|
| `main.py` | Pętla pygame, dispatcher kliknięć (`handle_click`) |
| `state.py` | Niemutowalne `GameState`, wszystkie akcje zwracają nowy stan |
| `data.py` | Ładuje `rounds/*.json` → lista `Round` obiektów |
| `layout.py` | Stałe pikseli, recty klikalne, kolory |
| `renderer.py` | Funkcje rysujące, ładowanie czcionek |
| `sounds.py` | `SoundManager`, lazy-load z `sounds/`, brak pliku = cicho |
| `rounds/` | Dane rund: `round01.json`, `round02.json`, … |
| `fonts/` | `VT323-Regular.ttf` (bundled) |
| `sounds/` | `*_normalized.mp3` pliki dźwiękowe |

---

## Model stanu (`state.py`)

```python
GameState(frozen=True):
    rounds:      tuple[Round]   # wszystkie rundy, nigdy nie mutowane
    round_index: int
    revealed:    tuple[int]*6   # 0=ukryte, 1=słowo widoczne, 2=pełne
    x_left:      tuple[bool]*3  # X-marki lewa strona
    x_right:     tuple[bool]*3  # X-marki prawa strona
    team1_score: int
    team2_score: int
    phase:       str            # "playing" | "gameover"
```

Akcje: `action_reveal_full`, `action_reveal_score`, `action_add_x_left`, `action_add_x_right`, `action_transfer_to_team`

---

## Format JSON rundy

```json
{
  "pytanie": "Treść pytania (nie wyświetlana na planszy)",
  "odpowiedzi": [
    {"odpowiedz": "Tekst odpowiedzi", "punkty": 35},
    ...
  ]
}
```
- Pliki: `rounds/round01.json`, `round02.json`, … (sortowanie alfabetyczne)
- Maksymalnie 6 odpowiedzi na planszy; krótsze listy uzupełniane pustymi
- Teksty auto-uppercase w `data.py`

---

## Układ ekranu (layout.py)

- Plansza główna: `x=360, y=100, w=1200, h=700`
- 6 rzędów odpowiedzi, `ROW_HEIGHT=90`
- X-strefy lewe: `x=200`, prawe: `x=1590`, 3 strefy po `130×130`
- Duże X (statyczne): lewa/prawa, `390px` wysokości
- Team 1: `Rect(60, 900, 300, 140)`
- Team 2: `Rect(1560, 900, 300, 140)`
- COFNIJ: `Rect(1740, 20, 160, 55)`
- Kolory: `GREEN=(0,230,0)`, `BLACK`, `RED=(220,0,0)`, `YELLOW=(255,220,0)`

---

## Dźwięki (`sounds.py`)

| Metoda | Plik |
|--------|------|
| `play_reveal_score()` | `good_normalized.mp3` |
| `play_wrong()` | `wrong_normalized.mp3` |
| `play_transfer()` / `play_game_over()` | `finish_normalized.mp3` |
| `play_reveal_word()` | `wait_for_it_normalized.mp3` |

Brakujący plik = cicho (nie crashuje). Wszystkie pliki w `sounds/`.

---

## Przepływ gry

1. Start → runda 0, wszystko ukryte
2. Klik na rząd tekstu → `action_reveal_full` (0→2), dźwięk `good`
3. Klik na strefę X → `action_add_x_left/right`, dźwięk `wrong`
4. Klik na team counter → `action_transfer_to_team`, SUMA trafia do drużyny, następna runda
5. Po ostatniej rundzie → phase `"gameover"`, ekran KONIEC GRY
6. Klik na ekranie gameover → restart od nowa

Undo: każda akcja pushuje stary stan na `ctx["history"]`, COFNIJ popuje.

---

## Preferencje użytkownika

- Specyfikacje dla nowych funkcji: **wystarczająco szczegółowe dla AI** (sygnatury funkcji, pixele, pseudokod)
- Plany przed implementacją, pytaj gdy coś niejasne
- Język komunikacji: **polski**
