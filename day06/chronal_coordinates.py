import numpy as np
import pandas as pd
from operator import itemgetter
from string import ascii_lowercase
from scipy.spatial.distance import cdist

### PART ONE ###

with open('coordinates.txt') as f:
    # change from (x, y) to (y, x) and sort coordinates by increasing y
    coords = sorted([(int(line.split(',')[1]), int(line.split(',')[0])) for line in f.readlines()], key=itemgetter(0))

coord_labels = [c.upper() + d.upper() for c in ascii_lowercase for d in ascii_lowercase][:len(coords)]

def get_closest_label(pos, coords, labels):
    distances = cdist(pos, coords, metric='cityblock').flatten()
    closest_index = np.where(distances == distances.min())[0]
    if len(closest_index) > 1:
        return '.'
    return labels[closest_index[0]].lower()

maxy = max(coords, key=itemgetter(0))[0] + 1
maxx = max(coords, key=itemgetter(1))[1] + 1

view = np.zeros((maxy, maxx), dtype='object')

# place coordinates on the view
for c, label in zip(coords, coord_labels):
    view[c] = label

it = np.nditer(view, flags=['refs_ok', 'multi_index'])
for i in it:
    if not i:
        ind = np.array(it.multi_index).reshape((1, 2))
        view[it.multi_index] = get_closest_label(ind, coords, coord_labels)

# save the view to file, just for debugging
df = pd.DataFrame(data=view)
df.to_csv('view.csv', sep=' ', header=False, index=False)

infinite_labels = set()
# labels found on the edges of the view have infinite area, remove these
for edge in (view[0], view[-1], view[:,0], view[:,-1]):
    infinite_labels.update(np.unique(edge))

finite_labels = [l for l in coord_labels if l.lower() not in infinite_labels]

view_list = view.flatten().tolist()
sizes = []
for fl in finite_labels:
    sizes.append(view_list.count(fl.lower()) + 1)
print(max(sizes))


### PART TWO ###

def sum_distances(pos, coords):
    return sum(cdist(pos, coords, metric='cityblock').flatten())

view2 = np.zeros((maxy, maxx))
size = 0
it = np.nditer(view2, flags=['multi_index'])
for i in it:
    ind = np.array(it.multi_index).reshape((1, 2))
    if sum_distances(ind, coords) < 10000:
        size += 1
print(size)



