#include <bits/stdc++.h>
#include <algorithm>
#include <math.h>
using namespace std;




extern "C"{
    vector<int> tabu_list;
    int tabu_number;
    struct Node{
        int num;
        float x;
        float y;
        float service_time;
        float score;
        int open_time;
        int close_time;
    };
    
    double randomNumber(int min, int max){
        static std::mt19937 rng{ std::random_device{}() };
        uniform_real_distribution<double> dist(min, max);
        return dist(rng);
    }

    int min(int a, int b){
        if (a>=b) return b;
        else return a;
    }

    float euclidian_distance(Node a, Node b){
        return sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2));
    }

    bool feasible_tour(vector<Node> tour, Node source){
        float t_current = 0;
        float t_max = source.close_time;
        Node current_vertex = source;
        // cout << " true: " << true << endl;
        for (int i=0; i<tour.size()+1; i++){
            
            Node next_vertex;
            if (i == tour.size()) next_vertex = source;
            else next_vertex = tour[i];
            if (max((float)t_current+euclidian_distance(next_vertex, current_vertex), (float)next_vertex.open_time) + next_vertex.service_time + euclidian_distance(next_vertex, source) > t_max) return false;
            
            if (t_current + euclidian_distance(next_vertex, current_vertex) <= next_vertex.close_time){
                    t_current = max((float)t_current + euclidian_distance(next_vertex, current_vertex), (float)next_vertex.open_time) + next_vertex.service_time;
                    current_vertex = next_vertex;
                }
            else return false;
        }
        
        return true;
    }
    
    float calculate_tcurrent(vector<Node> tour, Node source){
        float t_current = 0;
        float t_max = source.close_time;
        Node current_vertex = source;
        // cout << " true: " << true << endl;
        for (int i=0; i<tour.size()+1; i++){
            
            Node next_vertex;
            if (i == tour.size()) next_vertex = source;
            else next_vertex = tour[i];
            if (max((float)t_current+euclidian_distance(next_vertex, current_vertex), (float)next_vertex.open_time) + next_vertex.service_time + euclidian_distance(next_vertex, source) > t_max) return -1;
            if (t_current + euclidian_distance(next_vertex, current_vertex) <= next_vertex.close_time){
                    t_current = max((float)t_current + euclidian_distance(next_vertex, current_vertex), (float)next_vertex.open_time) + next_vertex.service_time;
                    current_vertex = next_vertex;
            }
        }
        
        return t_current;
    }

    vector<vector<Node>> swap_in_one_tour(vector<vector<Node>> current_solution, Node source){
        vector<vector<Node>> solution;
        vector<Node> &remain_vertices = current_solution[current_solution.size()-1];
        for (int i=0; i<current_solution.size()-1; i++){
            solution.push_back(current_solution[i]);
        }
        int tour_index = randomNumber(0, solution.size());
        vector<Node> &tour = solution[tour_index];
        vector<Node> copy_tour =  solution[tour_index];
        int counter = 0;
        // cout <<  "before swap " << calculate_tcurrent(tour, source) << endl;
        // float t_current_best = calculate_tcurrent(tour, source);
        do{
            if (tabu_list[tour_index] != 0) break;
            int first_index = rand() % tour.size();
            int second_index = rand() % tour.size();
            swap(tour[first_index], tour[second_index]);
            // t_current_best = calculate_tcurrent(tour, source);
            if (feasible_tour(tour, source)){
                tabu_list[tour_index] = tabu_number;
                break;
            }
            else{
                swap(tour[first_index], tour[second_index]);
            }
            counter ++; 
        } while (counter <= 100);

        solution.push_back(remain_vertices);
        return solution;
    }

    vector<vector<Node>> swap_between_two_tour(vector<vector<Node>> current_solution, Node source){
        srand (time(NULL));
        vector<vector<Node>> solution;
        vector<Node> &remain_vertices = current_solution[current_solution.size()-1];
        for (int i=0; i<current_solution.size()-1; i++){
            solution.push_back(current_solution[i]);
        }
        int first_tour_index = rand() % solution.size();
        vector<Node> &first_tour = solution[first_tour_index];
        int second_tour_index = rand() % solution.size();
        vector<Node> &second_tour = solution[second_tour_index];
        int counter = 0;
        do{
            int first_node_index = rand() % first_tour.size();
            int second_node_index = rand() % second_tour.size();

            swap(first_tour[first_node_index], second_tour[second_node_index]);
            
            if (feasible_tour(first_tour, source) && feasible_tour(second_tour, source)){
                tabu_list[first_tour_index] = tabu_number;
                tabu_list[second_tour_index] = tabu_number;
                break;
            }
            else{
                swap(first_tour[first_node_index], second_tour[second_node_index]);
            }
            counter ++; 
        } while (counter<=100);
        
        solution.push_back(remain_vertices);
        return solution;
    }

    
 
    bool compare_by_open_time(Node a, Node b){
        return a.open_time > b.open_time;
    }

    bool compare_by_close_time(Node a, Node b){
        return a.close_time > b.close_time;
    }

    bool compare_by_close_open_time(Node a, Node b){
        return a.close_time/(a.open_time)+1 > b.close_time/(b.open_time+1);
    }

    vector<vector<Node>> random_initial_solution(vector<Node> nodes, int team_number, int nodes_size){
        // srand (time(NULL));
        srand(time(NULL));
        vector<vector<Node> > solution;
        vector<Node> candidate = nodes;
        Node source = nodes[0];
        int t_max = nodes[0].close_time;
        candidate.erase(candidate.begin());
        for (int i=0; i<team_number; i++){
            float t_current = 0.0;
            vector<Node> tour;
            Node current_vertex = source;
            int counter = 0;
            while (candidate.size() > 0){

                // sort(candidate.begin(), candidate.end(), compare_by_open_time);
                
                // sort(candidate.begin(), candidate.end(), compare_by_close_time);

                // sort(candidate.begin(), candidate.end(), compare_by_close_open_time);


                    
                int random_candidate = randomNumber(0, candidate.size());
                // int random_candidate = rand() % candidate.size();
                Node next_vertex = candidate[random_candidate];
                if (max((float)t_current+euclidian_distance(next_vertex, current_vertex), (float)next_vertex.open_time) + next_vertex.service_time + euclidian_distance(next_vertex, source) > t_max) break;
                if (t_current + euclidian_distance(next_vertex, current_vertex) <= next_vertex.close_time){
                    t_current = max((float)t_current+euclidian_distance(next_vertex, current_vertex), (float)next_vertex.open_time) + next_vertex.service_time;
                    tour.push_back(next_vertex);
                    current_vertex = next_vertex;
                    candidate.erase(candidate.begin() + random_candidate);
                    // cout << next_vertex.id << "  :"  << t_current << endlsolution[i][j].id;

                }
                else{
                    if (counter == candidate.size()) break;
                    else{
                        counter++;
                        continue;
                    }
                }

            }
            solution.push_back(tour);
        }

        // int score = 0;
        // int num_of_vertex = 0;
        // for (int i=0; i<solution.size(); i++){
        //     cout << "tour number: " << i << " Feasebility: " << feasible_tour(solution[i], source) << endl;
        //     for (int j=0; j<solution[i].size(); j++){
        //         cout << solution[i][j].num << endl;
        //         score+=solution[i][j].score;
        //         num_of_vertex ++;
        //     }
        //     cout << "++++++++++++" << endl;
        // }

        // cout << score << "  " << num_of_vertex << endl;
        // cout << "++++++++++++" << endl;
        solution.push_back(candidate);
        return  solution;
    }

    bool find_vertex(vector<Node> tour, Node node){
        for (int i=0; i<tour.size(); i++){
            if (tour[i].num == node.num){
                return true;
            }
        }
        return false;
    }

    vector<vector<Node>> local_search_insertion(vector<vector<Node>> current_solution, Node source){
        vector<vector<Node>> solution;
        for (int i=0; i<current_solution.size()-1; i++){
            solution.push_back(current_solution[i]);
        }
        
        vector<Node> remain_vertices = current_solution[current_solution.size()-1];
        // cout << "current: " << current_tour[0].id << endl;
        // vertex u = remain_vertices[0];
        
        // current_tour.insert(current_tour.begin()+0, u);
        // cout << "current: " << current_tour[0].id << endl;;
        vector<vector<Node>> new_solution;
        vector<Node> visited;
        for (int i=0; i<solution.size(); i++){
            for (int j=0; j<solution[i].size(); j++){
                visited.push_back(solution[i][j]);
            }
        }

        for (int x=0; x<1; x++){
            for (int i=0; i<solution.size(); i++){
                vector<Node> &current_tour = solution[i];

                float t_current = 0;
                
                for (int j=0; j<current_tour.size(); j++){
                    for (int k=0; k<=remain_vertices.size(); k++){
                        // cout << remain_vertices.size() << endl;
                        Node new_vertex = remain_vertices[k];
                        if (find_vertex(visited, new_vertex)) {
                            continue;
                        }
                        current_tour.insert(current_tour.begin()+j, new_vertex); 
                        // cout << "before changing " << endl;
                        if (!feasible_tour(current_tour, source)){
                            current_tour.erase(current_tour.begin()+j); 
                        }
                        else {
                            visited.push_back(new_vertex);
                            break;
                        }
                        // cout << "after changing " << endl;
                    

                    }
                    
                }
            }

        }
        solution.push_back(remain_vertices);
        return solution;
    }

    
    


    float find_score(vector<vector<Node>> solution){
        float score = 0;
        for (int i=0; i<solution.size()-1; i++){
            for (int j=0; j<solution[i].size(); j++){
                score+=solution[i][j].score;
            }
        }
        return score;
    }

    void tabu_algorithm(Node* nodes, int team_number, int nodes_size, int number_of_iteration){
        

        vector<Node> verteces(nodes, nodes + nodes_size);
        Node source = verteces[0];

        
        
        float total_score = 0;
        for (int i=0; i<verteces.size(); i++){
            total_score += verteces[i].score;
        }
        cout << team_number << endl;
        cout << total_score << endl;
        for (int k=0; k<5; k++){
            
            vector<vector<Node> > random_solution = random_initial_solution(verteces, team_number, nodes_size);
            float best_score = find_score(random_solution);
            vector<vector<Node>> best_soloution = random_solution;
            vector<vector<Node>> solution = random_solution;

            tabu_number = team_number;
            for (int i=0; i<=team_number; i++){
                tabu_list.push_back(0);
            }
            for (int i=1; i<=5000; i++){
                // if (i%100 == 0){
                //     cout << i << endl;
                // }
                vector<vector<Node> > swap_in_tour_soloution = swap_in_one_tour(solution, verteces[0]);
                vector<vector<Node> > swap_between_tour_soloution = swap_between_two_tour(swap_in_tour_soloution, verteces[0]);

                vector<vector<Node> > local_optimum_solution = local_search_insertion(swap_between_tour_soloution, source);
                
                float new_solution_score = find_score(local_optimum_solution);
                if (new_solution_score>best_score){
                    best_score = new_solution_score;
                    solution = local_optimum_solution;
                    best_soloution = solution;
                }

                for (int i=0; i<=team_number; i++){
                    if (tabu_list[i] != 0) tabu_list[i]--;
                }
                // for (int i=0; i<=team_number; i++){
                //     cout << tabu_list[i] << "  ";
                // }
                // cout << endl;
            }
            best_soloution = solution;
            int score = 0;
            int num_of_vertex = 0;
            for (int i=0; i<best_soloution.size()-1; i++){
                // cout << 0 << ' ';
                // cout << "tour number: " << i <<  " Feasebility: " << feasible_tour(best_soloution[i], verteces[0]) <<  endl;
                for (int j=0; j<best_soloution[i].size(); j++){
                    // cout << best_soloution[i][j].num << ' ';
                    score+=best_soloution[i][j].score;
                    num_of_vertex ++;
                }
                // cout << 0 << endl;
                
            }
            cout << score << "  " << num_of_vertex << endl;
            // cout << "Gap: " << (total_score - score) / total_score << endl;
        }
    }
}
