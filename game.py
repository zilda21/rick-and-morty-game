import sys
import importlib # implemting to dynamically load a Morty class by its name 
from utils import generate_key, hmac_sha256, secure_random #<- I use this to pick random boxes or Rick's first choice
# not sure if this is the best way, but it works for the fairness check


def theoretical_probs(n: int):
    return 1.0 / n, (n - 1.0) / n  

def run_round(round_no, boxes, morty_cls):
   
    k1 = generate_key()
    m1 = secure_random(boxes)       
    h1 = hmac_sha256(k1, m1)
    print(f"\n--- New Round ---")
    print(f"Fairness proof (HMAC K1,m1): {h1}")

    gun_box = m1  

   
    rick_choice = secure_random(boxes)
    print(f"Rick chose box {rick_choice}")

    
    other_boxes = [i for i in range(boxes) if i != rick_choice]

  
    morty = morty_cls()
    h2 = morty.commit(n_minus_one=len(other_boxes))
    print(f"Morty commit (HMAC K2,m2): {h2}")

    r2 = secure_random(len(other_boxes))
    print(f"Game provides r2 = {r2} (0..{len(other_boxes)-1})")
    keep_index_in_others = morty.pick_keep_index(r2, len(other_boxes))
    keep_box = other_boxes[keep_index_in_others]
    print(f"Morty keeps box {keep_box} closed (others would be revealed)")
    
    k2, m2 = morty.reveal()
    ok = (hmac_sha256(k2, m2) == h2)
    print(f"Morty reveal OK: {ok}. K2={k2}, m2={m2}")

    final_choice = keep_box
    print(f"Rick switches to box {final_choice}")

    
    print(f"Gun was in box {gun_box} (K1={k1}, m1={m1})")
    win = (final_choice != gun_box)  
    print("Result:", "Rick survives!" if win else "Rick dies...")

    return {
        "Rnd": round_no,
        "HMAC1": h1[:16],          
        "Rick": rick_choice,
        "Keep": keep_box,
        "Final": final_choice,
        "Gun": gun_box,
        "Win": "Yes" if win else "No",
        "HMAC2": h2[:16],
    }

def start_game():
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

    rounds = 3
    rows = []
    wins = 0
    for r in range(1, rounds + 1):
        row = run_round(r, boxes, morty_cls)
        rows.append(row)
        if row["Win"] == "Yes":
            wins += 1
   
    print("\n--- Results Table ---")
    headers = ["Rnd","HMAC1","Rick","Keep","Final","Gun","Win","HMAC2"]
    line = " | ".join(f"{h:>5}" for h in headers)
    print(line)
    print("-" * len(line))
    for row in rows:
        print(" | ".join([
            f"{row['Rnd']:>5}",
            f"{row['HMAC1']:>5}",
            f"{row['Rick']:>5}",
            f"{row['Keep']:>5}",
            f"{row['Final']:>5}",
            f"{row['Gun']:>5}",
            f"{row['Win']:>5}",
            f"{row['HMAC2']:>5}",
        ]))
    p_stay, p_switch = theoretical_probs(boxes)
    print(f"\n--- Summary ---")
    print(f"Rounds: {rounds}, Wins: {wins}, Losses: {rounds - wins}")
    print(f"Win probability (experiment): {wins/rounds:.2f}")
    print(f"Win probability (calculated): stay={p_stay:.4f}, switch={p_switch:.4f}")

if __name__ == "start_game":
    start_game()
