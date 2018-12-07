import time
import pandas as pd
from operator import itemgetter

with open('records.txt') as f:
    lines = f.readlines()

### PART ONE ###

# parse records to dataframe
labels = ['date', 'time', 'guard_id', 'event']
records = []
for line in lines:
    datetime = line.split(']')[0].replace('[1518-', '') # use only day and time data
    date = datetime.split()[0]
    time = datetime.split()[1]
    if '#' in line:
        guard_id = line.split('#')[1].split()[0]
        event = 'begins'
    else:
        guard_id = None
        event = line.split(']')[1].strip()
    records.append((date, time, guard_id, event))

df = pd.DataFrame.from_records(records, columns=labels)
# sort by datetime
df.sort_values(by=['date', 'time'], inplace=True)
df['time'] = df['time'].apply(lambda x: x[3:])
# fill missing guard ids
current_guard = None
for i, row in df.iterrows():
    if row.event == 'begins':
        current_guard = df.at[i, 'guard_id']
    else:
        df.at[i, 'guard_id'] = current_guard
df = df[df.event != 'begins']

# create another dataframe with date, guard id and minutes as columns
df2 = df[['date', 'guard_id']]
df2.drop_duplicates(inplace=True)
df2.set_index('date', inplace=True)
# initialize with zeros
for i in range(60):
    df2.loc[:, '{:02}'.format(i)] = 0
for date, row in df2.iterrows():
    sleep_rows = df.loc[(df.date == date) & (df.event == 'falls asleep')].values
    wake_rows = df.loc[(df.date == date) & (df.event == 'wakes up')].values
    # change value to 1 for every minute of sleep
    for s, w in zip(sleep_rows, wake_rows):
        start, end = s[1], '{:02}'.format(int(w[1])-1)
        df2.loc[date, start:end] = 1
minutes = ['{:02}'.format(i) for i in range(60)]
df2['sum_date'] = df2[minutes].sum(axis=1)

# get the total number of minutes slept by each guard
guard_totals = []
for id in df2.guard_id.unique():
    guard_totals.append((id, df2[df2.guard_id==id]['sum_date'].sum()))
g_id, tot = max(guard_totals, key=itemgetter(1))
print(f"The ID of the guard who sleeps the most is {g_id}, with {tot} total minutes of sleep")

max_min = df2[df2.guard_id==g_id][minutes].sum(axis=0).idxmax()
print(f"The minute that the guard spent asleep the most is {max_min}")


### PART TWO ###

guard_maxminutes = []
for id in df2.guard_id.unique():
    counts = df2[df2.guard_id==id][minutes].apply(pd.Series.value_counts).loc[1, :]
    max_minute = counts.idxmax()
    guard_maxminutes.append((id, max_minute, counts[max_minute]))
g_id, minute, times = max(guard_maxminutes, key=itemgetter(2))
print(f"The ID of the guard most frequently asleep on the same minute is {g_id} ({times} times on minute {minute})")
