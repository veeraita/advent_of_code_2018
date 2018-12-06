### PART ONE ###

with open('boxes.txt') as f:
    ids = f.readlines()

twos = 0
threes = 0
for box_id in ids:
    two_found = False
    three_found = False
    for c in set(box_id.strip()):
        count = box_id.count(c)
        if count == 2 and not two_found:
            twos += 1
            two_found = True
        elif count == 3 and not three_found:
            threes += 1
            three_found = True

checksum = twos * threes

print(checksum)

### PART TWO ###

common = ''
for i in range(len(ids)):
    id1 = ids[i].strip()
    for j in range(i, len(ids)):
        id2 = ids[j].strip()
        if id1 == id2:
            continue
        diff = 0
        diff_index = 0
        for k, (a, b) in enumerate(zip(id1, id2)):
            if a != b:
                diff += 1
                diff_index = k
            if diff > 1:
                break
        if diff == 1:
            common = id1[:diff_index] + id1[diff_index+1:]
            break
    if common:
        break

print("Correct box IDs are {} and {}".format(id1, id2))
print("Common letters are {} (difference on index {})".format(common, diff_index))
