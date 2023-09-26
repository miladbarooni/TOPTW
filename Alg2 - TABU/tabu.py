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
clibrary = ctypes.CDLL(os.path.join(path, 'tabu.so'))


lines = []
for line in sys.stdin:
    lines.append(line.rstrip())

k, v, N, t = map(int, lines[0].split())
# v = 3
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

tabu_algorithm = clibrary.tabu_algorithm
tabu_algorithm.argtypes = [ctypes.POINTER(Node), ctypes.c_int, ctypes.c_int, ctypes.c_int]
tabu_algorithm(nodes, v, N+1, 10000)