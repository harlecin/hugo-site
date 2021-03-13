+++
date = "2021-03-13"
title = "Stackoverflow, Segfault & Co: Memory Allocation in C++"
+++

In this post we will take a look at how memory management works and we will create our very own stackoverflow :)

But let's start from the beginning:

Each program that runs on a computer is assigned its own virtual memory by the os. The addresses are arranged consecutively and the memory is divided into areas:

```
high address
 | os kernel space       (user code cannot read/write here)
 | stack                 (managed, variables in local scope)
 | heap                  (dynamically allocated variables)
 | BSS                   (unintialized static variables)
 | Data                  (explicitly initialized static variables)
 | Text                  (program code)
low address
```

Let's look into the invidiual blocks in more detail:

1. **Stack**: Continous memory block of fixed size. If your program exceeds the size of the stack, it crashes. Variables and function parameters are automatially allocated on the stack. Each thread of a program is assigned its own stack by the os. When the program leaves a specific scope all variables that are not in scope anymore are automatically freed by the compiler
2. **Heap**: Also called "free store" in cpp. Memory allocated on the heap has to be managed by the programmer. The heap is shared by all threads of a program.
3. **BSS**: Block Started by Symbol segment contains global and static variables that are not initialized (such as uninitialized arrays).
4. **Data**: Same as BSS, but variables are initialized with values other than zero. Is allocated once and has scope until the program ends.

## Stack Memory

So now we will take a closer look at the stack. Consider the following c++ program:

```
int foo(int a) 
{
    int s = 0;          -> 3) s=0 : This is the top of the stack
    s = a + s;

    return s;
}

int main()              -> 0) main() is the first item on the stack
{
    int x = 0;          -> 1) pushed to the stack: x = 0
    x = foo(42);        -> 2) a = 42 -> return address, base pointer

    return 0;
}
```
When we run the program the stack gets allocated and deallocated according to last-in-first-out.

So stack size looks basically like this:
```
start ---------------------------------> end
main()  main()  main()  main()  main()  <empty>
        x=0     x=0     x=0     x=42
                a=42    a=42    
                foo()   foo()
                        s=42
```

Now as promised, we are ready to create our very own stackoverflow :)

We will recursively call a function until our stack is full:
```
#include <stdio.h>

void foo(int i, int& j) {
    int k = i+1;
    printf ("%i: stack bottom : % p, current stack address : %p \n",i,&j, &k);
    foo(k, j);
}


int main() {
    int i = 1;
    foo(i, i);
    return 0;
}
```
Which on the machine I compiled it gives:
```
...
...
174656: stack bottom :  0x7ffdec5ec394, current stack address : 0x7ffdebded7a4 
174657: stack bottom :  0x7ffdec5ec394, current stack address : 0x7ffdebded774 
174658: stack bottom :  0x7ffdec5ec394, current stack address : 0x7ffdebded744 
Segmentation fault (core dumped)
```
The difference between `stack bottom` and `current stack` tells you how much space you allocated on the stack.

In this case we get: 0x7ffdec5ec394 - 0x7ffdebded744 = 8.383.568 byte or about 8 MB of stack space (since 1 hex = 1 byte)

## References:
- Udacity C++ Nanodegree