
// #include <bits/stdc++.h>
// using namespace std;
// int N = 8;
// int heuristic(vector<int> &state) 
// {
//     int h = 0;
//     for(int i = 0; i < N; i++) 
//     {
//         for(int j = i+1; j < N; j++) 
//         {
//             if(state[i] == state[j]) 
//             h++;
//             else if(abs(state[i] - state[j]) == abs(i - j)) 
//             h++;
//         }
//     }
//     return h;
// }

// void printBoard(vector<int> &state) 
// {
//     cout << "\nChessboard (Q = Queen, . = Empty):\n";
//     cout << "  ";
//     for(int i = 0; i < N; i++) cout << i << " ";
//     cout << "\n";
    
//     for(int row = 0; row < N; row++) 
//     {
//         cout << row << " ";
//         for(int col = 0; col < N; col++) 
//         {
//             if(state[col] == row) cout << "Q ";
//             else cout << ". ";
//         }
//         cout << "\n";
//     }
//     cout << "\n";
// }

// void printState(vector<int> &state, string label) 
// {
//     cout << label << ": [";
//     for(int i = 0; i < N; i++) 
//     {
//         cout << state[i];
//         if(i < N-1) cout << ", ";
//     }
//     cout << "] (Conflicts: " << heuristic(state) << ")\n";
// }

// vector<int> hillClimb(vector<int> state) 
// {
//     int iteration = 0;
//     while(true) 
//     {
//         iteration++;
//         int currentH = heuristic(state);
        
//         cout << "\n--- Iteration " << iteration << " ---\n";
//         printState(state, "Current State");
//         vector<int> bestState = state;
//         int bestH = currentH;
//         for(int col = 0; col < N; col++) 
//         {
//             int originalRow = state[col];
//             for(int row = 0; row < N; row++) 
//             {
//                 if(row == originalRow) 
//                 continue; 
                
//                 state[col] = row;
//                 int h = heuristic(state);

//                 if(h < bestH) 
//                 {
//                     bestH = h;
//                     bestState = state;
//                 }
//             }
//             state[col] = originalRow;
//         }
        
//         if(bestH >= currentH) 
//         {
//             cout << "\nNo better neighbor found. Stopping.\n";
//             cout << "Final heuristic value: " << currentH << "\n";
//             if(currentH == 0) 
//             {
//                 cout << "SUCCESS! Solution found with 0 conflicts.\n";
//             } 
//             else 
//             {
//                 cout << "STUCK at local optimum with " << currentH << " conflicts.\n";
//             }
//             break;
//         }
//         cout << "Better state found! Moving from h=" << currentH << " to h=" << bestH << "\n";
//         state = bestState;
//     }
    
//     return state;
// }

// int main() 
// {

//     cout << "   8-QUEENS PROBLEM - HILL CLIMBING\n";
    
//     srand(42); 
    
//     vector<int> state(N);
//     for(int i = 0; i < N; i++) 
//     {
//         state[i] = rand() % N;
//     }
    
//     cout << "INITIAL STATE (Fig 2.1 - Random placement):\n";
//     printState(state, "State");
//     printBoard(state);
    
//     vector<int> solution = hillClimb(state);
    
//     cout << "   GOAL STATE (Fig 2.2 - Solution)\n";

//     printState(solution, "Final State");
//     printBoard(solution);

//     int finalConflicts = heuristic(solution);
//     cout << "Final number of conflicts: " << finalConflicts << "\n";
    
//     if(finalConflicts == 0) 
//     {
//         cout << "\nSUCCESS! All 8 queens placed safely.\n";
//         cout << "No queen attacks any other queen.\n";
//     } 
//     else 
//     {
//         cout << "\nWARNING: Local optimum reached.\n";
//         cout << "Try running again for different initial state.\n";
//     }
    
//     return 0;
// }





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

vector<int> hillClimb(vector<int> state) 
{
    while(true) 
    {
        int currentH = heuristic(state);
        vector<int> bestState = state;
        int bestH = currentH;

        for(int col=0; col<N; col++) 
        {
            int originalRow = state[col];
            for(int row=0; row<N; row++) 
            {
                if(row==originalRow) continue;
                state[col] = row;
                int h = heuristic(state);
                if(h < bestH) 
                {
                    bestH = h;
                    bestState = state;
                }
            }
            state[col] = originalRow;
        }

        if(bestH >= currentH) break;
        state = bestState;
    }
    return state;
}

int main() 
{
    srand(time(0));
    vector<int> state(N);
    for(int i=0;i<N;i++) 
    state[i] = rand()%N;

    vector<int> solution = hillClimb(state);
    cout << "Hill Climbing Solution (Heuristic=" << heuristic(solution) << "):\n";
    for(int i=0;i<N;i++) 
    cout << solution[i] << " ";
    cout << "\n";
}



