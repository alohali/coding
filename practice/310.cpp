////310. Minimum Height Trees
class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<pair<int, int>>& edges) {
        vector<int>ret;
        if(n>2) {
            vector<unordered_set<int>> graph = makeGraph(n, edges);
            int Height;
            int root = bfs(0,graph, Height);
            bfs(root, graph, Height);
            ret=getRoots(root, graph, Height);
        }else if(n==1){
            ret.push_back(0);
        }else if(n==2){
            ret.push_back(0);
            ret.push_back(1);
        }
        return ret;
    }

    vector<unordered_set<int>> makeGraph(int n, const vector<pair<int, int>>& edges){
        vector<unordered_set<int>> graph(n);
        for(auto edge : edges){
            graph[edge.first].insert(edge.second);
            graph[edge.second].insert(edge.first);
        }
        return graph;
    }

    int bfs(int root, vector<unordered_set<int>> &graph, int&Height){
        int ret;
        queue<int> q0; q0.push(root);
        vector<int> dist(graph.size(), -1);
        dist[root] = 0;

        while(!q0.empty()){
            ret = q0.front(); q0.pop();
            for(auto neigh : graph[ret]){
                if(dist[neigh]<0){
                    q0.push(neigh);
                    dist[neigh] = dist[ret]+1;
                }
            }
        }
        Height = dist[ret];
        return ret;
    }
    vector<int> getRoots(int root, vector<unordered_set<int>> &graph, int Height){
        vector<int> ret;
        queue<int> q0; q0.push(root);
        vector<int> dist(graph.size(), -1);
        dist[root] = 0;
        int level = Height/2;
        int level2 = (Height%2)+level;
        while(!q0.empty()){
            int node = q0.front(); q0.pop();
            for(auto neigh : graph[node]){
                if(dist[neigh]<0){
                    q0.push(neigh);
                    dist[neigh] = dist[node]+1;
                    if((dist[neigh]==level) || dist[neigh]==level2){
                        ret.push_back(neigh);
                    }
                }
            }
        }
        return ret;
    }
};