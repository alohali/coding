class Solution {
public:
    void sortColors(vector<int>& nums) {
        int l = 0;
        for(int i=0; i<nums.size(); ++i){
            if(nums[i]==0){
                if(i!=l)
                    swap(nums[i],nums[l++]);
                ++l;
            } 
        }

        for(int i=l; i<nums.size(); ++i){
            if(nums[i]==1){
                if(i!=l)
                    swap(nums[i],nums[l++]);
                ++l;
            } 
        }
        return;
    }
};
