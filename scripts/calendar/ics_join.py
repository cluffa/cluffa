# %%
from ics import Calendar
import requests

# %%
url = 'https://app.wheniwork.com/calendar/b68c1b427df83d529efbf83950bd3f345afd7b89.ics'
c = Calendar(requests.get(url).text)

# %%
new = set()
events = [e for e in c.events]
events.sort(key=lambda x: x.begin.format('YYYY-MM-DD HH:mm:ss'))

current = events[0]
i = 1
while i < len(events):
    if current.intersects(events[i]):
        current = current.join(events[i])
    else:
        current.name = 'Work Shift at SparkAI'
        new.add(current)
        current = events[i]

    i += 1

# %%
c.events = new
c.name = 'SparkAI Schedule (joined)'

# %%
with open('scripts/calendar/my.ics', 'w') as f:
    f.writelines(c.serialize().replace('SparkAI Schedule', 'SparkAI Schedule (joined)'))
