class Solution {
public:
    string simplifyPath(string path) {
        vector<string> folder;
        string f = "";
        string ret = "";
        int dot_cnt = 0;
        for(int i=0; i<path.length(); ++i){
            if(path[i]=='/'){
                dot_cnt = 0;
                if(f=="")
                    continue;
                else{
                    folder.push_back(f);
                    f = "";
                }
            }
            else if(path[i]=='.' && f==""){
                dot_cnt++;
                if(dot_cnt==3){
                    f = "...";
                    dot_cnt = 0;
                }
                else if(i==path.length()-1 || path[i+1]!='.'){
                    if(i==path.length()-1 || path[i+1]=='/'){
                        if(dot_cnt==2){
                            if(folder.size())
                                folder.erase(folder.end()-1);
                        }else{
                            dot_cnt = 0;
                        }
                    }
                    else{
                        f = dot_cnt==1? ".":"..";
                    }
                }
            }
            else{
                dot_cnt = 0;
                f += path[i];
            }
        }
        for(int i=0;i < folder.size(); ++i){
            ret += "/" + folder[i];
        }
        if(f!="" )
            ret += "/"+f;
        else if(ret=="")
            ret = "/";
        return ret;
    }
};
