class Solution {
    std::vector<int> sizes;
    std::vector<int> id;
public:
    int longestConsecutive(vector<int>& nums) {
        if(nums.size()<=0)  return 0;
        int ret = 1;
        for(int i=0;i<nums.size();++i){
            id.push_back(i);
            sizes.push_back(1);
        }
        unordered_map<int,int> set0; 
        for(int i=0;i<nums.size();++i){
            int num = nums[i];
            if(set0.find(num)==set0.end()){
                set0[num] = i;
                int size0 = 0;
                if(set0.find(num-1)!=set0.end()){
                    size0 = merge(i, set0[num-1]);
                }
                if(set0.find(num+1)!=set0.end()){
                    size0 = merge(i, set0[num+1]);
                }
                if(size0>ret)
                    ret = size0;
            }
        }
        return ret;
    }

    int find(int a){
        while(id[a]!=a){
            id[a] = id[id[a]];
            a = id[a];
        }
        return a;
    }

    int merge(int a, int b){
        int ida = find(a);
        int idb = find(b);

        if(ida>idb){
            id[idb] = ida;
            return sizes[ida] += sizes[idb];
        }else{
            id[ida] = idb;
            return sizes[idb] += sizes[ida];
        }
    }

};