+++
date = "2021-04-03"
title = "Intro to C++ Concurrency"
+++


Let's start with the very basics before we work through a simple example in c++:

## Overview

When we want to perform multiple pieces of work simultaneously, we can either choose to run them in a synchronos or asynchronos manner:

**Synchronous**
```
                         time
main()      ---------        -------------------------> 
          func()    |        | return()
thread()            ------->
```

**Asynchronous**
```
                         time
main()      ------------------------------------------> 
          func()    |        
thread()            ------->
```

As you can see in the diagrams above, synchronous programs pause execution of the program that started them until completition while asynchronous programs run along side the calling thread.

Two very important concepts we need to define first are:

- **process**: Also called task = running computer program, controlled by the os
- **thread**: Also called "light-weight processes". Are concurrent execution units within a process

The os can set a process into one of several states:

- **Ready**: After creation the process is loaded into main memory and waiting in the CPU queue managed by the os to be executed
- **Running**: Os has given the process CPU time to run
- **Blocked**: Process is waiting for an event (e.g. i/o, resources)
- **Terminated**: Process completes or is killed
- **Ready suspended**: Process was moved out of main memory, but is ready as soon as it is moved to main memory again
- **Blocked suspended**: Process was moved out of main memory, but is blocked as soon as it is moved to main memory again

The os manages processes with a **scheduler** that can assign cpu time to different processes.

Managing processes is quite a lot of work for the os and a more light-weight and resource friendly way is to utilize threads:

As already stated, threads are concurrent execution units within a process. They are easier to create and destroy (like up to 100x).

Threads can share resources with processes such as files, network connections and memory while processes are isolated from each other. Quite similar to processes, threads also have states:

- **New**: When it is created a thread is in the new state - This state does not take cpu resources
- **Runnable**: Now the thread can be run if it is scheduled
- **Blocked**: Again, the threat does not consume cpu time and is waiting to resume execution

## C++ Implementation

Concurrency support was first included in the standard library in c++11. Before that you had to rely on third-party implementations or the native concurrency options provided by each os.

Simply include the `<thread>` header file and you are ready to go :)

Each running program has a "main thread" and potentially other threads as well. Each thread has a unique id:

```
#include <iostream>
#include <thread>

int main()
{
    unsigned int nCores = std::thread::hardware_concurrency();
    std::cout << "# Cores = " << nCores << std::endl;
    std::cout << "Thread id = " << std::this_thread::get_id() << std::endl;

    return 0;
}
```
On my machine I get:
```
# Cores = 12
Thread id = 9788
```

Now let's create a second thread:
```
#include <iostream>
#include <thread>

void foo()
{
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // simulate work
    std::cout << "Finished work in thread with id = " << std::this_thread::get_id() << std::endl; 
}

int main()
{
    // create thread
    std::thread t(foo);

    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    std::cout << "Finished work in main thread with id = " << std::this_thread::get_id() << std::endl;

    // Threads are non-blocking!
    // Use join() to block execution of the parent until the child thread finishes
    t.join();

    return 0;
}
```
We get:
```
Finished work in main thread with id = 8560
Finished work in thread with id = 18548
```

> Note: If you use g++ do not forget to add the flag -pthread! The MSVC compiler works without a flag.

Concurrent programs are non-deterministic in their execution, i.e. it cannot be predicted which thread will execute at which point in time. If we want to enforce a specific order of execution we can do this for example by strategically placing the `.join()` call.

By default, if you do not join threads the program will crash. You can use `t.detach()` to "detach" a thread. Now the program will continue executing, not waiting for the thread. The thread destructor does not block execution nor does it terminate the thread. A detached thread cannot be joined again!

## Threads with Function Objects

In the example above we passed a simple function to a worker thread. But we can also pass a class instance to a thread if it implements the function-call operator. So let's create a class with an overloaded `()` operator:

```
#include <iostream>
#include <thread>

class Thread {
    public:
        void operator()() {
            std::cout << "Thread object created" << std::endl;
        }
};

int main()
{
    // create thread
    // c++ most vexing parse:
    // std::thread t(Thread()); --> this will not work
   
    // All of the following will:
    std::thread t1{Thread()};
    std::thread t2((Thread()));
    std::thread t3 = std::thread(Thread());

    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    std::cout << "Finished work in main thread with id = " << std::this_thread::get_id() << std::endl;

    // Threads are non-blocking!
    // Use join() to block execution of the parent until the child thread finishes
    t1.join();
    t2.join();
    t3.join();

    return 0;
}
```

The code above illustrates the *most vexing parse* in c++: When the c++ grammar cannot differentiate between the construction of a class instance and a function, the compiler is required to interprete it as a function.

In all three cases, the function object is copied to the thread and the new thread calls the `()`operator. So one way to pass data to a thread is to pass it to the constructor of our class.

## Detour: Lambdas

We can also use lambdas to start threads and pass data to it. A lambda function is a function object, also called 'functor'. 

Lambdas consist of four parts:
```
       []           mutable           ()              {}
   capture list
    &, =, vars      optional     parameter list       body
```
By default, a lambda has only access to variables in its enclosing `{}`. By passing variables in the capture list we make them visible to our lambda function. If we pass `&` we make all variables from the enclosing scope visible by reference, if we pass `=` we copy them by value or alternatively we specify the variables we want to capture individually. All variables in a capture list are immutable by default. If we want to change them, we have to include `mutable` behind the capture list. For a detailed intro to lambdas checkout this [blog post](https://blog.feabhas.com/2014/03/demystifying-c-lambdas/).

Some example lambdas can look like this:
```
    int x = 0; // Define an integer variable

    // By reference
    auto l0 = [&x]() { std::cout << x << std::endl; };
    l0();
    auto l1 = [&x]() mutable { std::cout << ++x << std::endl; };
    l1();
    
    // capture by value
    // auto l2 = [x]() { std::cout << ++x << std::endl; }; --> error
    // this will work, but id is only changed in the local scope!
    auto l3 = [x]() mutable { std::cout << ++x << std::endl; };
    l3();

    auto l4 = [](int x) { std::cout << x << std::endl; };
    l4(x);;
```

A lamda always has return type `auto`.

## Threads with Lambdas
Since lambdas are function objects, we can pass them to a thread like so:

```
auto l1 = [&x]() mutable { std::cout << ++x << std::endl; };
std::thread t4(l1);

t4.join();
```

## Threads with Variadic Templates & Member Functions

The thread constructor is a 'variadic' template, meaning we can pass it a function with all its arguments directly:

```
#include <iostream>
#include <thread>

void Test(int i, int& j) { std::cout << i << std::endl;} 

int main()
{
    int i = 1; 

    //Note: We use std::ref() to signal that the argument is a reference:
    std::thread t1(Test, i, std::ref(i));

    t1.join();

    return 0;
}

```
When we pass a function using a variadic template, the arguments are copied if they are lvalues and moved if they are rvalues (rvalue -> I have no name). We can use `std::move()` to force move semantics on lvalues if desired, but then the object content is lost to the parent thread.

Now, let's take a look at using member functions with threads:
```
#include <iostream>
#include <thread>

class Thread {
    private:
        int x_ = 0;
    public:
        Thread(int x) { x_ = x;}

        void operator()() {
            std::cout << "Thread object created" << std::endl;
        }
        void print(int p) {
            std::cout << "Member function printing: " << x_ + p << std::endl;
        }
};


int main()
{

    Thread T1(1);
    Thread T2(2);
    //By value
    std::thread t1{&Thread::print, T1, 1};

    //By reference
    std::thread t2{&Thread::print, &T2, 1};

    std::cout << "Finished work in main thread with id = " << std::this_thread::get_id() << std::endl;


    t1.join();
    t2.join();

    return 0;
}
```
We need to be careful that `T2` is not destructed before the thread finishes if we pass it by reference, else we access an invalid memory address. We can use a smart pointer to make sure that it is not deallocated to early:
```
std::shared_ptr<Thread> T3(new Thread(1));
std::thread t3{&Thread::print, T3, 1}
```

We can also easily create threads in a vector. The following example highlights a concurrency bug that is introduced if we pass `i` by reference instead of by value (credits: Udacity.com):
```
#include <iostream>
#include <thread>
#include <chrono>
#include <random>
#include <vector>

int main()
{
    // create threads
    std::vector<std::thread> threads;
    for (size_t i = 0; i < 10; ++i)
    {
        // create new thread from a Lambda
        //Note: if you write [&i] you get random memory access, because the execution of threads
        //is not in order, the for loop quits and i is not in scope anymore!
        threads.emplace_back([i]() {
            
            // wait for certain amount of time
            std::this_thread::sleep_for(std::chrono::milliseconds(10 * i));

            // perform work
            std::cout << "Hello from Worker thread #" << i << std::endl;
        });
    }

    // do something in main()
    std::cout << "Hello from Main thread" << std::endl;

    // call join on all thread objects using a range-based loop
    for (auto &t : threads)
        t.join();

    return 0;
}
```

That's it for the introduction :)

## References:
- Udacity C++ Nanodegree