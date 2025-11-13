#include <bits/stdc++.h>
using namespace std;

int N = 8;

int heuristic(vector<int> &state) {
    int h = 0;
    for(int i = 0; i < N; i++)
        for(int j = i + 1; j < N; j++)
            if(state[i] == state[j] || abs(state[i] - state[j]) == abs(i - j))
                h++;
    return h;
}

vector<int> firstChoiceHC(vector<int> state, int maxTrials = 50) {
    while (true) {
        bool improved = false;
        int hCurrent = heuristic(state);

        for (int t = 0; t < maxTrials; t++) {
            int col = rand() % N;
            int row = rand() % N;
            if (row == state[col]) continue;

            vector<int> newState = state;
            newState[col] = row;

            int hNew = heuristic(newState);
            if (hNew < hCurrent) {
                state = newState;
                improved = true;
                break;
            }
        }

        if (!improved) break;
    }
    return state;
}

int main() {
    srand(time(0));
    vector<int> state(N);
    for (int i = 0; i < N; i++)
        state[i] = rand() % N;

    vector<int> solution = firstChoiceHC(state);
    cout << "First-Choice Hill Climbing Solution (Heuristic=" << heuristic(solution) << "):\n";
    for (int i = 0; i < N; i++)
        cout << solution[i] << " ";
    cout << "\n";
}
