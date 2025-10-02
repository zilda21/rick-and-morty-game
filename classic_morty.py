from morty_base import MortyBase

# ClassicMorty behaves same as base, but could be extended...

class ClassicMorty(MortyBase):
 def __init__(self):
        super().__init__()
        print("Classic Morty is playing...")
