# save this as convert.py
import json
import time
import random

PUSH_CHARS = "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"

last_push_time = 0
last_rand_chars = [0] * 12


def generate_push_id(now: int = None) -> str:
    global last_push_time, last_rand_chars

    if now is None:
        now = int(time.time() * 1000)  # current time in ms

    duplicate_time = (now == last_push_time)
    last_push_time = now

    # Timestamp part
    time_stamp_chars = []
    timestamp = now
    for _ in range(8):
        time_stamp_chars.insert(0, PUSH_CHARS[timestamp % 64])
        timestamp //= 64
    push_id = "".join(time_stamp_chars)

    # Randomness part
    if not duplicate_time:
        last_rand_chars = [random.randint(0, 63) for _ in range(12)]
    else:
        # If same ms, increment the last random number
        i = 11
        while i >= 0 and last_rand_chars[i] == 63:
            last_rand_chars[i] = 0
            i -= 1
        if i >= 0:
            last_rand_chars[i] += 1

    push_id += "".join(PUSH_CHARS[i] for i in last_rand_chars)

    return push_id


# ---- Main Script ----

# Load your JSON file (must be an array of objects)
with open("bags.json", "r", encoding="utf-8") as f:
    input_data = json.load(f)

output_data = {}
for item in input_data:
    key = generate_push_id()
    output_data[key] = item

# Save to new JSON file
with open("firebase_ready.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("✅ Done! Check firebase_ready.json")
