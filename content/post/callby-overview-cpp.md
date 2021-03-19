+++
date = "2021-03-19"
title = "CallBy: Pointer/Reference/Const Reference"
+++

By default c++ uses call-by-value, but copying large arguments can be expensive so we can also use call by:

1. pointer
2. reference
3. const reference 

Since as a user we do not see if a function that takes an argument actually modifies it, we can use `const references` to have the compiler guarantee that an argument that is passed is not modified.

The syntax looks as follows: Note that changing a const reference gives a compile error.

```
#include <iostream>
    
void CallByPointer(int *i)
{
    *i = *i + 1;
}

void CallByReference(int &i)
{
    i = i + 1;
}

void CallByReferenceConst(int const &i) {
    //error C3892: 'i': you cannot assign to a variable that is const
    i = i + 1;
}

int main()
{
    int i = 0;
    
    CallByPointer(&i);
    std::cout << i << std::endl; //i = 1

    CallByReference(i);
    std::cout << i << std::endl; //i = 2

    CallByReferenceConst(i);
    std::cout << i << std::endl; //error: see function definition

    return 0;
}
```