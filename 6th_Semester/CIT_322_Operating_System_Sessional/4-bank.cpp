#include <bits/stdc++.h>
using namespace std;

int balance = 0;
atomic_flag locker = ATOMIC_FLAG_INIT;

void acquire_locker() {
    while (locker.test_and_set(memory_order_acquire));
}

void release_locker() {
    locker.clear(memory_order_release);
}

void func() {
    acquire_locker();

    int local_bal = balance;
    local_bal++;
    cout << local_bal << endl;
    balance = local_bal;

    release_locker();
}

int main() {
    thread t1(func);
    thread t2(func);

    t1.join();
    t2.join();

    cout << "Final balance -> " << balance << endl;

    return 0;
}