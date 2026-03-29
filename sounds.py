class SoundManager:
    """
    Stub SoundManager — all methods are no-ops until sound assets are added.

    To wire up sounds later:
    1. Place MP3/WAV files in the sounds/ directory:
         sounds/reveal.mp3    — played when an answer is revealed
         sounds/wrong.mp3     — played when an X mark is added
         sounds/transfer.mp3  — played when score is transferred to a team
         sounds/gameover.mp3  — played on the KONIEC GRY screen
    2. Initialize pygame.mixer before creating SoundManager.
    3. Replace each pass with:
         pygame.mixer.Sound("sounds/X.mp3").play()
    """

    def play_reveal(self): pass
    def play_wrong(self): pass
    def play_transfer(self): pass
    def play_game_over(self): pass
