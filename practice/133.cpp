
class Solution {


/**
 * Definition for undirected graph.
 * struct UndirectedGraphNode {
 *     int label;
 *     vector<UndirectedGraphNode *> neighbors;
 *     UndirectedGraphNode(int x) : label(x) {};
 * };
 */


public:
    UndirectedGraphNode *cloneGraph(UndirectedGraphNode *node) {
        if(!node)   return nullptr;
        unordered_map<int, UndirectedGraphNode*> labelmap;
        stack<UndirectedGraphNode *> sta0;
        sta0.push(node);

        UndirectedGraphNode* root =  new UndirectedGraphNode(node->label);
        labelmap[root->label] = root;
        root->neighbors.reserve(node->neighbors.size());

        while(!sta0.empty()){
            node = sta0.top();  sta0.pop();
            UndirectedGraphNode* newNode = labelmap[node->label];
            
            for(auto neigh : node->neighbors){

                if(labelmap.find(neigh->label)==labelmap.end()){
                    UndirectedGraphNode* temp =  new UndirectedGraphNode(neigh->label);
                    labelmap[neigh->label] = temp;
                    temp->neighbors.reserve(neigh->neighbors.size());
                    newNode->neighbors.push_back(temp);
                    sta0.push(neigh);
                }else{
                    newNode->neighbors.push_back(labelmap[neigh->label]);
                }
            }
        }
        return root;

    }
};