import pathlib

import pygame


class SoundManager:
    """
    Loads and plays sound effects from the sounds/ directory.
    Missing files are silently ignored so the game always runs.

    Available files used:
      sounds/wait_for_it.mp3  — word revealed (step 1)
      sounds/good.mp3         — full answer revealed (step 2)
      sounds/wrong.mp3        — X mark added
      sounds/finish.mp3       — score transferred to a team / round end
    """

    def __init__(self) -> None:
        self._cache: dict = {}

    def _play(self, filename: str) -> None:
        path = pathlib.Path("sounds") / filename
        if not path.exists():
            return
        if filename not in self._cache:
            try:
                self._cache[filename] = pygame.mixer.Sound(str(path))
            except Exception:
                return
        self._cache[filename].play()

    def play_reveal_word(self):  self._play("wait_for_it.mp3")
    def play_reveal_score(self): self._play("good.mp3")
    def play_wrong(self):        self._play("wrong.mp3")
    def play_transfer(self):     self._play("finish.mp3")
    def play_game_over(self):    self._play("finish.mp3")
