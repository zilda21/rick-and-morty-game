import sys
import importlib
from utils import generate_key, hmac_sha3_256, secure_random

def ask_int(prompt: str, lo: int, hi_inclusive: int) -> int:
    while True:
        try:
            v = int(input(f"{prompt} ({lo}..{hi_inclusive}): ").strip())
            if lo <= v <= hi_inclusive:
                return v
            print(f"Invalid choice. Enter a number between {lo} and {hi_inclusive}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_round(round_no, boxes, morty_cls):
    print(f"\n--- New Round ---")

    k1 = generate_key()
    m1 = secure_random(boxes)              
    h1 = hmac_sha3_256(k1, m1)             
    print(f"HMAC1 (K1,m1) = {h1}")
    r1 = ask_int("Rick, enter your number for fair gen [r1]", 0, boxes - 1)
    gun_box = (m1 + r1) % boxes            

   
    guess = ask_int("Rick, what is your box guess?", 0, boxes - 1)
    print(f"Rick chose box {guess}")

    
    other_boxes = [i for i in range(boxes) if i != guess]
    morty = morty_cls()

    keep_box = None
    h2 = k2 = m2 = r2 = None

    if morty_cls.__name__ == "ClassicMorty":
      
        k2 = generate_key()
        m2 = secure_random(len(other_boxes))
        h2 = hmac_sha3_256(k2, m2)
        print(f"HMAC2 (K2,m2) = {h2}")

        r2 = ask_int("Rick, enter your number for fair gen [r2]", 0, len(other_boxes) - 1)
        idx = (m2 + r2) % len(other_boxes)

        keep_box = gun_box if guess != gun_box else other_boxes[idx]
        print(f"Morty keeps box {keep_box} closed (others would be revealed).")
    else:
      
        keep_box = gun_box if guess != gun_box else min(other_boxes)
        print(f"Morty (lazy) keeps box {keep_box} closed (no randomness).")

    sw = input("Switch to the other closed box? (y/n): ").strip().lower()
    final_choice = keep_box if sw == "y" else guess
    print(f"Rick {'switches' if sw == 'y' else 'stays'} → final box {final_choice}")

 
    print(f"Reveal #1: m1={m1}, r1={r1}, K1={k1}")
    print(f"Check: (m1 + r1) % {boxes} = {(m1 + r1) % boxes}")
    if h1 != hmac_sha3_256(k1, m1):
        print("WARNING: HMAC1 mismatch!")

    if morty_cls.__name__ == "ClassicMorty":
        print(f"Reveal #2: m2={m2}, r2={r2}, K2={k2}")
        print(f"Check: (m2 + r2) % {len(other_boxes)} = {(m2 + r2) % len(other_boxes)}")
        if h2 != hmac_sha3_256(k2, m2):
            print("WARNING: HMAC2 mismatch!")

   
    print(f"Gun was in box {gun_box}")
    win = (final_choice != gun_box)    
    print("Result:", "Rick survives!" if win else "Rick dies...")

  
    short = lambda s: s[:16] if s else "-"
    return {
        "Rnd": round_no,
        "HMAC1": short(h1),
        "m1+r1 mod N": (m1 + r1) % boxes,
        "Guess": guess,
        "Keep": keep_box,
        "Final": final_choice,
        "Gun": gun_box,
        "Win": "Yes" if win else "No",
        "HMAC2": short(h2),
    }

def main():
    if len(sys.argv) < 3:
        print("Error: Missing arguments.\nUsage: python game.py <boxes> <MortyClass>\nExample: python game.py 3 classic_morty.ClassicMorty")
        return

    try:
        boxes = int(sys.argv[1])
    except ValueError:
        print("Error: First argument must be an integer (number of boxes).")
        return
    if boxes <= 2:
        print("Error: Number of boxes must be greater than 2.")
        return

    morty_path = sys.argv[2]
    try:
        module_name, class_name = morty_path.split(".")
        mod = importlib.import_module(module_name)
        morty_cls = getattr(mod, class_name)
    except Exception:
        print(f"Error: Morty implementation '{morty_path}' not found.")
        return

    print(f"\n=== Rick & Morty Game ===")
    print(f"Boxes: {boxes}, Morty: {morty_path}")

    rows, wins, rounds_played = [], 0, 0
    while True:
        rounds_played += 1
        row = run_round(rounds_played, boxes, morty_cls)
        rows.append(row)
        if row["Win"] == "Yes":
            wins += 1

       
        again = input("Play another round? (y/n): ").strip().lower()
        if again != "y":
            break

   
    try:
        from tabulate import tabulate
        print("\n--- Results Table ---")
        headers = ["Rnd","HMAC1","m1+r1 mod N","Guess","Keep","Final","Gun","Win","HMAC2"]
        data = [[row[h] for h in headers] for row in rows]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    except Exception:
        print("\n--- Results Table (plain) ---")
        headers = ["Rnd","HMAC1","m1+r1 mod N","Guess","Keep","Final","Gun","Win","HMAC2"]
        line = " | ".join(f"{h:>10}" for h in headers)
        print(line)
        print("-" * len(line))
        for row in rows:
            print(" | ".join(f"{str(row[h]):>10}" for h in headers))

   
    p_stay, p_switch = morty_cls().theoretical_probabilities(boxes)
    print(f"\n--- Summary ---")
    print(f"Rounds: {rounds_played}, Wins: {wins}, Losses: {rounds_played - wins}")
    print(f"Win probability (experiment): {wins/rounds_played:.2f}")
    print(f"Win probability (calculated by {morty_cls.__name__}): stay={p_stay:.4f}, switch={p_switch:.4f}")

if __name__ == "__main__":
    main()
