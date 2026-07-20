#include <bits/stdc++.h>
#include <windows.h>

using namespace std;

// Shared variable - NO SYNCHRONIZATION (Race Condition!)
int next_id = 1000;

// Structure to store student information
struct Student {
    string name;
    int id;
};

vector<Student> students;

// Function to simulate student admission
DWORD WINAPI admitStudent(LPVOID arg) {
    string* name = (string*)arg;
    
    // RACE CONDITION: Multiple threads reading, incrementing, and assigning the same ID
    int temp = next_id;        // Thread reads current value
    
    // Simulate some processing time (increases chance of race condition)
    for (int i = 0; i < 100000; i++) {
        volatile int x = i;    // Busy loop to increase race condition likelihood
    }
    
    next_id = temp + 1;        // Thread increments and writes back
    
    Student s;
    s.name = *name;
    s.id = temp;
    
    students.push_back(s);
    
    delete name;
    return 0;
}

int main() {
    cout << "RACE CONDITION DEMONSTRATION" << endl;
    cout << "University Student ID Assignment System" << endl;
    
    cout << "Creating 20 threads to admit students simultaneously...\n" << endl;
    
    vector<HANDLE> threads;
    threads.resize(20);
    
    // Create 20 threads, each admitting a student
    for (int i = 0; i < 20; i++) {
        string *name = new string("Student_" + to_string(i + 1));
        threads[i] = CreateThread(NULL, 0, admitStudent, (LPVOID)name, 0, NULL);
        if (threads[i] == NULL) {
            cout << "Error: Could not create thread " << i << endl;
            return 1;
        }
    }
    
    // Wait for all threads to complete
    for (int i = 0; i < 20; i++) {
        WaitForSingleObject(threads[i], INFINITE);
        CloseHandle(threads[i]);
    }
    
    cout << "All admission requests processed!\n" << endl;
    
    // Display assigned student IDs
    cout << "Assigned Student IDs:" << endl;
    cout << "--------------------" << endl;
    for (auto& student : students) {
        cout << student.name << " -> ID: " << student.id << endl;
    }
    
    cout << "\n========== RACE CONDITION ANALYSIS ==========" << endl;
    
    // Check for duplicate IDs
    set<int> unique_ids;
    map<int, int> id_count;
    
    for (auto& student : students) {
        unique_ids.insert(student.id);
        id_count[student.id]++;
    }
    
    cout << "Total students: " << students.size() << endl;
    cout << "Unique IDs assigned: " << unique_ids.size() << endl;
    
    if (unique_ids.size() < students.size()) {
        cout << "\n*** RACE CONDITION DETECTED! ***" << endl;
        cout << "Multiple students have the SAME ID!\n" << endl;
        
        cout << "Duplicate IDs:" << endl;
        for (auto& pair : id_count) {
            if (pair.second > 1) {
                cout << "  ID " << pair.first << " assigned to " << pair.second 
                     << " students" << endl;
            }
        }
    } else {
        cout << "\nNo duplicates this run (race condition didn't manifest)." << endl;
        cout << "Run again - race conditions are non-deterministic!" << endl;
    }
    
    cout << "\nFinal next_id value: " << next_id << endl;
    cout << "(Expected: 1020, Actual: " << next_id << ")" << endl;
    cout << "The discrepancy shows lost updates due to race condition!" << endl;
    
    return 0;
}