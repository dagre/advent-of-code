from enum import Enum
from datetime import datetime, date, time
import re

event_pattern = re.compile(r'\[([0-9]*)-([0-9]*)-([0-9]*) ([0-9]*):([0-9]*)\] (.*)')

class EventType(Enum):
    SHIFT_START = 0
    SLEEP = 1
    WAKE = 2

class Event:
    def __init__(self, datetime, type, guard_id):
        self.datetime = datetime
        self.type = type
        self.guard_id = guard_id
    
    def __repr__(self):
        return "%s: %s [%s]" % (self.datetime, self.type, self.guard_id)

def get_event_type(evt):
    if 'wakes up' in evt:
        return EventType.WAKE
    elif 'falls asleep' in evt:
        return EventType.SLEEP
    elif 'begins shift' in evt:
        return EventType.SHIFT_START
    else:
        raise Exception('unknown event: ' + evt)

def extract_guard_id(evt):
    if 'Guard' in evt:
        hash_index = evt.find('#')
        next_space_index = evt.find(' ', hash_index)
        return int(evt[hash_index+1:next_space_index])
    else:
        return None

def parse(str):
    groups = event_pattern.findall(str)
    (year,day,month,hour,minute,desc) = groups[0]
    event_date = date(int(year), int(day), int(month))
    event_time = time(int(hour), int(minute))
    event_datetime = datetime.combine(event_date, event_time)
    event_type = get_event_type(desc)
    guard_id = extract_guard_id(desc)
    return Event(event_datetime, event_type, guard_id)

def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(parse(line))
            line = fp.readline()
    return lines

def assign_guard_ids(events):
    last_guard_id = None
    for evt in events:
        if evt.guard_id == None:
            evt.guard_id = last_guard_id
        else:
            last_guard_id = evt.guard_id

# prepare input
lines = load_file('input-4a.txt')
lines.sort(key = lambda x:x.datetime)
assign_guard_ids(lines)

def process(evts):
    guards = {}
    previous_event = None

    for evt in evts:
        if evt.guard_id not in guards:
            guards[evt.guard_id] = {
                'timeline': [0 for i in range(0,60)],
                'total': 0
            }
        if evt.type == EventType.WAKE:
            for m in range(previous_event.datetime.minute, evt.datetime.minute):
                guards[evt.guard_id]['timeline'][m] += 1
                guards[evt.guard_id]['total'] += 1
        previous_event = evt
    
    return guards

guards = process(lines)

def part1(guards):    
    max_guard_id, max_guard_value = None, {}
    for guard_id, value in guards.items():
        if max_guard_id == None or max_guard_value['total'] < value['total']:
            max_guard_id = guard_id
            max_guard_value = value
    
    top_index, top_minute = 0,0
    for index, minute in enumerate(max_guard_value['timeline']):
        if minute > top_minute:
            top_index = index
            top_minute = minute

    return max_guard_id * top_index

def part2(guards):
    top_guard_id, top_minute, top_minute_value = 0, 0, 0
    for guard_id, value in guards.items():
        for minute, num_times_asleep in enumerate(value['timeline']):
            if num_times_asleep > top_minute_value:
                top_guard_id = guard_id
                top_minute = minute
                top_minute_value = num_times_asleep
    
    return top_guard_id * top_minute

print(part1(guards))
print(part2(guards))