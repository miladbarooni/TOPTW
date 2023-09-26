#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import sys
import random
import math
import copy
# from joblib import Parallel, delayed
file_path = "../Instances/c102.txt" 
import concurrent.futures


# In[2]:


class Node:
    def __init__(self, num, x, y, service_time, score, open_time, close_time):
        self.num = num
        self.x = x
        self.y = y
        self.service_time = service_time
        self.open_time = open_time
        self.close_time = close_time
        self.score = score


def is_feasible (tour, source):
    t_current=0
    t_max=source.close_time
    current_vertex=source
    # print("tour", tour)
    for i in range(len(tour)+1):
        next_vertex= None
        if i==len(tour):
            next_vertex= source
        else:
            next_vertex=tour[i]
        if max(t_current+math.dist([next_vertex.x,next_vertex.y],[current_vertex.x,current_vertex.y]),next_vertex.open_time)+next_vertex.service_time +math.dist([next_vertex.x,next_vertex.y],[source.x,source.y])>t_max:
            return False
        if (t_current + math.dist([next_vertex.x,next_vertex.y],[current_vertex.x,current_vertex.y]) <= next_vertex.close_time):
                t_current = max(t_current +math.dist([next_vertex.x,next_vertex.y],[current_vertex.x,current_vertex.y]), next_vertex.open_time) + next_vertex.service_time;
                current_vertex = next_vertex
            
        else: 
            return False
    return True

def calculate_score(solution, source):
    score=0
    for i in range(len(solution)):
        tour=solution[i]
        if is_feasible(tour, source):
            for j in range (len(tour)):
                score += tour[j].score
    return score

def solution_to_num(solution):
    solution_in_num = [[obj.num for obj in inner_list] for inner_list in solution]
    return solution_in_num

def tour_to_num(tour):
    tour_in_num = [obj.num for obj in tour]
    return tour_in_num


# In[3]:


def euclidian_distance(first_node: Node, second_node: Node):
    return math.dist([first_node.x, first_node.y], [second_node.x, second_node.y])

def random_initial_solution(nodes, team_number):
    solution = []
    candidate = copy.deepcopy(nodes)
    source = nodes[0]
    t_max = nodes[0].close_time
    candidate.pop(0)
    
    for i in range(team_number):
        t_current = 0.0
        tour = []
        current_vertex = source
        counter = 0
        
        while len(candidate) > 0:
            random_candidate = random.randint(0, len(candidate) - 1)
            next_vertex = candidate[random_candidate]
            
            if (max(t_current + euclidian_distance(next_vertex, current_vertex), next_vertex.open_time) +
                    next_vertex.service_time + euclidian_distance(next_vertex, source)) > t_max:
                break
            
            if t_current + euclidian_distance(next_vertex, current_vertex) <= next_vertex.close_time:
                t_current = max(t_current + euclidian_distance(next_vertex, current_vertex),
                                next_vertex.open_time) + next_vertex.service_time
                tour.append(next_vertex)
                current_vertex = next_vertex
                candidate.pop(random_candidate)
            else:
                if counter == len(candidate):
                    break
                else:
                    counter += 1
                    continue
        
        solution.append(tour)
    
    return solution


# In[4]:


lines = []

with open(file_path, 'r') as file:
    for line in file:
        lines.append(line.rstrip())


k, v, N, t = map(int, lines[0].split())
# v = 3
nodes = []
optimal_score = 0
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
    nodes.append(node)
    optimal_score+=score
source = nodes[0]
optimal_score


# In[5]:


# initial_solution = random_initial_solution(nodes, v)
# print(print_solution_num(initial_solution))
# calculate_score(initial_solution, source)



# In[7]:


initial_population = []
population_size = 200
for i in range(population_size):
    print(i)
    random_member = random_initial_solution(nodes, v)
    initial_population.append(random_member)


# In[8]:


def repair_tour_in_solution(solution, index):
    tour = solution[index]
    tour_size = len(tour)
    
    for j in range(len(solution)):
        i = 0
        while i < tour_size:   
            if j != index and tour[i].num in tour_to_num(solution[j]):
                tour.pop(i)

                i -= 1
                tour_size -= 1
            i += 1
    solution[index] = tour
    return solution

def mutation_insert(solution, index):
    candidate = copy.deepcopy(nodes)
    candidate.pop(0)
    for i in range(len(solution)):
        for j in range(len(solution[i])):
                k = 0
                candidate_size = len(candidate)
                while k < candidate_size:
                    if candidate[k].num == solution[i][j].num:
                        candidate.pop(k)
                        break
                    k += 1
    tour = solution[index]
    random.shuffle(candidate)
    can_insert = False
    list_of_index = [i for i in range(len(tour)+1)] 
    random.shuffle(list_of_index)
    for i in list_of_index:
        for j in range(len(candidate)):
            tour.insert(i, candidate[j])
            if is_feasible(tour, source):
                can_insert = True
                break
            else:
                tour.pop(i)
        if can_insert:
            break
    return solution

def mutation_remove(solution, index):
    tour = solution[index]
    if len(tour) <= 2 :
        return solution
    random_index = random.randint(0, len(tour)-1)
    tour.pop(random_index)
    return solution

def cross_over_and_mutation(first, second):
    first_solution = copy.deepcopy(first)
    second_solution = copy.deepcopy(second)
    
    first_index = random.randint(0, v-1)
    second_index = random.randint(0, v-1)
    # print(first_index)
    # print(second_index)

    first_solution[first_index], second_solution[second_index] = second_solution[second_index], first_solution[first_index]

    first_solution = repair_tour_in_solution(first_solution, first_index)
    second_solution = repair_tour_in_solution(second_solution, second_index)

    # first_solution = mutation_insert(first_solution, first_index)
    # second_solution = mutation_insert(second_solution, second_index)
    
    for i in range(len(first_solution)//2):
        uniform_probability = random.uniform(0, 1)
        random_tour_index = random.randint(0, len(first_solution)-1)
        if uniform_probability >= 0.2:
            first_solution = mutation_insert(first_solution, random_tour_index)
        else:
            
            first_solution = mutation_remove(first_solution, random_tour_index)
    
    for i in range(len(second_solution)//2):
        uniform_probability = random.uniform(0, 1)
        random_tour_index = random.randint(0, len(second_solution)-1)
        if uniform_probability >= 0.2:
            second_solution = mutation_insert(second_solution, random_tour_index)
        else:
            second_solution = mutation_remove(second_solution, random_tour_index)

    return [first_solution, second_solution]


def cross_over(first, second):
    first_solution = copy.deepcopy(first)
    second_solution = copy.deepcopy(second)
    
    first_index = random.randint(0, v-1)
    print(first_index)
    second_index = random.randint(0, v-1)
    print(second_index)
    # first_index = 0
    # second_index = 1
    first_solution[first_index], second_solution[second_index] = second_solution[second_index], first_solution[first_index]
    repair_tour_in_solution(first_solution, first_index)
    repair_tour_in_solution(second_solution, second_index)
    
    return [first_solution, second_solution]



# In[11]:


def generate_new_population(population):
    first_solution_index = random.randint(0, population_size-1)
    second_solution_index = random.randint(0, population_size-1)
    while second_solution_index == first_solution_index:
        second_solution_index = random.randint(0, population_size-1)
    
    return cross_over_and_mutation(population[first_solution_index], population[second_solution_index])
num_threads = 100

population = copy.deepcopy(initial_population)
for i in range(500):
    # population.sort(key=lambda i:calculate_score(i, source), reverse=True)
    # print(i, " ", calculate_score(population[0], source))
    new_population = []
#     for j in range(100):
        
#         first_solution_index = random.randint(0, population_size-1)
#         second_solution_index = random.randint(0, population_size-1)
#         while second_solution_index == first_solution_index:
#             second_solution_index = random.randint(0, population_size-1)
        
#         new_population += cross_over_and_mutation(population[first_solution_index], population[second_solution_index])
#     results = Parallel(n_jobs=4)(delayed(generate_new_population)(population) for i in range(100))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit each item to the executor
        futures = [executor.submit(generate_new_population, population) for i in range(100)]
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
    # print(futures[0].result())
    # print(len(futures))
    # print(len(results[0]))
    new_population = []
    for j in range(len(futures)):
        new_population += futures[j].result()
    
    pool = new_population + population
    # for i in range(le)
    pool.sort(key=lambda i:calculate_score(i, source), reverse=True)
    print(i, " ", calculate_score(pool[0], source))
    population = pool[:int(0.7*population_size)] + random.choices(pool[int(0.7*population_size):], k=int(0.3*population_size))
    print(len(population))
        # print(solution_to_num(population[first_solution_index]))

        # print(solution_to_num(population[second_solution_index]))
        # print(solution_to_num(new_population[0]))

        # print(solution_to_num(new_population[1]))

    
        


# In[ ]:


import numpy as np
sol_array = np.concatenate(solution_to_num(population[0]))
print( np.sort(sol_array))
for i in range(10):
    
    print(tour_to_num(population[0][i]))
    


# In[ ]:





# In[15]:


# Example lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Swapping elements
index1 = 1  # Index of the element in list1 to be swapped
index2 = 1  # Index of the element in list2 to be swapped

list1[index1], list2[index2] = list2[index2], list1[index1]

# Output
print(list1)  # [1, 6, 3]
print(list2)  # [4, 5, 2]

