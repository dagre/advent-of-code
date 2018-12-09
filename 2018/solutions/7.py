import re
import networkx as nx

pattern = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin')

def parse(str):
    groups = pattern.findall(str)
    return groups[0]

def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(parse(line))
            line = fp.readline()
    return lines

def build_dependency_graph(dependencies):
    graph = nx.DiGraph()
    for f, t in dependencies:
        # nodes automatically added
        graph.add_edge(f, t)
    return graph

def iter(graph, candidates, done):
    available_tasks = [n for n in graph.nodes if graph.in_degree(n) == 0]

    if len(available_tasks) == 0:
        return ''
    else:
        next = min(available_tasks)
        graph.remove_node(next)
        available_tasks.remove(next)
        done.add(next)
        return next + iter(graph, available_tasks, done)

def part1(dependencies):
    graph = build_dependency_graph(dependencies)
    return iter(graph, [], set())

def task_duration(task):
    return ord(task) - ord('A') + 1 + 60

def part2(dependencies, num_workers):
    graph = build_dependency_graph(dependencies)
    t = 0
    workers_available_at = [0 for i in range(0, num_workers)]
    last_worker_task = [None for i in range(0, num_workers)]
    
    while True:
        # first, check if any of the workers have finished a task
        for wi, w in enumerate(workers_available_at):
            if w <= t and last_worker_task[wi] in graph.nodes:
                # worker has finished a task, remove it from the graph
                graph.remove_node(last_worker_task[wi])

        # now, check if we have any more tasks left
        if len(graph.nodes) == 0:
            # all tasks done
            return t

        # next, check which tasks can be worked on, if any
        available_tasks = sorted([n for n in graph.nodes if graph.in_degree(n) == 0 and n not in last_worker_task])
        if len(available_tasks) != 0:
            # some tasks are available
            task_durations = []
            for wi, w in enumerate(workers_available_at):
                if w <= t and len(available_tasks) > 0:
                    task = available_tasks[0]
                    duration = task_duration(task)
                    workers_available_at[wi] = t + duration
                    last_worker_task[wi] = task
                    available_tasks.remove(task)
                    task_durations.append(duration)
        # time travel to the first time when any of the currently busy workers will have finished their current task
        t = min(filter(lambda x: x>t, workers_available_at))
            

dependencies = load_file('input/input-7a.txt')

print(part1(dependencies))
print(part2(dependencies, 5))