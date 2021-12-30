+++
date = "2021-04-13"
title = "Mutexes and Locks"
+++

To avoid data races, c++ has a concept called *mutex*, short for Mutual EXclusion. A mutex manages access to a shared resource and ensures that only one thread at a time is able to access the resource:
```
thread 1 --------------
                      |
                  locks resource
                      |
                     mutex ---> access --> shared variable
                      x
                  is blocked
                      |
thread 2 --------------
```
Threads can (un-)lock a mutex to (release) acquire a shared data source.

> Note: Read-only access has to lock a mutex as well if you want to prevent data races!

Using a simple `mutex` takes only 4 steps:
```
#include <mutex>        // 1. include header
...
std::mutex mutex_;      // 2. create mutex
...
mutex_.lock();          // 3. acquire resource
//resource manipulation = critical section
mutex_.unlock();        // 4. release resource
```

There are additional ways we can manage resource access with a `mutex`:

- **recursive_mutex**: allow multiple resource acquisitions from the same thread
- **timed_mutex**: similar to `mutex`, but allows `try_lock_for()` and `try_lock_until()`
- **recursive_timed_mutex**: combination of the above

> Note: try_lock(), try_lock_for() and try_lock_until() return bool and can be used to check if lock was successfully acquired

## Deadlock
One problem with locking a resource is that we need to make sure that it is unlocked as well, which might not be possible if code between `lock()` and `unlock()`, i.e. code in the critical section, throws an exception. In this case, the resource stays locked.

A deadlock can also occur when threads lock a resource and wait for another thread to release a resource which in turn waits for the other thread to release. 

A solution to this problem is similar to the RAII concept: 

## Lock Guards
The standard library provides `std::lock_guard` to acquires a lock, but releases the lock if the life time of an object is over, quite similar to how smart pointers clean up after themselves. On construction, the lock is aquired and released on destruction + it is exception save.

Simply replace the lock/unlock code with:
```
// init mutex
std::mutex mtx;

std::lock_guard<std::mutex> lck(mtx);
```
The lock is released as soon as `lck` goes out-of-scope.

Alternatively, we can use `std::unique_lock` if we want finer control over (un-)locking, which supports:

- deferred locking
- time locking
- recursive locking
- transfer of lock ownership and 
- condition variables

The syntax looks like this:
```
std::mutex mtx;
...

std::unique_lock<std::mutex> lck(mtx);
{
    ...
    {
    lck.unlock();
    ...
    lck.lock();
    }
}
```
The lock will be released when `lck` goes out of scope at the latest. However, you can still create a deadlock if locks are acquired in the wrong order. To (un-)lock multiple mutex together use:
```
std::mutex mutex1, mutex2;

std::lock(mutex1, mutex2);
std::lock_guard<std::mutex> lock2(mutex2, std::adopt_lock);
std::lock_guard<std::mutex> lock1(mutex1, std::adopt_lock);
```

However, it is best to avoid using several mutexes at once if possible.