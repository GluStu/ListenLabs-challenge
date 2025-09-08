import requests 

# Best so far       |    target 
# 394 rank          |    ????
# 815 rejections    |    sub 800
# 55.1% accuracy    |    dc

# Potential strat: in the best one still got like 16 overshoot of each. So maybe reucing yng and wd by 10-15 pts each, 
# a dynamic changer, calculate the expected value left (keep in ming the corr while calculating) and start allowing all post that and 
# expected reduction 810-815 maybe (givena  good run)
# also can add a shifter too like if the % of wd or yng to have more if under the % of ovrall (maybe not, will reduce eff)
# And increase by 1 instead of 1.02 and change 580 to 567 (580/1.02) -> var subjected to change

# === CONFIG ===
BASE_URL = "https://berghain.challenges.listenlabs.ai"
PLAYER_ID = "58d7599f-44a1-46b3-937d-8a23a69a45bd"
SCENARIO = 1

# === START NEW GAME ===
print("Starting new game...")
try:
    res = requests.get(f"{BASE_URL}/new-game?scenario={SCENARIO}&playerId={PLAYER_ID}")
    res.raise_for_status()
    game = res.json()
except Exception as e:
    print("❌ Failed to start game:", e)
    exit(1)

game_id = game["gameId"]
constraints = game["constraints"]
rel_freq = game["attributeStatistics"]["relativeFrequencies"]

print(f"Game ID: {game_id}")


# === FIRST PERSON (index 0): no decision yet ===
try:
    url = f"{BASE_URL}/decide-and-next?gameId={game_id}&personIndex=0"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    current_person = data["nextPerson"]
except Exception as e:
    print("❌ Failed to get first person:", e)
    exit(1)

# === GAME LOOP ===
person_index = 0  # next person to retrieve
cmp = False
yng = 0
wd = 0
while True:
    try:
        # Decide for the previous person
        attrs = current_person["attributes"]
        is_young = attrs.get("young", False)
        if is_young:
            yng += 1.02
        is_well_dressed = attrs.get("well_dressed", False)
        if is_well_dressed:
            wd += 1.02
        if yng >= 580 or wd >= 580:
            cmp = True
        accept = is_young or is_well_dressed or cmp
        decision = "ACCEPT" if accept else "REJECT"

        print(f"[{current_person['personIndex']}] Young: {is_young}, Well Dressed: {is_well_dressed} => {decision}, yng cnt: {yng}, wd cnt: {wd}")

        # Now make the decision and get the next person
        url = f"{BASE_URL}/decide-and-next?gameId={game_id}&personIndex={person_index}&accept={str(accept).lower()}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        current_person = data["nextPerson"]
        person_index += 1

    except requests.exceptions.RequestException as e:
        print("❌ HTTP request failed:", e)
        break
    except Exception as e:
        print("❌ Unexpected error:", e)
        break