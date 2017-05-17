class Solution {
public:

    TreeNode* sortedListToBST(ListNode* head) {
        if(head==NULL)  return NULL;
        node = head;
        ListNode *temp = head;
        int size = 0;
        while(temp!=NULL){
            size++;
            temp = temp->next;
        }
        return recur(0, size);
    }
private:
    ListNode *node;
    TreeNode *recur(int s, int e){
        if(s>=e)    return NULL;
        int mid = (s+e)/2;

        TreeNode *l = recur(s, mid);
        TreeNode *n0 = new TreeNode(node->val);
        node = node->next;
        n0->left = l;

        TreeNode *r = recur(mid+1,e);
        n0->right = r;

        return n0;

    }
};
