+++
date = "2021-03-19"
title = "Pointers - Syntax Overview"
+++

This post is a short reminder to my future self summarising pointer syntax:


## Pointer Basics
```
#include <iostream>

int main() {
    int a = 5;
    int b = 15;

    int* p1 = &a;       //initialize int pointer p1 and assign address of a to pointer p1
    int* p2 = &b;       //initialize int pointer p2 and assign address of b to pointer p2

    *p1 = 10;           //dereference pointer and change variable a to 10
    std::cout << "a = " << a << " and b = " << b << std::endl;
    
    *p2 = *p1;          //dereference pointer p2 and set it to the content of p1 (b = 10)
    std::cout << "a = " << a << " and b = " << b << std::endl;

    p1 = p2;            //set the address of p1 to point to b (a = b = 10)
    std::cout << "a = " << a << " and b = " << b << std::endl;

    *p1 = 20;           //set b = 20
    std::cout << "a = " << a << " and b = " << b << std::endl;
}
```

And we get:
```
>>> a = 10 and b = 15
>>> a = 10 and b = 10
>>> a = 10 and b = 10
>>> a = 10 and b = 20
```

## Pointers with Objects

Pointers allow us to access class members and variables by first dereferencing the pointer to the class. You can either dereference manually (*p3) and then access members using dot-syntax or us the shorthand p3->x:
```
#include <iostream>

class TestClass {
    public:
        int x{1};
        int y{2};
};


int main() {

    TestClass test;
    TestClass* p3 = &test;

    std::cout << "TestClass.x = " << p3->x << " and TestClass.y = " << (*p3).y << std::endl;

}
```
and we get:
```
>>> TestClass.x = 1 and TestClass.y = 2
``` 

## Pointers with Arrays

Usually we create pointers to the first entry of an array, which works quite nicely as arrays occupy consecutive chunks of memory. But we can also initialize a pointer of array type:

```
#include <iostream>

int main() {

    int a[5] = {0,1,2,3,4};
    int b[6] = {5,6,7,8,9,10};
    int c = 11;

    int (*array)[5] = &a;                                   
    std::cout << (*array)[0] << std::endl;                  //dereference array pointer and access member of array

    // '=': cannot convert from 'int (*)[6]' to 'int (*)[5]'
    // array = &b; 

    //However, this all works:
    int* p = a;                                             //create pointer to first array element (arrays decay to pointer)
std::cout << *(p+0) << std::endl;                          
    p = b;
    std::cout << *(p+1) << std::endl;
    p = &c;
    std::cout << *(p) << std::endl;

}
```

Hope you find it useful future self :)