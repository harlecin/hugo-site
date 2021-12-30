+++
date = "2021-04-13"
title = "Data Passing & Races"
+++

We already covered different ways to pass data to threads during thread construction. Now we will take a look at sending data from the worker to the parent thread as well. To do this, threads follow a very strict sync protocol implemented in the c++ standard. C++ includes a single-use channel to pass data (and also exceptions) back and forth between threads. The two ends of the channel are named:

- **Promise** - Sending end (`std::promise`)
- **Future** -  Receiving end (`std::future`)

and they are included in the `<future>` header.

Let's look at an example:

```
#include <iostream>
#include <thread>
#include <future>

//Note: the function uses move-semantics:
void promiseIncrementByOne(std::promise<int> && prms, int x) {

    //set promise value
    prms.set_value(x + 1);
}

int main() {
    int x = 1;

    // We establish the 2-way communication channel:
    std::promise<int> prms;
    std::future<int> ftr = prms.get_future();

    std::cout << "x = " << x << std::endl;
    std::thread t(promiseIncrementByOne, std::move(prms), x);

    // Return the value from the future
    // If the value is not ready, block the calling thread until it is
    int resFromThread = ftr.get();
    std::cout << "x + 1 = " << resFromThread << std::endl;

    t.join();

}
```
> Note: promises cannot be copied - The promise-future channel is a one-time communication channel, so we need move-semantics to pass promises around

It is also possible to `wait()` or `wait_for()` a promise to set the value before we `get()` the result:

```
auto status = ftr.wait_for(std::chrono::millisceconds(1000));
if (status == std::future_status::ready) {
    ...
} else if (status == std::future_status::timeout || status == std::future_status::deferred) {
    ...
}
```

To pass an exception, we can simply use, e.g. in a try-catch block:
```
try {
    ...
}
catch(...) //catch all exceptions
{
    prms.set_exception(std::current_exception());
}
```
instead of `set_value()`. On the parent side we do:
```
try {
    auto res = ftr.get();
}
catch(std::runtime_error e) 
{
    std::cout << e.what() << std::endl;
}
```

## async

A simpler way to pass data and exceptions is to use: `std::async()` instead of `std::thread()`. Let's revisit our example from the beginning using `async()`:

```
#include <iostream>
#include <future>

int incrementByOne(int x) {
    return x + 1;
}

int main() {
    int x = 1;

    // We use async instead of prms
    std::future<int> ftr = std::async(incrementByOne, x);

    std::cout << "x = " << x << std::endl;

    // Return the value from the future
    int resFromThread = ftr.get();
    std::cout << "x + 1 = " << resFromThread << std::endl;
    
    return 0;
}
```
One of the main benefits of `async` except from being easier to write, is that the system decides if the function should be run (a)synchronosly or not. You can force a specific policy using `std::launch::async` or `std::launch::deferred` as first parameter to `async`.

## Task-based concurrency
As we saw before, `async` let's us specify that a function can be run in parallel and the system decides at runtime if it does. This works because behind the scence the system manages a thread pool and assigns tasks to threads depending on their utilization. Since creating threads takes time and effort by the operating system, it is usually not efficient to run small/short tasks in parallel. Thread pools help reduce this overhead and provide benefits to parallel code even for small tasks.

# Data Races
When passing complex data structures there is always a risk that it includes pointers to some shared data buffer. In these cases it is necessary to perform a deep copy to ensure that no data race occurs. By default only atomic data types implement deep copy out-of-the-box. An alternative to using a deep-copy is to use move-semantics, which has the added benefit of less memory usage. Unique pointers are also useful to prevent data races from occuring since they cannot be copied, only moved.

In my next post, I will cover how to use mutexes to prevent data races and deadlocks.

