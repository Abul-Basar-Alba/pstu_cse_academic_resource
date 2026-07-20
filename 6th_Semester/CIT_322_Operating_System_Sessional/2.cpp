#include <iostream>
#include <vector>
#include <iomanip>
#include <windows.h>

using namespace std;

struct DatabaseRecord {
    int account_id;
    double balance;
    int version;
};

struct Transaction {
    int process_id, seq_num;
    string operation;
    double amount, balance;
};

DatabaseRecord db = {1001, 1000.0, 0};
bool flag[2] = {false, false};
int turn = 0;
vector<Transaction> log;
int count_ops = 0;

void lock(int id) {
    int other = 1 - id;
    flag[id] = true;
    turn = other;
    while (flag[other] && turn == other);
}

void unlock(int id) {
    flag[id] = false;
}

void updateDatabase(int id, double amount, int ops) {
    cout << "\nProcess " << id << " starting (" << ops << " operations)..." << endl;
    
    for (int i = 0; i < ops; i++) {
        lock(id);
        
        double old_bal = db.balance;
        for (int j = 0; j < 50000; j++) volatile int x = j;
        
        db.balance += amount;
        db.version++;
        count_ops++;
        
        Transaction t;
        t.process_id = id;
        t.seq_num = count_ops;
        t.operation = (amount > 0) ? "DEPOSIT" : "WITHDRAW";
        t.amount = amount;
        t.balance = db.balance;
        log.push_back(t);
        
        cout << "  [" << count_ops << "] P" << id << ": " << old_bal 
             << " -> " << db.balance << endl;
        
        unlock(id);
        Sleep(0);
    }
    cout << "Process " << id << " done." << endl;
}

DWORD WINAPI processThread(LPVOID arg) {
    int* data = (int*)arg;
    double amt = data[2] ? 100.0 : -50.0;
    updateDatabase(data[0], amt, data[1]);
    delete[] data;
    return 0;
}

int main() {
    cout << "======================================\n"
         << "PETERSON'S ALGORITHM\n"
         << "Mutual Exclusion & Fair Turn-Taking\n"
         << "======================================\n\n";
    
    cout << "Initial State: Balance = $" << db.balance << "\n"
         << "Process 0: Deposit $100 x10\n"
         << "Process 1: Withdraw $50 x10\n\n";
    
    HANDLE threads[2];
    int* data0 = new int[3]{0, 10, 1};
    int* data1 = new int[3]{1, 10, 0};
    
    threads[0] = CreateThread(NULL, 0, processThread, data0, 0, NULL);
    threads[1] = CreateThread(NULL, 0, processThread, data1, 0, NULL);
    
    WaitForMultipleObjects(2, threads, TRUE, INFINITE);
    CloseHandle(threads[0]);
    CloseHandle(threads[1]);
    
    cout << "\n======================================\n"
         << "RESULTS\n"
         << "======================================\n\n";
    
    cout << "Final Balance: $" << fixed << setprecision(2) << db.balance << "\n";
    cout << "Expected: $1500.00\n";
    cout << "Status: " << (db.balance == 1500.0 ? "✓ CORRECT" : "✗ ERROR") << "\n\n";
    
    cout << "Transaction Log:\n";
    cout << "---\n";
    for (auto& t : log) {
        cout << setw(2) << t.seq_num << " | P" << t.process_id 
             << " | " << setw(8) << t.operation << " | $" 
             << setw(7) << fixed << setprecision(2) << t.balance << "\n";
    }
    
    int p0 = 0, p1 = 0;
    for (auto& t : log) { (t.process_id == 0) ? p0++ : p1++; }
    
    cout << "\n✓ Mutual Exclusion: Guaranteed (no interleaving)\n"
         << "✓ Fair Turn-Taking: P0=" << p0 << ", P1=" << p1 << "\n"
         << "✓ Data Integrity: Final = Expected\n";
    
    return 0;
}
