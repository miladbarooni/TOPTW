import os
import math
import copy
import random
import time
import csv
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

def euclidian_distance(first_node: Node, second_node: Node):
    return math.dist([first_node.x, first_node.y], [second_node.x, second_node.y])

def random_initial_solution(nodes, team_number):
    solution = []
    candidate = copy.deepcopy(nodes)
    source = nodes[0]
    t_max = source.close_time
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
                if counter == 30:
                    break
                else:
                    counter += 1
                    continue
        
        solution.append(tour)
    
    return solution

source = None
all_instances = os.listdir("../Instances")


all_instances.sort()
print(all_instances)
print(len(all_instances))
all_scores = []
headerList = ['Instance', 'Tour Number', 'Optimal Score', 'Max Score', 'Min Score', 'Mean Score', 'Gap']
  
# open CSV file and assign header
# with open("genetics_result.csv", 'w') as file:
#     dw = csv.DictWriter(file, delimiter=',', 
#                         fieldnames=headerList)
#     dw.writeheader()

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
    for i in random.choices(list_of_index, k=10):
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
    if len(tour) <= 1 :
        return solution
    random_index = random.randint(0, len(tour)-1)
    tour.pop(random_index)
    return solution

def mutation_swap(solution, index):
    tour = solution[index]
    can_swap = 0
    for i in range(len(tour)):
        for j in range(i, len(tour)):
            tour[i], tour[j] = tour[j], tour[i]
            if not is_feasible(tour, source):
                tour[i], tour[j] = tour[j], tour[i]
            else:
                can_swap += 1
                break
        if can_swap == 1:
            break
    return solution

def cross_over_and_mutation(first, second, third):
    current_solution = copy.deepcopy(first)
    p_best = copy.deepcopy(second)
    g_best = copy.deepcopy(third)
    for i in range(len(current_solution)):
        uniform_probability = random.uniform(0, 1)
        random_tour_index = random.randint(0, len(current_solution)-1)
        current_solution = mutation_swap(current_solution, random_tour_index)
        if uniform_probability >= 0.2:
            current_solution = mutation_insert(current_solution, random_tour_index)
        else:
            
            current_solution = mutation_remove(current_solution, random_tour_index)

    for i in range(int((p_best_w/100)*v)):
        first_index = random.randint(0, v-1)
        second_index = random.randint(0, v-1)

        current_solution[first_index], p_best[second_index] = p_best[second_index], current_solution[first_index]

        current_solution = repair_tour_in_solution(current_solution, first_index)
        p_best = repair_tour_in_solution(p_best, second_index)

    for i in range(int((g_best_w/100)*v)):
        first_index = random.randint(0, v-1)
        second_index = random.randint(0, v-1)

        current_solution[first_index], g_best[second_index] = g_best[second_index], current_solution[first_index]

        current_solution = repair_tour_in_solution(current_solution, first_index)
        g_best = repair_tour_in_solution(g_best, second_index)


    return current_solution



for idx, instance_file in enumerate(all_instances):
    print(instance_file)
    try:
        lines = []

        with open("../Instances/"+instance_file, 'r') as file:
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
        instance_score = []
        max_iteration = 5000
        
        for k in range(3):
            initial_population = []
            population_size = 100
            for i in range(population_size):
                random_member = random_initial_solution(nodes, v)
                initial_population.append(random_member)
            p_best_w = 10
            g_best_w = 30
            g_best = None
            g_best_score = 0
            for i in range(len(initial_population)):
                solution_score = calculate_score(initial_population[i], source)
                if solution_score > g_best_score:
                    g_best_score = solution_score
                    g_best = initial_population[i]
            p_best = [initial_population[i] for i in range(population_size)]
            population = copy.deepcopy(initial_population)
            t_end = time.time() + 60
            for i in range(max_iteration):
                if time.time() > t_end:
                    break
                new_population = []
                for j in range(population_size):
                    p_best_j = p_best[j]
                    new_solution = cross_over_and_mutation(population[j], p_best_j, g_best)
                    new_solution_score = calculate_score(new_solution, source)
                    if new_solution_score >= g_best_score:
                        g_best_score = new_solution_score
                        g_best = new_solution
                    if new_solution_score > calculate_score(p_best_j, source):
                        p_best[j] = new_solution
                    new_population.append(new_solution)
                population = copy.deepcopy(new_population)
            instance_score.append(g_best_score)
        instance_dict = {"Instance": instance_file[:-4], "Tour Number": v, "Optimal Score": optimal_score, "Max Score": max(instance_score), 
                            "Min Score": min(instance_score), "Mean Score": sum(instance_score)/len(instance_score),
                            "Gap": 1- (max(instance_score)/optimal_score)}
    except:
        instance_dict = {"Instance": instance_file[:-4], "Tour Number": v, "Optimal Score": optimal_score, "Max Score": None, "Min Score":None, "Mean Score": None,
                         "Gap": None}
    with open('PSO.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=instance_dict.keys())
        writer.writerow(instance_dict)