import importlib
from utils import generate_key, hmac_sha3_256, secure_random
from terminaltables import AsciiTable


def run_round(n_boxes: int, morty_cls) -> tuple:
   
    k1 = generate_key()
    m1 = secure_random(n_boxes)
    h1 = hmac_sha3_256(k1, m1)

    print(f"Morty: HMAC1={h1}")
    while True:
        try:
            r1 = int(input(f"Morty: Rick, enter your number [0,{n_boxes}) so you don’t whine later that I cheated, alright? "))
            if 0 <= r1 < n_boxes:
                break
            else:
                print(f"Morty: Uh… enter a number in [0,{n_boxes}) please.")
        except ValueError:
            print("Morty: That's not even a number, Rick!")

    guess = int(input(f"Morty: Okay, okay, I hid the gun. What’s your guess [0,{n_boxes})? "))
    print(f"Rick: {guess}")

    morty = morty_cls()
    keep, gun_box = morty.play(n_boxes, guess)

    k2 = generate_key()
    m2 = secure_random(n_boxes - 1)
    h2 = hmac_sha3_256(k2, m2)

    print("Morty: Let’s, uh, generate another value now, I mean, to select a box to keep in the game.")
    print(f"Morty: HMAC2={h2}")
    while True:
        try:
            r2 = int(input(f"Morty: Rick, enter your number [0,{n_boxes-1}), and, uh, don’t say I didn’t play fair, okay? "))
            if 0 <= r2 < (n_boxes - 1):
                break
            else:
                print(f"Morty: Uh… enter a number in [0,{n_boxes-1}) please.")
        except ValueError:
            print("Morty: That’s not even a number, Rick!")

    print(f"Morty: I'm keeping the box you chose, I mean {guess}, and the box {keep}.")
    choice = int(input("Morty: You can switch your box (enter 0), or, you know, stick with it (enter 1).  "))
    final_box = keep if choice == 0 else guess

   
    print(f"Morty: Aww man, my 1st random value is {m1}.")
    print(f"Morty: KEY1={k1.hex()}")
    print(f"Morty: So the 1st fair number is ({r1} + {m1}) % {n_boxes} = {(r1 + m1) % n_boxes}.")

    print(f"Morty: Aww man, my 2nd random value is {m2}.")
    print(f"Morty: KEY2={k2.hex()}")
    print(f"Morty: Uh, okay, the 2nd fair number is ({r2} + {m2}) % {n_boxes-1} = {(r2 + m2) % (n_boxes-1)}")

    print(f"Morty: Your portal gun is in the box {gun_box}.")
    if final_box == gun_box:
        print("Morty: Whoa, Rick survives!")
        return choice == 0, True
    else:
        print("Morty: Aww man, you lost, Rick. Now we gotta go on one of *my* adventures!")
        return choice == 0, False


def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python game.py <num_boxes> <morty_class>")
        return

    try:
        n_boxes = int(sys.argv[1])
        if n_boxes < 3:
            raise ValueError
    except ValueError:
        print("Number of boxes must be an integer >= 3.")
        return

    morty_module, morty_class = sys.argv[2].rsplit(".", 1)
    morty_cls = getattr(importlib.import_module(morty_module), morty_class)

    print("\n=== Rick & Morty Game ===")
    print(f"Boxes: {n_boxes}, Morty: {sys.argv[2]}")

    rounds = {"switch": {"rounds": 0, "wins": 0},
              "stay": {"rounds": 0, "wins": 0}}

    while True:
        did_switch, win = run_round(n_boxes, morty_cls)
        if did_switch:
            rounds["switch"]["rounds"] += 1
            if win:
                rounds["switch"]["wins"] += 1
        else:
            rounds["stay"]["rounds"] += 1
            if win:
                rounds["stay"]["wins"] += 1

        again = input("Morty: D-do you wanna play another round (y/n)? ").strip().lower()
        if again != "y":
            break


    table_data = [
        ["Game results", "Rick switched", "Rick stayed"],
        ["Rounds", rounds["switch"]["rounds"], rounds["stay"]["rounds"]],
        ["Wins", rounds["switch"]["wins"], rounds["stay"]["wins"]],
        ["P (estimate)",
         f"{(rounds['switch']['wins'] / rounds['switch']['rounds']):.3f}" if rounds['switch']['rounds'] > 0 else "?",
         f"{(rounds['stay']['wins'] / rounds['stay']['rounds']):.3f}" if rounds['stay']['rounds'] > 0 else "?"],
        ["P (exact)", f"{(n_boxes - 1) / n_boxes:.3f}", f"{1 / n_boxes:.3f}"]
    ]

    table = AsciiTable(table_data, "GAME STATS")
    print(table.table)


if __name__ == "__main__":
    main()
