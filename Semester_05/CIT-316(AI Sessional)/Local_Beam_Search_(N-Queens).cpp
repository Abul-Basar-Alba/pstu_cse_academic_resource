#include <bits/stdc++.h>
using namespace std;

int N = 8;

int heuristic(vector<int> &state) 
{
    int h = 0;
    for(int i=0;i<N;i++)
        for(int j=i+1;j<N;j++)
            if(state[i]==state[j] || abs(state[i]-state[j])==abs(i-j)) h++;
    return h;
}

vector<int> localBeamSearch(int k=3, int maxIterations=100)
 {
    srand(time(0));
    vector<vector<int>> states(k);
    for(int i=0;i<k;i++)
        for(int j=0;j<N;j++) states[i].push_back(rand()%N);

    for(int iter=0; iter<maxIterations; iter++) 
    {
        vector<vector<int>> allNeighbors;

        for(auto &state: states) 
        {
            for(int col=0; col<N; col++) 
            {
                for(int row=0; row<N; row++) 
                {
                    if(row == state[col]) 
                    continue;
                    vector<int> neighbor = state;
                    neighbor[col] = row;
                    allNeighbors.push_back(neighbor);
                }
            }
        }
        sort(allNeighbors.begin(), allNeighbors.end(), [](vector<int> &a, vector<int> &b){
            int ha=0,hb=0;
            for(int i=0;i<a.size();i++)
                for(int j=i+1;j<a.size();j++)
                {
                    if(a[i]==a[j] || abs(a[i]-a[j])==abs(i-j)) 
                    ha++;
                    if(b[i]==b[j] || abs(b[i]-b[j])==abs(i-j))
                     hb++;
                }
            return ha<hb;
        });

        states.assign(allNeighbors.begin(), allNeighbors.begin()+k);
        if(heuristic(states[0])==0) break;
    }

    return states[0];
}

int main() 
{
    vector<int> solution = localBeamSearch();
    cout << "Local Beam Search Solution (Heuristic=" << heuristic(solution) << "):\n";
    for(int i=0;i<N;i++) cout << solution[i] << " ";
    cout << "\n";
}
