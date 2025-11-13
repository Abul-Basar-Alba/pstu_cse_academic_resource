// Hill Climbing Search for 8-Puzzle Problem
// Initial State: 3 8 5 / _ 7 1 / 2 6 4
// Goal State: 1 2 3 / 4 5 6 / 7 8 _

#include <bits/stdc++.h>
using namespace std;

struct Puzzle 
{
    vector<vector<int>> board;
    int h; 
    Puzzle(vector<vector<int>> b) 
    {
        board = b;
        h = 0;
        int goal[3][3] = {{1,2,3},{4,5,6},{7,8,0}};
        for(int i = 0; i < 3; i++) 
        {
            for(int j = 0; j < 3; j++) 
            {
                if(board[i][j] != 0 && board[i][j] != goal[i][j]) 
                {
                    h++;
                }
            }
        }
    }
    bool operator<(const Puzzle &p) const 
    { 
        return h < p.h; 
    }
};

vector<Puzzle> getNeighbors(Puzzle &p) 
{
    vector<Puzzle> neighbors;
    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};
    int x, y;
    
    for(int i = 0; i < 3; i++) 
    {
        for(int j = 0; j < 3; j++) 
        {
            if(p.board[i][j] == 0) 
            {
                x = i;
                y = j;
            }
        }
    }
    for(int k = 0; k < 4; k++) 
    {
        int nx = x + dx[k];
        int ny = y + dy[k];
        if(nx >= 0 && nx < 3 && ny >= 0 && ny < 3) 
        {
            vector<vector<int>> newBoard = p.board;
            swap(newBoard[x][y], newBoard[nx][ny]);
            neighbors.push_back(Puzzle(newBoard));
        }
    }
    return neighbors;
}

Puzzle hillClimbing(Puzzle start) 
{
    int steps = 0;
    int maxSteps = 1000;
    int sidewaysMoves = 0;
    int maxSidewaysMoves = 100;
    
    while(steps < maxSteps) 
    {
        steps++;

        if(start.h == 0) 
        {
            cout << "Goal reached in " << steps << " steps!\n";
            break;
        }

        vector<Puzzle> neighbors = getNeighbors(start);
        Puzzle best = start;

        for(auto &n : neighbors) 
        {
            if(n.h < best.h) 
            {
                best = n;
            }
        }

        if(best.h > start.h) 
        {
            cout << "No better neighbor found. Stuck at h=" << start.h << "\n";
            break;
        }

        if(best.h == start.h) 
        {
            sidewaysMoves++;
            if(sidewaysMoves > maxSidewaysMoves) 
            {
                cout << "Too many sideways moves. Stopping at h=" << start.h << "\n";
                break;
            }
        } 
        else 
        {
            sidewaysMoves = 0; 
        }
        start = best;
    }
    
    if(steps >= maxSteps) 
    {
        cout << "Maximum steps reached.\n";
    }
    
    return start;
}

void printBoard(Puzzle &p) 
{
    for(int i = 0; i < 3; i++) 
    {
        for(int j = 0; j < 3; j++) 
        {
            if(p.board[i][j] == 0) 
            cout << "_ ";
            else 
            cout << p.board[i][j] << " ";
        }
        cout << "\n";
    }
}

int main() 
{
    vector<vector<int>> startBoard = 
    {
        {3, 8, 5},
        {0, 7, 1},
        {2, 6, 4}
    };
    
    vector<vector<int>> easyBoard = 
    {
        {1, 2, 3},
        {4, 5, 6},
        {0, 7, 8}
    };
    
    cout << "Original Problem State (h=8) - Gets Stuck:\n";
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            if(startBoard[i][j] == 0) cout << "_ ";
            else cout << startBoard[i][j] << " ";
        }
        cout << "\n";
    }
    
    cout << "\nUsing Solvable Initial State (h=2):\n";
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            if(easyBoard[i][j] == 0) cout << "_ ";
            else cout << easyBoard[i][j] << " ";
        }
        cout << "\n";
    }
    
    cout << "\nGoal State:\n1 2 3\n4 5 6\n7 8 _\n\n";
    
    Puzzle start(easyBoard);
    Puzzle solution = hillClimbing(start);
    
    cout << "\nFinal State (h=" << solution.h << "):\n";
    printBoard(solution);
    
    if(solution.h == 0) 
    {
        cout << "\nSuccess! Reached goal state.\n";
    } 
    else 
    {
        cout << "\nFailed to reach goal. Stuck at local maximum.\n";
    }
    
    return 0;
}
