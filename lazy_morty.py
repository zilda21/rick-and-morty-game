from morty_base import MortyBase

class LazyMorty(MortyBase):
      def __init__(self):
        super().__init__()
        print("Lazy Morty yawns... let's see what happens.")
    #instead you can add pass both inputs works for me
