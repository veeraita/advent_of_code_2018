import numpy as np

### PART ONE ###

with open('fabric.txt') as f:
    lines = f.readlines()

claims = []
# parse data to dicts
for line in lines:
    id = line.split('@')[0].strip('#')
    pos = line.split('@')[1].split(':')[0].strip()
    size = line.split(':')[1].strip()

    left, top = pos.split(',')
    width, height = size.split('x')
    claims.append({
        'id': int(id),
        'left': int(left),
        'top': int(top),
        'width': int(width),
        'height': int(height)
    })

fabric = np.zeros((1000, 1000))

for claim in claims:
    s1 = slice(claim['left'], claim['left']+claim['width'])
    s2 = slice(claim['top'], claim['top']+claim['height'])
    # if there is already a claim for some square inches, update value to -1
    # otherwise mark the square inches with claim ID
    fabric[s1, s2][np.where(fabric[s1, s2] > 0)] = -1
    fabric[s1, s2][np.where(fabric[s1, s2] == 0)] = claim['id']
print(len(np.where(fabric < 0)[0]), "overlapping square inches")


### PART TWO ###

# use the filled matrix from part one
intact_id = ''
for claim in claims:
    intact_size = np.size(fabric[fabric == claim['id']])
    # if the number of non-overlapping matrix elements is the same as the size of the rectangle,
    # there is no overlapping at all
    if intact_size == claim['height'] * claim['width']:
        intact_id = claim['id']
        break
print("ID of the non-overlapping claim is", intact_id)
