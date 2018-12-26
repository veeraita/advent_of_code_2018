from collections import defaultdict
from string import ascii_uppercase
import numpy as np
import pandas as pd

### PART ONE ###

requirements = {}
for a in ascii_uppercase:
    requirements[a] = set()
with open('instructions.txt') as f:
    for line in f.readlines():
        step = line.split()[7]
        required_step = line.split()[1]
        requirements[step].add(required_step)
requirements_orig = requirements.copy()

finished_steps = []
available_steps = []
while len(finished_steps) < len(ascii_uppercase):
    for k in ascii_uppercase:
        requirements[k] = [step for step in requirements[k] if step not in finished_steps]
        if len(requirements[k]) == 0 and k not in available_steps and k not in finished_steps:
            print("Step", k, "is now available")
            available_steps.append(k)
    next_step = sorted(available_steps)[0]
    available_steps.remove(next_step)
    print("Step", next_step, "is finished")
    finished_steps.append(next_step)

print("".join(finished_steps), '\n')

### PART TWO ###

letter2seconds = {}
max_time = 0
for i, l in enumerate(ascii_uppercase):
    letter2seconds[l] = i + 61
    max_time += letter2seconds[l]

requirements = requirements_orig.copy()
finished_steps = []
available_steps = []
current_steps = []
schedule = np.zeros((max_time, 5), dtype='object')

for second in range(max_time):
    if len(finished_steps) == len(ascii_uppercase):
        break

    for k in ascii_uppercase:
        requirements[k] = [step for step in requirements[k] if step not in finished_steps]
        if len(requirements[k]) == 0 and k not in available_steps and k not in current_steps and k not in finished_steps:
            print("Step", k, "is now available")
            available_steps.append(k)
    available_steps.sort()
    if len(np.where(schedule[second] == 0)[0]) == 0:
        # all workers busy
        continue

    for step in current_steps:
        if len(np.where(schedule[second + 1] == step)[0]) == 0:
            print("Step", step, "finished at time", second)
            current_steps.remove(step)
            finished_steps.append(step)

    for i in range(5):
        if available_steps and schedule[second, i] == 0:  # worker is idle
            next_step = available_steps.pop(0)
            current_steps.append(next_step)
            duration = letter2seconds[next_step]
            schedule[second:second + duration, i] = next_step
            print("Worker {} starting step {} at time {} (duration {} seconds)".format(i + 1, next_step, second,
                                                                                       duration))
# save to file, for debugging
df = pd.DataFrame(data=schedule)
df.to_csv('schedule.csv', sep=' ', header=False, index=True)
print(schedule[~(schedule == 0).all(1)].shape[0], "seconds")