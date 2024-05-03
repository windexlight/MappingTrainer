
words = [
    ("the", 164.4472319),
    ("of", 93.48264599),
    ("and", 92.3858634),
    ("to", 86.26840189),
    ("a", 64.54804845),
    ("in", 60.19965264),
    ("for", 42.17343569),
    ("is", 33.44793927),
    ("on", 26.65761935),
    ("that", 24.16706865),
    ("by", 23.81180013),
    ("this", 22.94762849),
    ("with", 22.62522073),
    ("i", 21.93656937),
    ("you", 21.29654416),
    ("it", 19.99567722),
    ("not", 18.71855363),
    ("or", 18.41471072),
    ("be", 17.0498827),
    ("are", 17.01356639),
    ("from", 16.17469591),
    ("at", 16.15107933),
    ("as", 15.97451185),
    ("your", 14.65695527),
    ("all", 14.37543496),
    ("have", 11.11819101),
    ("new", 11.02618564),
    ("more", 10.98007693),
    ("an", 10.79168221),
    ("was", 10.54405728),
    ("we", 9.884680722),
    ("will", 9.640394614),
    ("home", 9.075732873),
    ("can", 8.830306658),
    ("us", 8.736405114),
    ("about", 8.719498158),
    ("if", 8.067376396),
    ("my", 7.532901926),
    ("has", 7.43713399),
    ("but", 7.107183096),
    ("our", 7.09906821),
    ("one", 7.061955389),
    ("other", 6.954943791),
    ("do", 6.75784469),
    ("no", 6.660897235),
    ("time", 6.458985),
    ("they", 6.277863334),
    ("he", 5.990870668),
    ("up", 5.89933628),
    ("may", 5.884073196),
    ("what", 5.774423588),
    ("which", 5.761050103),
    ("their", 5.564412467),
    ("out", 5.271229094),
    ("use", 5.117545038),
    ("any", 5.051875439),
    ("there", 4.983845138),
    ("see", 4.84339435),
    ("only", 4.704319359),
    ("so", 4.704073746),
    ("his", 4.692474882),
    ("when", 4.624547893),
    ("here", 4.547000886),
    ("who", 4.484565694),
    ("also", 4.384361869),
    ("now", 4.345680654),
    ("help", 4.343308735),
    ("get", 4.30727507),
    ("view", 4.280939077),
    ("first", 4.109512319),
    ("been", 4.087178164),
    ("would", 4.07029524),
    ("how", 4.064636878),
    ("were", 4.056473303),
    ("me", 4.027459637),
    ("some", 3.90102287),
    ("these", 3.845400227),
    ("its", 3.736107613),
    ("like", 3.700266259),
    ("than", 3.572494629),
    ("find", 3.568469875),
    ("date", 3.475529411),
    ("back", 3.468824781),
    ("top", 3.441741293),
    ("people", 3.413946611),
    ("had", 3.413444467),
    ("list", 3.35912529),
    ("name", 3.301850295),
    ("just", 3.289791514),
    ("over", 3.264108453),
    ("state", 3.220617211),
    ("year", 3.206319322),
    ("day", 3.171800286),
    ("into", 3.165254951),
    ("email", 3.155548066),
    ("two", 3.137414351),
    ("health", 3.13043434),
    ("world", 3.07014387),
    ("next", 3.027276844),
    ("used", 2.995538608),
    ("go", 2.993038185),
    ("work", 2.981648421),
    ("last", 2.968269),
    ("most", 2.958380459),
    ("music", 2.942874057),
    ("data", 2.892262218),
    ("make", 2.879299646),
    ("them", 2.864485149),
    ("should", 2.85757375),
    ("system", 2.82165728),
    ("her", 2.786018593),
    ("city", 2.776094363),
    ("add", 2.752403062),
    ("number", 2.727923937),
    ("such", 2.706160176),
    ("please", 2.701330048),
    ("after", 2.650876394),
    ("then", 2.629416568),
    ("good", 2.600042866),
    ("well", 2.573646691),
    ("she", 2.410795027),
    ("know", 2.17573285),
    ("way", 2.171573245),
    ("could", 2.148798316),
    ("because", 1.928542769),
    ("take", 1.878970984),
    ("want", 1.838744158),
    ("even", 1.746393791),
    ("him", 1.560297138),
    ("think", 1.548501776),
    ("look", 1.229971722),
    ("say", 1.1148399),
    ("come", 1.096934057),
    ("give", 1),
]

_letter_map = {chr(x): 0 for x in range(ord('a'), ord('z')+1)}
for w, _ in words:
    for x in w:
        _letter_map[x] += 1
_n = sum(1 for x in _letter_map.items() if x[1] > 0)

_letters = [x[0] for x in sorted(_letter_map.items(), key=lambda a: a[1], reverse=True)]
for i, x in enumerate(_letters):
    _letter_map[x] = i

_words = []
# for word

letters = ['e', 't', 'o', 'a', 'h', 's', 'n', 'i', 'w', 'l', 'r', 'u', 'm', 'd', 'y', 'c', 'b', 'k', 'f', 'p', 'v', 'g', 'j', 'x']

# New candidate (score 817.9433359040002): (('e', 't', 'o', 'a', 'h', 's', 'n', 'i', 'r', 'f'), ('l', 'u', 'm', 'd', 'y', 'c', 'b', 'k', 'p', 'j'))
# New candidate (score 766.8655049750001): (('e', 't', 'o', 'h', 's', 'i', 'w', 'r', 'u', 'f'), ('a', 'n', 'l', 'm', 'd', 'y', 'c', 'b', 'k', 'v'))
# 670.4s, 2.49567%: Candidate (('e', 't', 'o', 'h', 's', 'i', 'w', 'r', 'u', 'f'), ('a', 'n', 'l', 'm', 'd', 'y', 'c', 'b', 'k', 'v'))

if __name__ == "__main__":
    import itertools
    import time
    import math
    total_iterations = math.factorial(len(letters))/(math.factorial(len(letters)-10)*math.factorial(10))
    total_iterations *= math.factorial(len(letters)-10)/(math.factorial(len(letters)-20)*math.factorial(10))
    print(F"Running {total_iterations} iterations")
    min_score = sum([len(w[0]) for w in words])*words[0][1]
    t_last = time.time()
    t_last_candidate = t_last
    iterations = 0
    candidate = None
    for layer1 in itertools.combinations(letters, 10):
        for layer2 in itertools.combinations([x for x in letters if x not in layer1], 10):
            x, b = set(layer1), set(layer2)
            score = 0
            for word in words:
                if word[0][0] in x:
                    layer = 1
                elif word[0][0] in b:
                    layer = 2
                else:
                    layer = 3
                for x in word[0][1:]:
                    if x in x:
                        if layer != 1:
                            score += word[1]
                            layer = 1
                    elif x in b:
                        if layer != 2:
                            score += word[1]
                            layer = 2
                    else:
                        if layer != 3:
                            score += word[1]
                            layer = 3
            iterations += 1
            if score < min_score:
                candidate = (layer1, layer2)
                min_score = score
                print(F"New candidate (score {score}): {candidate}")
                t_last = time.time()
                t_last_candidate = t_last
            elif (time.time() - t_last) > 10:
                t_last = time.time()
                print(F"{format(time.time() - t_last_candidate,'.1f')}s, {format(iterations/total_iterations*100,'.5f')}%: Candidate {candidate}")

