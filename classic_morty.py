import random

class ClassicMorty:
    def play(self, n_boxes: int, guess: int) -> tuple:
        """
        Classic Morty:
        - Never removes the box with the portal gun.
        - If Rick guessed correctly, he picks a random other box to keep.
        - If Rick guessed wrong, he always keeps the gun box hidden.
        """
        print("Classic Morty is playing...")
        
        
        gun_box = random.randint(0, n_boxes - 1)

        if guess == gun_box:
           
            keep = random.choice([i for i in range(n_boxes) if i != guess])
        else:
           
            keep = gun_box

        return keep, gun_box
