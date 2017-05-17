class Solution {
public:
    vector<Interval> insert(vector<Interval>& intervals, Interval newInterval) {
        
        int s = newInterval.start;
        int e = newInterval.end;
        vector<Interval> v;
        int i=0;
        if(intervals.size()==0){
            v.push_back(newInterval);
            return v;
        }
        for(; intervals[i].end < s && i<intervals.size(); ++i){
            v.push_back(intervals[i]);
        }

        for(; intervals[i].start<=e && i<intervals.size(); ++i){
            s = min(intervals[i].start, s);
            e = max(intervals[i].end, e);
        }
        v.push_back(Interval(s,e));
        
        for(; i<intervals.size(); ++i){
            v.push_back(intervals[i]);
        }
        return v;
    }
};
