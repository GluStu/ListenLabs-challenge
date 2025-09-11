import requests

#intl 15 prob?? 

BASE_URL = "https://berghain.challenges.listenlabs.ai"
PLAYER_ID = "" #Player Id
SCENARIO = 3
person_index = 0


print("Starting new game...")
try:
    res = requests.get(f"{BASE_URL}/new-game?scenario={SCENARIO}&playerId={PLAYER_ID}")
    res.raise_for_status()
    game = res.json()
except Exception as e:
    print("Failed to start game:", e)
    exit(1)

game_id = game["gameId"]
constraints = game["constraints"]

print(f"Game ID: {game_id}")

try:
    url = f"{BASE_URL}/decide-and-next?gameId={game_id}&personIndex=0"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    current_person = data["nextPerson"]
except Exception as e:
    print("Failed to get first person:", e)
    exit(1)

# attributes in order: T, W, C, B
MIN_REQ = {"U": 500, "I": 650, "F": 550, "Q": 250, "V": 200, "G": 800}
K = 1000

accepted = 0
acc_attr = {"U": 0, "I": 0, "F": 0, "Q": 0, "V": 0, "G": 0}
attrs = ["U", "I", "F", "Q", "V", "G"]

def decide(candidate):
    global accepted, acc_attr
    attrs = ["U", "I", "F", "Q", "V", "G"]

    S = K - accepted
    r = {j: max(0, MIN_REQ[j] - acc_attr[j]) for j in MIN_REQ}
    
    if all(acc_attr[a] >= MIN_REQ[a] for a in attrs):
        return True

    # 1) hard locks: if any attribute needs exactly S more, it is mandatory
    locked = [j for j in r if r[j] == S and r[j] > 0]
    if locked and not all(candidate.get(j, 0) == 1 for j in locked):
        return False  # <-- reject if a hard-locked attribute is missing

    # 1b) single-unmet rule: if exactly one attribute is still unmet, require it
    unmet = [j for j, need in r.items() if need > 0]
    if len(unmet) == 1 and candidate.get(unmet[0], 0) == 0:
        return False

    # 2) mandatory pair guardrail
    attrs = ["U", "I", "F", "Q", "V", "G"]
    for i in range(len(attrs)):
        for j in range(i + 1, len(attrs)):
            ni = attrs[i]; nj = attrs[j]
            need_pair = max(0, r[ni] + r[nj] - S)
            if need_pair > 0 and candidate.get(ni, 0) == 0 and candidate.get(nj, 0) == 0:
                return False
    
    # 3) greedy accept
    accepted += 1
    for j in MIN_REQ:
        if candidate.get(j, 0) == 1:
            acc_attr[j] += 1
    return True

while True:
    try:
        attrs = current_person["attributes"]
        underground_veteran = attrs.get("underground_veteran", False)
        international = attrs.get("international", False)
        fashion_forward = attrs.get("fashion_forward", False)
        queer_friendly = attrs.get("queer_friendly", False)
        vinyl_collector = attrs.get("vinyl_collector", False)
        german_speaker = attrs.get("german_speaker", False)
        cand = {
        "U": underground_veteran,
        "I": international,
        "F": fashion_forward,
        "Q": queer_friendly,
        "V": vinyl_collector,
        "G": german_speaker,
        }
        accept = decide(cand)

        if not accept and (vinyl_collector or queer_friendly):
            accept = True
            accepted += 1
            if vinyl_collector:
                acc_attr["V"] += 1
            if queer_friendly:
                acc_attr["Q"] += 1
        decision = "accept" if accept else "reject"

        print(f"[{current_person['personIndex']}] underground: {underground_veteran}, international: {international}, fashion: {fashion_forward}, queer: {queer_friendly}, vinyl: {vinyl_collector}, german: {german_speaker} => {decision}")


        url = f"{BASE_URL}/decide-and-next?gameId={game_id}&personIndex={person_index}&accept={str(accept).lower()}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        current_person = data["nextPerson"]
        person_index += 1

    except requests.exceptions.RequestException as e:
        print("HTTP request failed:", e)
        break
    except Exception as e:
        print("Unexpected error:", e)
        break
