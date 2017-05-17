class Solution {
public:
    vector<vector<int>> pathSum(TreeNode* root, int sum) {
        vector<vector<int>> ret;
        if(root==NULL)  return ret; 
        vector<int> ele;
        dfs(ret, ele, sum, root);

        return ret;
    }
    void dfs(vector<vector<int>> &res, vector<int>& ele, int sum,TreeNode* root){
        if(root==NULL)
            return;
        if(root->left==NULL && root.right==NULL){
            if(root->val==sum ){
                ele.push_back(root->val);
                res.push_back(ele);
                ele.erase(ele.end()-1);
            }
        }
        else if(root->val<sum){
            ele.push_back(root->val);
            dfs(res, ele, sum-root->val, root->left);
            dfs(res, ele, sum-root->val, root->right);
            ele.erase(ele.end()-1);
        }
    }
};
