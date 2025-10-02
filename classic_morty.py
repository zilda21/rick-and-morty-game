# classic_morty.py
from morty_base import MortyBase

class ClassicMorty(MortyBase):
    def __init__(self):
        super().__init__()
        print("Classic Morty is playing...")

    # ClassicMorty never removes the gun → default probabilities are correct.
