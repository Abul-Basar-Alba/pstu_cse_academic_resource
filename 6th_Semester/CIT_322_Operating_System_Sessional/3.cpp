#include <iostream>
#include <fstream>
#include <string>
#include <windows.h>

using namespace std;

class SafeLogger {
private:
    HANDLE mutex;
    string fname;
    
public:
    SafeLogger(string f) : fname(f) {
        mutex = CreateMutex(NULL, FALSE, NULL);
        ofstream file(fname);
        file << "=== THREAD-SAFE LOG ===\n\n";
        file.close();
    }
    
    ~SafeLogger() {
        if (mutex) CloseHandle(mutex);
    }
    
    void log(int id, string msg) {
        WaitForSingleObject(mutex, INFINITE);
        
        ofstream file(fname, ios::app);
        if (file.is_open()) {
            file << "[T" << id << "] " << msg << "\n";
            file.flush();
        }
        
        ReleaseMutex(mutex);
    }
};

class UnsafeLogger {
private:
    string fname;
    
public:
    UnsafeLogger(string f) : fname(f) {
        ofstream file(fname);
        file << "=== UNSAFE LOG (NO SYNC) ===\n\n";
        file.close();
    }
    
    void log(int id, string msg) {
        ofstream file(fname, ios::app);
        if (file.is_open()) {
            file << "[T" << id << "] " << msg << "\n";
            file.flush();
        }
    }
};

struct Args {
    SafeLogger* log;
    int id, count;
};

struct UnsafeArgs {
    UnsafeLogger* log;
    int id, count;
};

DWORD WINAPI safeThread(LPVOID arg) {
    Args* a = (Args*)arg;
    
    for (int i = 0; i < a->count; i++) {
        for (int j = 0; j < 100000; j++) volatile int x = j;
        a->log->log(a->id, "Entry " + to_string(i + 1));
        cout << "T" << a->id << " logged " << (i + 1) << "\n";
    }
    
    delete a;
    return 0;
}

DWORD WINAPI unsafeThread(LPVOID arg) {
    UnsafeArgs* a = (UnsafeArgs*)arg;
    
    for (int i = 0; i < a->count; i++) {
        for (int j = 0; j < 100000; j++) volatile int x = j;
        a->log->log(a->id, "Entry " + to_string(i + 1));
        cout << "T" << a->id << " logged " << (i + 1) << "\n";
    }
    
    delete a;
    return 0;
}

int main() {
    cout << "======================================\n"
         << "THREAD-SAFE LOGGING SYSTEM\n"
         << "======================================\n\n";
    
    // Safe logging test
    cout << "[1] SAFE (with mutex)\n";
    cout << "Creating 5 threads, 3 entries each...\n\n";
    
    SafeLogger safe("safe.txt");
    HANDLE threads[5];
    
    for (int i = 0; i < 5; i++) {
        Args* a = new Args{&safe, i, 3};
        threads[i] = CreateThread(NULL, 0, safeThread, a, 0, NULL);
    }
    
    WaitForMultipleObjects(5, threads, TRUE, INFINITE);
    for (int i = 0; i < 5; i++) CloseHandle(threads[i]);
    
    cout << "\n✓ All 15 entries logged safely\n\n";
    
    // Unsafe logging test
    cout << "[2] UNSAFE (no synchronization)\n";
    cout << "Creating 5 threads, 3 entries each...\n\n";
    
    UnsafeLogger unsafe("unsafe.txt");
    HANDLE threads2[5];
    
    for (int i = 0; i < 5; i++) {
        UnsafeArgs* a = new UnsafeArgs{&unsafe, i, 3};
        threads2[i] = CreateThread(NULL, 0, unsafeThread, a, 0, NULL);
    }
    
    WaitForMultipleObjects(5, threads2, TRUE, INFINITE);
    for (int i = 0; i < 5; i++) CloseHandle(threads2[i]);
    
    cout << "\n✗ Entries may be corrupted\n\n";
    
    // Display results
    cout << "======================================\n"
         << "LOG FILES\n"
         << "======================================\n\n";
    
    cout << "--- SAFE.TXT ---\n";
    ifstream f1("safe.txt");
    if (f1.is_open()) {
        string line;
        while (getline(f1, line)) cout << line << "\n";
        f1.close();
    }
    
    cout << "\n--- UNSAFE.TXT ---\n";
    ifstream f2("unsafe.txt");
    if (f2.is_open()) {
        string line;
        while (getline(f2, line)) cout << line << "\n";
        f2.close();
    }
    
    cout << "\n======================================\n"
         << "ANALYSIS\n"
         << "======================================\n";
    cout << "\nSafeLogger:\n"
         << "✓ Mutex ensures mutual exclusion\n"
         << "✓ WaitForSingleObject: Efficient (no spinning)\n"
         << "✓ All entries clean and complete\n\n";
    
    cout << "UnsafeLogger:\n"
         << "✗ No synchronization = race conditions\n"
         << "✗ Entries may interleave or corrupt\n"
         << "✗ Not for multi-threaded use\n";
    
    return 0;
}
