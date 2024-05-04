from wordlist import words
from words import layer1, layer2, layer3, _layer_map, _letter_map, _words

# layer1 -- New candidate (score 26495.022): (('s', 'r', 'n', 'c', 'd', 'h'), ['a', 'o'], ('e', 'i'), 't')
# layer2 -- New candidate (score 4258.551):  (('p', 'g', 'b', 'f', 'v', 'w'), ['m', 'k'], ('u', 'y'), 'l')

if __name__ == "__main__":
    import itertools
    min_score = sum(len(w) for w, _ in _words) * _words[0][1]
    candidate = None
    for face in itertools.combinations(layer2, 6):
        rem = [x for x in layer2 if x not in face]
        for back in rem:
            shoulders = [x for x in rem if x != back]
            for left in itertools.combinations(shoulders, 2):
                if left[0] != shoulders[0]:
                    break
                right = [x for x in shoulders if x not in left]
                for i, _ in enumerate(_layer_map):
                    _layer_map[i] = 0
                for x in face:
                    _layer_map[_letter_map[x]] = 1
                for x in left:
                    _layer_map[_letter_map[x]] = 2
                for x in right:
                    _layer_map[_letter_map[x]] = 3
                _layer_map[_letter_map[back]] = 4
                score = 0
                for w, s in _words:
                    last = w[0]
                    for x in w[1:]:
                        if _layer_map[x] != 0:
                            if _layer_map[x] == _layer_map[last]:
                                score += s
                        last = x
                if score < min_score:
                    min_score = score
                    candidate = (face, right, left, back)
                    print(F"New candidate (score {format(score,'.3f')}): {candidate}")
