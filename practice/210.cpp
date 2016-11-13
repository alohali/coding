class Solution {
public:
    vector<int> findOrder(int numCourses, vector<pair<int, int>>& prerequisites) {
        vector<unordered_set<int>> graph = make_graph(numCourses, prerequisites);
        vector<int> ret;
	    vector<int> courses(numCourses);
        if(1){
	        vector<int> degrees = degree(graph);
	        for(int i=0; i<numCourses; ++i){
	        	int j;
	        	for(j=0; j<numCourses; ++j)
	        		if(degrees[j]==0) break;
	        	if(j==numCourses)
	        		return ret;
	        	degrees[j] = -1;
	        	courses[i] = j;
	        	for(int neigh:graph[j]){
	        		degrees[neigh]--;
	        	}
	        }
	    }else{
	    	vector<bool> visited(numCourses, false);
	    	vector<bool> onpath(numCourses,  false);

	    	for(int i=0; i<numCourses; ++i){
	    		if(!visited[i] && !dfs_cycle(graph, i, visited, onpath)){
	    			return ret;
	    		}
	    	}
	    }

        return courses;
    }

private:
	vector<unordered_set<int>> make_graph(int numCourses, vector<pair<int, int>>& prerequisites){
		vector<unordered_set<int>> graph(numCourses);
		for(auto node:prerequisites){
			graph[node.second].insert(node.first);
		}
		return graph;
	}
	vector<int> degree(const vector<unordered_set<int>>& graph){
		vector<int> degree(graph.size(),0);
		for(auto node: graph){
			for(auto successor: node){
				degree[successor]++;
			}
		}
		return degree;
	}
	bool dfs_cycle(const vector<unordered_set<int>>& graph, int node, vector<bool>& visited, vector<bool>& onpath){
		if(visited[node]) return true;
		visited[node] = onpath[node] = true;

		for(auto successor:graph[node]){
			if(onpath[successor] || !dfs_cycle(graph, successor, visited, onpath))
				return false;
		}
		onpath[node] = false;
		return true;
	}
};