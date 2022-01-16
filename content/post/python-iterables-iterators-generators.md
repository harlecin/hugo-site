+++
date = "2022-01-16"
title = "Python Iterables, Iterators and Generators"
+++

Python is very popular for data processing and munging and has some powerful tools for data streaming/lazy evaluation that allow us to work with datasets that do not fit into memory.

In this post I want to talk about the tools that Python has build in to make stream processing possible, namely:

- Iterables,
- Iterators and
- Generators

Let's get started:

# The Iterator Pattern
The iterator pattern allows us to loop over data and only fetch items that we want to work on. This allows us as already mentioned to work with datasets that don't fit into memory.

One example of lazy evaluation is the `range()` function, although confusingly, it is not an iterator, but a range-class object.

Compare the output of the following two lines:
```
import sys

sys.getsizeof(range(10000))
sys.getsizeof(list(range(10000)))
```
    48
    90112

In the first case, we do not actually create a list of 10000 integers, so we need only 48 bytes to store everything, whereas in the second case we are actually allocating storage for 10000 ints which uses 90112 bytes of storage.

In Python, all collections are iterable, meaning we can loop over them. Whenever we loop over an object, the interpreter calls the `__iter__()` special method of the object (or `__getitem__()` if it is not available). If that is not possible, we get an error saying the object is not iterable.

Since a sequence in Python is just an ordered collection that implements `__getitem__()` (mostly for backwards compatibility, they also implement `__iter__` now), they are also iterable.

When building a custom iterable, you should stick to `__iter__`.

We get the following defintion:

> **Iterable**: An object implementing `__iter__` returning an iterator. Iterators are obtained from iterables.

We can also see that nicely here:
```
l = [1, 2] # iterable, NOT an iterator
it = iter(l) # build an iterator from an iterable by calling __iter__()
next(it) # iterate over the iterator
```
This is equivalent to:
```
it2 = l.__iter__() # build iterator
it2.__next__() # iterate over iterator by calling next
it2.__iter__() # returns self so it2 can be used as iterable since it returns an iterator, i.e. itself
```

So we have:
```
Iterable                    ----->  Iterator
    __iter__()->Iterator    builds       __iter__()->self (=Iterator)
                                         __next__()
```
Meaning that an iterable should return a new iterator instance. A concrete iterator implements next and iter (which only returns self).
This is necessary to allow an iterator to work with a for-loop, which expects an iterable (see [here](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)). Note that if you use an iterator in stead of an iterable in a for loop, it will only return results once. Then the iterator is empty, while an iterable would produce a new iterator so the for loop can start again. 

We get the following definition:

> **Iterator**: Any object implementing __next__() to return the next item or raise StopIteration. Iterators also implement __iter__() returning self, making them iterable, but not restartable (as they are not producing a new iterator)

Now let's put everything together:

```
from typing import List, Iterator

class ExampleIterable:
    def __init__(self, i: List[int]) -> None:
        self.i = i
    
    def __iter__(self) -> Iterator:
        return ExampleIterator(self.i)

class ExampleIterator:
    def __init__(self, j: List[int]) -> None:
        self.j = j
        self.index = 0
    
    def __next__(self) -> int:
        try:
            integer = self.j[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return integer
    
    def __iter__(self) -> 'ExampleIterator':
        return self

test = ExampleIterable([1,2,3])

for integer in test:
    print(integer)
```
# Generators
The implementation of the Iterator is quite verbose and thankfully there is an easier way to do it. We can simply replace the Iterator class by a generator expression:
```
from typing import List, Generator

class ExampleIterable2:
    def __init__(self, i: List[int]) -> None:
        self.i = i
    
    def __iter__(self) -> Generator:
        for integer in self.i:
            yield integer

test = ExampleIterable2([1,2,3])

for integer in test:
    print(integer)
```
In Python changing a `return` to a `yield` changes a normal function to a generator function, which returns a generator object when called.

> **Generators**: A generator is an iterator that produces values passed to yield

As we showed in the beginning when we compared `list` with `range`, only producing values that we need saves a lot of memory. We can use this fact in our example by passing a generator to `iter` thereby producing values on demand:

```
from typing import List, Generator

class ExampleIterable3:
    def __init__(self, i: range) -> None:
        self.i = i
    
    def __iter__(self) -> Generator:
        for integer in self.example_generator(self.i):
            yield integer

    def example_generator(self, r: range):
        for i in r:
            yield i

test = ExampleIterable3(range(3))

for integer in test:
    print(integer)
```

Here we have a generator inside a generator :)

We can also create a generator using a generator expression like so:
```
(for i in range(r))
```

# References
The content of this post is based on the excellent book 'Fluent Python'  by Luciano Ramalho.
