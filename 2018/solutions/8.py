import re
import networkx as nx
from enum import Enum

class ParseStatus(Enum):
    EXPECT_NUM_CHILDREN = 1
    EXPECT_NUM_METADATA = 2
    EXPECT_METADATA = 3

def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(parse(line))
            line = fp.readline()
    return lines

def parse(str):
    return [int(m) for m in str.split(' ')]

def build_tree(values):
    graph = nx.DiGraph()
    node_index = 0
    stack = []
    mode = ParseStatus.EXPECT_NUM_CHILDREN
    tmp_num_children = None
    for v in values:
        if mode == ParseStatus.EXPECT_NUM_CHILDREN:
            if tmp_num_children != None:
                raise Exception('num children not expected prior to new node')

            tmp_num_children = v
            mode = ParseStatus.EXPECT_NUM_METADATA
        elif mode == ParseStatus.EXPECT_NUM_METADATA:
            if tmp_num_children == None:
                raise Exception('num children expected prior to metadata')
            
            parent = None
            if len(stack) != 0:
                (par_ndx, par_nc, par_nm) = stack[len(stack) - 1]
                stack[len(stack) - 1] = (par_ndx, par_nc-1, par_nm)
                parent = par_ndx
            
            stack.append((node_index, tmp_num_children, v))
            graph.add_node(node_index, num_children = tmp_num_children, num_metadata = v, metadata = [])

            if parent != None:
                graph.add_edge(parent, node_index)
            
            if tmp_num_children == 0:
                if v > 0:
                    mode = ParseStatus.EXPECT_METADATA
                else:
                    # no metadata or children, we can remove it from the stack and expect another node
                    stack.pop()
                    mode = ParseStatus.EXPECT_NUM_CHILDREN
            else:
                mode = ParseStatus.EXPECT_NUM_CHILDREN
            
            tmp_num_children = None
            node_index += 1
        elif mode == ParseStatus.EXPECT_METADATA:
            # this metadata belongs to the last item on the stack
            (index, num_children, num_metadata) = stack[len(stack) - 1]
            graph.nodes.data()[index]['metadata'].append(v)
            if num_metadata == 1:
                # we're done from this node's metadata
                stack.pop()
                if len(stack) == 0:
                    # we're done
                    break
                else:
                    (p_ndx, p_nc, p_nm) = stack[len(stack) - 1]
                    while p_nc == 0 and p_nm == 0:
                        stack.pop()
                        (p_ndx, p_nc, p_nm) = stack[len(stack) - 1]
                    if p_nc == 0:
                        # no more children, but has metadata
                        mode = ParseStatus.EXPECT_METADATA
                    else:
                        # no more metadata, but has children
                        mode = ParseStatus.EXPECT_NUM_CHILDREN
            else:
                stack[len(stack) - 1] = (index, num_children, num_metadata - 1)
                mode = ParseStatus.EXPECT_METADATA
    assert len(stack) == 0 # we should have processed all the nodes
    return graph

def part1(tree):
    return sum([sum(n[1]['metadata']) for n in tree.nodes.data()])

def value(node, graph):
    metadata = graph.nodes.data()[node]['metadata']
    out_degree = graph.out_degree(node)
    if out_degree == 0:
        return sum(metadata)
    else:
        succ = list(graph.successors(node))
        child_values = [value(succ[ndx-1], graph) for ndx in metadata if ndx > 0 and ndx <= out_degree]
        return sum(child_values)
        
def part2(tree):
    return value(0, tree)

lines = load_file('input/input-8a.txt')
tree = build_tree(lines[0])

print(part1(tree))
print(part2(tree))