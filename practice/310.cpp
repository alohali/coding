class Solution {
    vector<int> parent;
    vector<int> rank;
public:
    int numIslands(vector<vector<char>>& grid) {
        int nR = grid.size();
        if(nR == 0) return 0;
        int nC = grid[0].size();
        int num=0;
        parent.resize(nR*nC, 0);
        rank.resize(nR*nC, 0);
        for(int i=0; i<parent.size(); i++) {
            parent[i] = i;
        }
        for(int i=0; i<nR; i++) {
            for(int j=0; j<nC; j++) {
                if(grid[i][j] == '0') continue;
                calculateNumIslands(i, j, grid, num);
            }
        }
        return(num);
    }
    
    void calculateNumIslands(int r, int c, vector<vector<char>>& grid, int &num) {
        int cell = 0, cellUp = 0, cellLeft = 0;
        int nR = grid.size();
        int nC = grid[0].size();
        cell = r * nC + c;
        cellLeft = r * nC + c-1;
        cellUp = (r-1) * nC + c;
        num += 1;
        if(c > 0 && grid[r][c-1] == '1') {
            merge(cell, cellLeft);
            num -= 1;
        }
        int rootOfCell = getRoot(cell);
        int rootOfCellUp = 0;
        if(r > 0 && grid[r-1][c] == '1') {
            rootOfCellUp = getRoot(cellUp);
            if(rootOfCell != rootOfCellUp) {
                merge(cell, cellUp);
                num -= 1;
            }
        }
    }
    
    void merge(int a, int b) {
        int root_a = getRoot(a);
        int root_b = getRoot(b);
        int rank_a = rank[root_a];
        int rank_b = rank[root_b];
        if(rank_a > rank_b) {
            parent[root_b] = root_a;
        } else {
            parent[root_a] = root_b;
            if(rank_a == rank_b) {
                pathCompress(b);    
            }
        }
    }
    
    int getRoot(int x) {
        if(parent[x] == x) {
            return x;
        }
        return(getRoot(parent[x]));
    }
    
    int pathCompress(int x) {
        if(parent[x] == x) {
            return x;
        }
        parent[x] = pathCompress(parent[x]);
        return(parent[x]);
    }
};







vector<int> findMinHeightTrees(int n, vector<pair<int, int>>& edges) {
        vector<vector<int>> neighbors(n);
        int numNeighbors[n]{};
        
        for (auto e : edges) {                                  // update stats based on edges
            neighbors[e.first].push_back(e.second), numNeighbors[e.first]++;
            neighbors[e.second].push_back(e.first), numNeighbors[e.second]++;
        }
        
        queue<int> leaves;                                      // use queue to record leaves/sinks
        for (int i = 0; i < n; i++)
            if (numNeighbors[i] <= 1) { leaves.push(i); }       // '<' is for case of n == 1
            
        while (n > 2) {                                         // BFS
            n -= leaves.size();                                 // decrease n for the nodes in leaves
            for (int len = leaves.size(); len; len--) {         // process nodes in leaves
                int cur = leaves.front(); leaves.pop();
                
                for (auto nb : neighbors[cur])                  // update leaves
                    if (--numNeighbors[nb] == 1) { leaves.push(nb); }
            }
        }
        
        vector<int> ans;
        while (leaves.size()) { 
            ans.push_back(leaves.front());                      // construct answer vector
            leaves.pop();
        }
        return ans;
}





////310. Minimum Height Trees
class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<pair<int, int>>& edges) {
        
    }
};