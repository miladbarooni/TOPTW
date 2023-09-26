#include <bits/stdc++.h>
#include <algorithm>
#include <math.h>
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
    

    float euclidian_distance(Node a, Node b){
        return sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2));
    }

    bool feasible_tour(Node*  tour_pointer, Node source, int tour_size){
        vector<Node> tour(tour_pointer, tour_pointer + tour_size);
        // cout << tour.size() << " " << source.num << " " << tour_size;
        float t_current = 0;
        float t_max = source.close_time;
        Node current_vertex = source;
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
    
   


    float find_score(Node*  tour_pointer, int tour_size){
        float score = 0;
        vector<Node> tour(tour_pointer, tour_pointer + tour_size);
        for (int j=0; j<tour.size(); j++){
            score+=tour[j].score;
        }
        cout << score << endl;
        return score;
    }
}
