#include <bits/stdc++.h>
#include <algorithm>
using namespace std;




extern "C"{
    
    struct Node{
        int num;
        float x;
        float y;
        float service_time;
        float score;
        int open_time;
        int close_time;
    };

    float find_score(vector<vector<Node>> solution){
        float score = 0;
        for (int i=0; i<solution.size()-1; i++){
            for (int j=0; j<solution[i].size(); j++){
                score+=solution[i][j].score;
            }
        }
        return score;
    }

    int min(int a, int b){
        if (a>=b) return b;
        else return a;
    }

    float euclidian_distance(Node a, Node b){
        return sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2));
    }
    
    struct GreedySort {
        GreedySort(Node current_vertex) { this->current_vertex = current_vertex; }
            bool operator () (Node a, Node b) { 
                float first_ratio = pow(a.score, 2) / (euclidian_distance(a, current_vertex));
                float second_ratio = pow(b.score, 2)  / (euclidian_distance(b, current_vertex));
                // float first_ratio = pow(a.S, 2) / (euclidian_distance(a, current_vertex)+a.O);
                // float second_ratio = a.C - a.O;
                return first_ratio >= second_ratio;

            }

            Node current_vertex;
    };

    double randomNumber(int min, int max){
        static std::mt19937 rng{ std::random_device{}() };
        uniform_real_distribution<double> dist(min, max);
        return dist(rng);
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


    Node** convert_to_pointer_to_pointer(vector<vector<Node>> node_vector){
        int rows = node_vector.size();
        int cols = node_vector[0].size();
        Node** arr = new Node*[rows];
        arr[0] = new Node[rows * cols];
        for (int i = 1; i < rows; i++) {
            arr[i] = arr[0] + i * cols;
        }
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                arr[i][j] = node_vector[i][j];
            }
        }   
        return arr;

    }

    vector<vector<Node>> initial_solution(vector<Node> nodes, int team_number, int nodes_size){
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
                sort(candidate.begin(), candidate.end(), GreedySort(current_vertex));
                int random_candidate = min(randomNumber(0, 7), candidate.size());
                // cout << random_candidate << endl;
                // cout << random_candidate << endl;
                // cout << candidate[random_candidate].num <<
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
                    if (counter == 6) break;
                    else{
                        counter++;
                        continue;
                    }
                }

            }
            solution.push_back(tour);
        }

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

    vector<vector<Node>> local_search_insertion(vector<vector<Node>> greedy_constructive, Node source){
        vector<vector<Node>> solution;
        for (int i=0; i<greedy_constructive.size()-1; i++){
            solution.push_back(greedy_constructive[i]);
        }
        
        vector<Node> remain_vertices = greedy_constructive[greedy_constructive.size()-1];

        vector<vector<Node>> new_solution;
        vector<Node> visited; 
        for (int x=0; x<3; x++){
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
                        if (!feasible_tour(current_tour, source)){
                            current_tour.erase(current_tour.begin()+j); 
                        }
                        else {
                            visited.push_back(new_vertex);
                            break;
                        }
                    

                    }
                    
                }
            }

        }

        return solution;

    }
    void grasp_algorithm(Node* nodes, int team_number, int nodes_size, int number_of_iteration){
        
        srand(time(NULL));

        
        vector<Node> verteces(nodes, nodes + nodes_size);
        float total_score = 0;
        for (int i=0; i<verteces.size(); i++){
            total_score += verteces[i].score;
        }
        Node source = verteces[0];
        
        cout << team_number << endl;
        cout << total_score << endl;
        for (int k=0; k<5; k++){
            time_t timeStart = clock();
            int best_score = 0;
            vector<vector<Node>> best_soloution; 
            for (int i=1; i<=100000; i++){
                // if (i%100 == 0){
                //     cout << "Iteration: " << i << endl;
                //     sleep(10);
                // }
                vector<vector<Node> > greedy_constructive = initial_solution(verteces, team_number, nodes_size);
                // cout << "greedy: " << find_score(greedy_constructive) << endl;
                vector<vector<Node> > local_optimum_solution = local_search_insertion(greedy_constructive, source);
                // cout << "optimum: " << find_score(local_optimum_solution) << endl;
                int score = 0;
                int num_of_vertex = 0;
                for (int i=0; i<local_optimum_solution.size(); i++){
                    for (int j=0; j<local_optimum_solution[i].size(); j++){
                        score+=local_optimum_solution[i][j].score;
                        num_of_vertex ++;
                    }
                }
                
                if (score>=best_score){
                    best_score = score;
                    best_soloution = local_optimum_solution;
                }
                if ((clock() - timeStart) / CLOCKS_PER_SEC >= 30) // time in seconds
                    break;
            }
            int score = 0;
            int num_of_vertex = 0;
            for (int i=0; i<best_soloution.size(); i++){
                // cout << 0 << ' ';
                // cout << "tour number: " << i <<  " Feasebility: " << feasible_tour(best_soloution[i], verteces[0]) <<  endl;
                for (int j=0; j<best_soloution[i].size(); j++){
                    // cout << best_soloution[i][j].num << ' ';
                    score+=best_soloution[i][j].score;
                    num_of_vertex ++;
                }
                // cout << 0 << endl;
                
            }
            // for (int i=0; i<best_soloution.size(); i++){
            //     cout << feasible_tour(best_soloution[i], source) << endl;
            // }
            cout << score << "  " << num_of_vertex << endl;
            // cout << "Gap: " << (total_score - score) / total_score << endl;
        }
    }
}
