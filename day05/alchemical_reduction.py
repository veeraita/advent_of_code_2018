from string import ascii_lowercase
from operator import itemgetter

with open('polymer.txt', 'r') as f:
    poly = f.read()

### PART ONE ###

def reduce(polymer):
    index = 0
    while True:
        to_remove = set()
        while index < len(polymer) - 1:
            k = polymer[index]
            s = polymer[index + 1]
            if k != s and k.lower() == s.lower():
                to_remove.update([index, index + 1])
                index = max(0, index - 1) # optimization: no need to start from the beginning
                break
            index += 1
        if len(to_remove) == 0:
            break
        # turn the string into a list, delete elements and combine again into string
        l_polymer = list(polymer)
        for i in sorted(to_remove, reverse=True):
            del l_polymer[i]
        polymer = "".join(l_polymer)
        #print("Current length: ", len(polymer))
    return len(polymer)

#reduced_length = reduce(poly)
#print("\nFinal length: ", reduced_length)
#print("\n")


### PART TWO ###

lengths = []
for c in ascii_lowercase:
    print(c)
    modified_poly = poly.replace(c, '').replace(c.upper(), '')
    print(len(modified_poly))
    if len(modified_poly) < len(poly):
        reduced_length = reduce(modified_poly)
        lengths.append((c, reduced_length))

letter, length = min(lengths, key=itemgetter(1))
print(f"Maximum reduction achieved by removing units of type {letter} (final length {length} units)")
