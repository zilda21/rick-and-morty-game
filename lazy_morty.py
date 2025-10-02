class LazyMorty:
    def play(self, n_boxes: int, guess: int) -> tuple:
        """
        Lazy Morty:
        - Never removes the box with the portal gun.
        - Always keeps the lowest possible index box.
        """
        print("Lazy Morty yawns... let's see what happens.")
        
     
        gun_box = 0

        keep = 0 if guess != 0 else 1

        return keep, gun_box
