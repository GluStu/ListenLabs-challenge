# ListenLabs-challenge

# Description:
## Berghain Challenge
You're the bouncer at a night club. Your goal is to fill the venue with N=1000 people while satisfying constraints like "at least 40% Berlin locals", or "at least 80% wearing all black". People arrive one by one, and you must immediately decide whether to let them in or turn them away. Your challenge is to fill the venue with as few rejections as possible while meeting all minimum requirements.


## How it works
- People arrive sequentially with binary attributes (e.g., female/male, young/old, regular/new)
- You must make immediate accept/reject decisions
- The game ends when either:
(a) venue is full (1000 people)
(b) you rejected 20,000 people


## Scenarios & Scoring
There are 3 different scenarios. For each, you are given a list of constraints and statistics on the attribute distribution. You can assume participants are sampled i.i.d., meaning the attribute distribution will not change as the night goes on. You know the overall relative frequency of each attribute and the correlation between attributes. You don't know the exact distribution.
You score is the number of people you rejected before filling the venue (the less the better).

## Ouptcome
It was a bit luck-based (at least my strategy). Wanted to finish top 100, reached 97 towards the end; by the time all of the people completed their simulations, I was pushed back to 125. 🙃

<img width="908" height="67" alt="image" src="https://github.com/user-attachments/assets/1c97b8be-1bd3-40d6-8553-76a9a23c8940" />

Overall, great exp,,, 10/10 will do it again
