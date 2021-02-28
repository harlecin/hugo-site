+++
date = "2021-02-28"
title = "From Basic to Advanced OOP in C++"
+++

C++ is also commonly called C with classes and in this post I want to give you an overview about basic and advanced oop concepts in c++.

Let's start from the very beginning with `structures`:

## Structures
Structs allow you to define your own custom types to complement the build-in types (also called 'primitives' or fundamental types) like `int`, `float`, `string` and so forth. For example we could implement the following type:
```
struct Date {
    // You can provide defaults in {}
    int day{1};
    int month{1};
    int year{1970};
};

Date date;
date.day = 1;
date.month = 1;
date.year = 2020;
```

We can also restrict access and validate inputs like so:
```
struct Date {
    // You can provide defaults in {}
    // You can use private and public to restrict access
    // We used const to protect member data in getters
    public:
        int Day() const { return day; }
        int Month() const { return month; }
        int Year() const { return year; }

        void Day(int d) { 
            if(d > 0 && d <= 31) {day = d;}
        }
    private:
        int day{1};
        int month{1};
        int year{1970};
};

Date date;
date.Day(1);
date.Month(1);
date.Year(2020);
```
Private attributes can only be accessed and changed by methods from within the struct. If we set members as private, we need methods to access and change them, called 'getters' and 'setters'.

As you can see, the code became quite a bit longer and harder to read, so if possible keep attributes public and avoid getters and setters.

To validate data we defined 'invariants'. Invariants restrict the range of attributes, so it is basically a rule that defines which values are allowed.

## Classes

You could also implement your custom type as a class. All you have to do is switch the `struct` keyword with the `class` keyword. The key difference is that structs use public access by default and classes private access. You can find a detailed discussion of when to use classes vs. structs in [this stackoverflow post](https://stackoverflow.com/questions/54585/when-should-you-use-a-class-vs-a-struct-in-c#54596)

## Constructors

Constructors initalize objects. All classes come with a default constructor that takes no arguments, but we can also implement our own. 

Including a constructor is easy, just include a method with the same name as the class:
```
class Date {
    public:
        // We used an initalizer list for year and set day and month afterwards:
        Date(int d, int m, int y): year(y) {
            day = d;
            month = m;
        }
    private:
        int day;
        int month;
        int year;
};

```
The benefit of using initalizer lists is that initialization sets the value as soon as the object exits in contrast to assigment which sets the value after the object is created (see [c++ core guidelines](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c49-prefer-initialization-to-assignment-in-constructors)). Member variables can be set to `const` if you use an initializer list!

The syntax for initializer lists is simple: Pass the argument to the constructor to the variable you want to assign to in ():
```
class Test {
    public:
        Constructor(int v): var(v) {}

    private:
        int var;
};
```
Also note that attributes defined as references have to use initialization lists!

In order to keep our class definition lean, we can separate the code for class declaration (header file) and class definition (cpp file):
```
// date.h
class Date {
    public:
        int Day();
        int Month();
        int Year();
    private:
        int day{1};
        int month{1};
        int year{1};
};

// date.cpp
include "date.h"

int Date::Day() { return day; }
int Date::Month() { return month; }
int Date::Year() { return year; }
```

## Inheritance and Composition

Inheritance in c++ is easily accomplished likes so:
```
class Base {
    public:
        int a;
    protected:
        int b;
    private:
        int c; 
};

class PublicDerived : public Base {
    // a is public
    // b is protected
    // c is not accessible from Derived
};

class ProtectedDerived : protected Base {
    // a is protected
    // b is protected
    // c is not accessible from Derived
};

class PrivateDerived : private Base {
    // a is private
    // b is private
    // c is not accessible from Derived
};
```

If you use no access specifier keyword the default inheritance is private.
For more info on when to use `protected` checkout the docs [here](https://docs.microsoft.com/en-us/cpp/cpp/protected-cpp?view=msvc-160).

Multiple inheritance has the following syntax:
```
class Derived : public BaseA, public BaseB {
    ...
};
```

An alternative to inheritance is to use composition:
```
class A {};

class B {
    A()
};
```

## Function and Operator Overloading

Operator overloading works just like regular function overloading, but you have to write `operator` before the operator you want to overload. For example, if you have a Matrix class you could overload the `+, -, <>` operators to work with matrices.

The syntax looks the following:

```
PointXY operator+(const PointXY& addend) {
  //...logic to add Points
}
```

## Virtual functions

We can use virtual functions to create an abstract base class like so:

```
#include <iostream>

class Vehicle {
    virtual void Drive() const = 0;
};

class Car : Vehicle {
    void Drive() override {
        std::cout << "brumbrum\n";
    }
};
```
Virtual functions can be used to declare an interface. By having `=0` behind the virtual function, we declare it as a 'pure' virtual function. A pure virtual function is only declared, but not defined. Pure functions make a class abstract, i.e. it cannot be instantiated. You can also omit the `=0` and provide an implementation for the virtual function.

If our function `Drive()` is not declared as `virtual` the implementation in the derived class would hide the base class function.

We put the `override` keyword in our derived class to signal to the compiler that we want to overwrite the base class virtual function. You don't have to use `override` but it can help catch errors.

## Generic Programming

One very cool feature in c++ are Templates. A template allows us to generalize a function to work with many classes without having to implement each individual function like we had to with overloading.

It works as follows:

```
template <typename T>
T Min(T a, T b) {
    return a < b ? a : b;
}

int main () {
    Min<int>(1,2)
    Min<float>(1.0, 2.0)
}
```
Now we have a function `Min()` that works with any class that has a valid implementation of `<`. So this is probably the main draw back of templates: templates only work if the classes you use them with implement the necessary operations required by the template. In c++ 20 a new feature called 'concepts' will expand on templates to also specify what operations a class has to implement in order for the template to work.

## Deduction
We can also use template deduction to use templates to have the compiler figure out how to work with our template:

```
Min(1,2)
Min(1.0, 2.0)

// Also works vectors if we use g++ -std=c++17 to compile the code:
vector v{1,2,4}
```

## Class Templates
We can also use templates with classes like so:
```
#include<string>
#include<iostream>

template <typename A, typename B>

class TemplateClass {
    public:
        TemplateClass(A a, B b): a_(a), b_(b) {}
        A a_;
        B b_;
};

int main() {
    TemplateClass<std::string, int> test("a", 1);
    std::cout << test.a_ << "\n";
    std::cout << test.b_ << "\n";
}
```
The class above works with any class we pass in.

