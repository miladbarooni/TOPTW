import os
import ctypes
import sys


class Node(ctypes.Structure):
    _fields_ = [
        ('num', ctypes.c_int),
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('service_time', ctypes.c_float),
        ('score', ctypes.c_float),
        ('open_time', ctypes.c_int),
        ('close_time', ctypes.c_int)
    ]

path = os.getcwd()
clibrary = ctypes.CDLL(os.path.join(path, 'check.so'))


lines = []
for line in sys.stdin:
    lines.append(line.rstrip())

k, v, N, t = map(int, lines[0].split()) 
v = 3
nodes = (Node * (N+1))()
for i, line in enumerate(lines[2:]):
    line_list = line.split()
    num = int(line_list[0])
    x = float(line_list[1])
    y = float(line_list[2])
    service_time = float(line_list[3])
    score = float(line_list[4])
    open_time = int(line_list[-2]) if lines.index(line) != 2 else 0
    close_time = int(line_list[-1]) if lines.index(line) != 2 else int(line_list[-1])
    node = Node(num, x, y, service_time, score, open_time, close_time)
    nodes[i] = node


feasible_tour = clibrary.feasible_tour
feasible_tour.argtypes = [ctypes.POINTER(Node), Node, ctypes.c_int]
find_score = clibrary.find_score
find_score.argtypes = [ctypes.POINTER(Node), ctypes.c_float]



solution = []

with open('result.txt') as f:
    lines = f.readlines()
    
    for i, line in enumerate(lines):
        line_list = line.rstrip().split()
        tour = (Node * (len(line_list) - 2))()
        for j, node_id in enumerate(line_list[1:-1]):
            print(node_id)
            tour[j] = nodes[int(node_id)]
        solution.append(tour)
for i, tour in enumerate(solution):
    print(f"{i+1}th tour: ", feasible_tour(tour, nodes[0], len(tour)))
# for i, tour in enumerate(solution):
#     print(f"{i+1}th tour score: ", find_score(tour, len(tour)))
# grasp_algorithm(nodes, nodes[0], N+1)