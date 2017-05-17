class Solution {
public:
    string getPermutation(int n, int k) {
        int ptable[n];
        //1! to  n!
        string ret = "";
        ptable[0] = 1;
        for(int i=1; i<n; ++i)
            ptable[i] = ptable[i-1] * (i+1);
        vector<char> vtable = {'1','2','3','4','5','6','7','8','9'};
        int tmp;
        while(n-- > 0){
            tmp = k / ptable[n];
            k = k % ptable[n];
            ret += vtable[tmp];
            vtable.erase(vtable.begin() + tmp );
        }
        return ret;

    }
};
