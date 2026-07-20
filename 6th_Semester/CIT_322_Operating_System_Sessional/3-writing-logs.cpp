#include <bits/stdc++.h>
using namespace std;

mutex mtx;

void func(int i) {
    lock_guard<mutex> lock(mtx);
    cout << "Thread writing log: " << i << endl;
}

int main() {
    thread t1(func, 1);
    thread t2(func, 2);
    thread t3(func, 3);

    t1.join();
    t2.join();
    t3.join();

    return 0;
}