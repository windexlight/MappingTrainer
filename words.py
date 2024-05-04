from wordlist import words

_letter_map = {chr(x): 0 for x in range(ord('a'), ord('z')+1)}
for w, _ in words:
    for x in w:
        _letter_map[x] += 1

_letters_with_counts = [x for x in sorted(_letter_map.items(), key=lambda a: a[1], reverse=True)]
_letters = [x[0] for x in _letters_with_counts]
for i, x in enumerate(_letters):
    _letter_map[x] = i
_letter_count = len(_letters)

_words = [([_letter_map[x] for x in word], score/words[-1][1]) for word, score in words if len(word) > 1]

_layer_map = [0] * _letter_count

LAYER_SIZE = 11

N = _letter_count - 4 #sum(1 for x in _letter_map.items() if x[1] > 0)
_set = list(range(N))

# New candidate (score 817.9433359040002): (('e', 't', 'o', 'a', 'h', 's', 'n', 'i', 'r', 'f'), ('l', 'u', 'm', 'd', 'y', 'c', 'b', 'k', 'p', 'j'))
# New candidate (score 766.8655049750001): (('e', 't', 'o', 'h', 's', 'i', 'w', 'r', 'u', 'f'), ('a', 'n', 'l', 'm', 'd', 'y', 'c', 'b', 'k', 'v'))
# 670.4s, 2.49567%: Candidate (('e', 't', 'o', 'h', 's', 'i', 'w', 'r', 'u', 'f'), ('a', 'n', 'l', 'm', 'd', 'y', 'c', 'b', 'k', 'v'))
# 2981.9s, 29.36472%: Score 683.833, Candidate (['e', 't', 'a', 'h', 's', 'i', 'n', 'l', 'w', 'd', 'v'], ['o', 'r', 'm', 'u', 'y', 'c', 'b', 'k', 'f', 'p', 'g'], ['j', 'x', 'q', 'z'])
#    80.0s, 1.00977%: Score 683.833, Candidate (['e', 't', 'a', 'h', 's', 'n', 'i', 'l', 'w', 'd', 'v'], ['o', 'r', 'm', 'u', 'y', 'c', 'b', 'k', 'f', 'p', 'g'], ['j', 'x', 'q', 'z'])
# 4178.3s, 99.97789%: Score 136893.080, Candidate (['e', 'i', 'a', 's', 'r', 'n', 't', 'o', 'c', 'd', 'h'], ['l', 'p', 'u', 'm', 'g', 'b', 'y', 'f', 'v', 'w', 'k'], ['x', 'j', 'z', 'q'])

layer1, layer2, layer3 = ['e', 'i', 'a', 's', 'r', 'n', 't', 'o', 'c', 'd', 'h'], ['l', 'p', 'u', 'm', 'g', 'b', 'y', 'f', 'v', 'w', 'k'], ['x', 'j', 'z', 'q']

if __name__ == "__main__":
    import itertools
    import time
    import math
    total_iterations = math.factorial(N)/(math.factorial(N-(LAYER_SIZE*2))*math.factorial(LAYER_SIZE*2))
    total_iterations *= (math.factorial(LAYER_SIZE*2)/math.factorial(LAYER_SIZE)**2) / 2
    print(F"Running {total_iterations} iterations")
    print(F"Using letter set {_letters_with_counts[:N]}")
    print(F"Excluding letters (will be on layer 3) {_letters_with_counts[N:]}")
    min_score = sum(len(w) for w, _ in _words) * _words[0][1]
    t_last = time.time()
    t_last_candidate = t_last
    iterations = 0
    candidate = None
    for outer in itertools.combinations(_set, LAYER_SIZE*2):
        i = 0
        for x in outer:
            _layer_map[x] = 2
            while i < x:
                _layer_map[i] = 3
                i += 1
            i += 1
        while i < _letter_count:
            _layer_map[i] = 3
            i += 1
        for inner in itertools.combinations(outer, LAYER_SIZE):
            if inner[0] != outer[0]:
                break # Skip second half because it's just the same sets with the layers reversed
            for x in inner:
                _layer_map[x] = 1
            score = 0
            for w, s in _words:
                last = w[0]
                for x in w[1:]:
                    if _layer_map[x] != _layer_map[last]:
                        score += s
                    last = x
            iterations += 1
            for x in inner:
                _layer_map[x] = 2 # Restore it for the next iteration
            if score < min_score:
                candidate = ([_letters[x] for x in inner],
                             [_letters[x] for x in outer if x not in inner],
                             [_letters[x] for x in list(range(len(_letters))) if x not in outer])
                min_score = score
                print(F"New candidate (score {format(score,'.3f')}): {candidate}")
                t_last = time.time()
                t_last_candidate = t_last
            elif (time.time() - t_last) > 10:
                t_last = time.time()
                print(F"{format(time.time() - t_last_candidate,'.1f')}s, {format(iterations/total_iterations*100,'.5f')}%: Score {format(min_score,'.3f')}, Candidate {candidate}")

