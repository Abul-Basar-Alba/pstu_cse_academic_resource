#include <bits/stdc++.h>
#include <windows.h>

using namespace std;

class Lock {
private:
    volatile bool locked;
    HANDLE mtx;
    
public:
    Lock() : locked(false) {
        mtx = CreateMutex(NULL, FALSE, NULL);
    }
    
    ~Lock() {
        if (mtx) CloseHandle(mtx);
    }
    
    // Atomic test and set
    bool acquire() {
        WaitForSingleObject(mtx, INFINITE);
        bool old = locked;
        locked = true;
        ReleaseMutex(mtx);
        return old;
    }
    
    void release() {
        locked = false;
    }
};

int counter = 0;

void safeIncrement(Lock& lock, int id, int ops) {
    for (int i = 0; i < ops; i++) {
        // Spin until lock acquired
        while (lock.acquire());
        
        // Critical section
        int old = counter;
        for (int j = 0; j < 100000; j++) volatile int x = j;
        counter = old + 1;
        
        cout << "T" << id << " -> " << counter << "\n";
        lock.release();
        Sleep(0);
    }
}

void unsafeIncrement(int id, int ops) {
    for (int i = 0; i < ops; i++) {
        // No sync - race condition!
        int old = counter;
        for (int j = 0; j < 100000; j++) volatile int x = j;
        counter = old + 1;
        
        cout << "T" << id << " -> " << counter << "\n";
        Sleep(0);
    }
}

struct Args {
    Lock* lock;
    int id, ops;
};

DWORD WINAPI safe(LPVOID arg) {
    Args* a = (Args*)arg;
    safeIncrement(*a->lock, a->id, a->ops);
    delete a;
    return 0;
}

DWORD WINAPI unsafe(LPVOID arg) {
    Args* a = (Args*)arg;
    unsafeIncrement(a->id, a->ops);
    delete a;
    return 0;
}

int main() {
    cout << "======================================\n"
         << "TEST-AND-SET (TAS) INSTRUCTION\n"
         << "======================================\n\n";
    
    // Safe with Test-And-Set
    cout << "[1] SAFE: Using Test-And-Set\n"
         << "5 threads, 5 increments each\n"
         << "Expected: 25\n\n";
    
    counter = 0;
    Lock tas;
    HANDLE t1[5];
    
    for (int i = 0; i < 5; i++) {
        Args* a = new Args{&tas, i, 5};
        t1[i] = CreateThread(NULL, 0, safe, a, 0, NULL);
    }
    
    WaitForMultipleObjects(5, t1, TRUE, INFINITE);
    for (int i = 0; i < 5; i++) CloseHandle(t1[i]);
    
    cout << "\n✓ Result: " << counter << " "
         << (counter == 25 ? "(CORRECT)" : "(WRONG)") << "\n\n";
    
    // Unsafe without synchronization
    cout << "---\n\n"
         << "[2] UNSAFE: No Synchronization\n"
         << "5 threads, 5 increments each\n"
         << "Expected: 25\n\n";
    
    counter = 0;
    HANDLE t2[5];
    
    for (int i = 0; i < 5; i++) {
        Args* a = new Args{NULL, i, 5};
        t2[i] = CreateThread(NULL, 0, unsafe, a, 0, NULL);
    }
    
    WaitForMultipleObjects(5, t2, TRUE, INFINITE);
    for (int i = 0; i < 5; i++) CloseHandle(t2[i]);
    
    cout << "\n✗ Result: " << counter << " "
         << (counter != 25 ? "(RACE CONDITION!)" : "(survived)") << "\n\n";
    
    cout << "======================================\n"
         << "EXPLANATION\n"
         << "======================================\n\n";
    
    cout << "Test-And-Set Atomic Operation:\n"
         << "bool test_and_set(bool* target) {\n"
         << "  old = *target;    // Read\n"
         << "  *target = true;   // Set\n"
         << "  return old;       // Return old\n"
         << "}\n\n";
    
    cout << "Usage:\n"
         << "while (test_and_set(&lock))  // Spin if locked\n"
         << "  ;  // Keep trying\n"
         << "// Now we have lock!\n"
         << "critical_section();\n"
         << "lock = false;  // Release\n\n";
    
    cout << "Key Properties:\n"
         << "✓ Atomic: No interruption between read and set\n"
         << "✓ Hardware: CPU guarantees atomicity\n"
         << "✓ Effective: Prevents race conditions\n"
         << "✗ Inefficient: Busy spinning wastes CPU\n";
    
    return 0;
}
