### PART ONE ###

change = 0
with open('changes.txt') as f:
    lines = f.readlines()
for num in lines:
    change += int(num)

print("Total change: ", change)


### PART TWO ###

change = 0
seen = set([0])
found = False
while not found:
    for num in lines:
        change += int(num)
        if change in seen:
            found = True
            break
        seen.add(change)
print("First frequency reached twice: ", change)
