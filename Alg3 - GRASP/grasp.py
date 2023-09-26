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
clibrary = ctypes.CDLL(os.path.join(path, 'grasp.so'))


lines = []
for line in sys.stdin:
    lines.append(line.rstrip())

k, v, N, t = map(int, lines[0].split())

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

grasp_algorithm = clibrary.grasp_algorithm
grasp_algorithm.argtypes = [ctypes.POINTER(Node), ctypes.c_int, ctypes.c_int, ctypes.c_int]
grasp_algorithm(nodes, v, N+1, 10000)
# print(nodes)
# print(v)
# print(len(nodes))
# initial_solution = clibrary.initial_solution
# initial_solution.argtypes = [ctypes.POINTER(Node), ctypes.c_int, ctypes.c_int]
# initial_solution.restype = ctypes.POINTER(ctypes.POINTER(Node))
# vector_of_tours = initial_solution(nodes, v, N+1)
# result = []
# for i in range(v+2):
#     subvec = ctypes.cast(vector_of_tours[i], ctypes.POINTER(Node))
#     sub_list = []
#     j = 0
#     while True:
#         val = subvec[j]
#         print(val.num, val.x, val.y)
#         if val.num == 0:
#             break
#         sub_list.append(val)
#         j += 1
#         if j >= 15:
#             break
#         print(i)

#     # len_subvec = ctypes.sizeof(subvec) / ctypes.sizeof(subvec[0])
#     # for j in range(len_subvec):
#     #     sub_list.append(subvec[i])
#     print(sub_list)

#     break
#     # subvec_list = [subvec[j] for j in range(2)]
    # print(subvec_list)
    # result.append(subvec_list)
# for res in result:
#     res_str = ""
#     for i in range(len(res)):
#         res_str+=str(res[i].num) + " "
#     print(res_str)

# for node 