+++
date = "2021-03-12"
title = "Intro Memory Management in C++"
+++


Most people's dislike of c++ probably comes from the fact that when you write in cpp, you have to manage memory yourself. While this can be frustrating at times (hello there, `segfault` and `bad_alloc`:) it is actually immensely powerful and interesting.

So let's get right to it:)

## Memory Addresses and Hexadecimal Numbers

Computers store information in bytes which are themselves comprised of 8 bits. A bit can either be 0 or 1 which gives rise to the base 2 or binary system used a lot with computers. So far so trivial :) While this system might seem obvious in hindsight, in the beginning engineers tried to use the classic base 10, also called decimal system. However, as it turned out, representing 10 individual symbols is quite difficult in the presence of noise so John Atansasoff proposed the base 2, or binary system. This system turned out to be more robust and became the standard in the computing world (Source: [udacity/cpp-nanodegree](https://classroom.udacity.com/nanodegrees/nd213/parts/789a1625-9b09-4615-9210-ddbc12e9247b/modules/5d2b96c2-52eb-4264-b387-da31d90b1e1f/lessons/ec63b3b7-590d-43ef-9492-66f6f23d9988/concepts/e6830afc-c398-4af8-9221-f2675293f46f))

All computer information is stored in binary form. One of the earliest mappings or encoding schemes for characters is called ASCII (American Standard Code for Information Interchange). 

The ASCII table represents each charachter as an 8 bit number:
![ascii-table](/img/ascii-table-black.png)


Thankfully, nowadays most programs work with UTF-8 encoding, which allows a much richer set of characters to be represented.

In the table you can also see a column called 'Hex'. This column contains the hexadecimal representation of a given character, i.e. wrt. base 16.

Why do we need yet another number system?

1. Better readability than binary
2. Information density (you can store any number from 0 to 255 since 16^2 = 256)
3. Since 1 byte is equal to 8 bits (2^8=256), it is natural to represent a byte with a hex number.

## Analysing Memory with a Debugger

Now we take a look at how the following program stores variables in memory:

```
//file test.cpp with executable test
1 #include <stdio.h>
2 
3 int main()
4 {
5   char str[] = "Hello world c++!";
6
7   printf("%s", str);
8 }
```

First, let's attach `gdb`, add a breakpoint and run:
```
gdb ./test
(gdb) break 7
(gdb) r
```
Now let's print our vector and it's memory address:
```
(gdb) p str
$1 = "Hello world c++!"
(gdb) p &str
$2 = (char (*)[17]) 0x7fffffffd9200
```
The vector is allocated at memory position `0x7fffffffd9200`. The leading `0x` signifies that the following number is in hexadecimal. If you are interested in why the postfix `0x` was chosen, take a look at this [stackoverflow](https://stackoverflow.com/questions/2670639/why-are-hexadecimal-numbers-prefixed-with-0x) post.

If you want to take a look at this specific memory address, you can do so like so:
```
//x ... print memory, 5 ... number of units, x ... in hex, b ... unit Byte
(gdb) x/5xb 0x7fffffffd920
0x7fffffffd920: 0x48    0x65    0x6c    0x6c    0x6f
```

Now if we go back to the ascii table we will see that this is the hex representation of "Hello".

To take a look at the next byte, we can simply increment our hex number by one:
```
(gdb) x/5xb 0x7fffffffd920+1
0x7fffffffd921: 0x65    0x6c    0x6c    0x6f    0x20
```
Giving us "ello ": So we moved one Byte by incrementing the hex-address: This is basically all there is to pointer arithmetic:)

In general, you can get the size of a data type in c++ by using:
```
sizeof(T)
```
So for example `sizeof(int)` gives us 4 bytes. If you plot the addresses of an int array, you will see that the addresses increment by 4 between each individual number.

On 32-bit computers, each address is 32-bit long and points to one byte of physical memory. Since 2^32 ~ 4.294.967.296 this gives us a total addressable memory of 4GB for those systems.

Since different systems have different amounts of physical memory, we have virtual memory so that maps the address space to actual physical space. If a program requests more memory than is available in ram, the os can swap data to the hard disc.

![address-space](/img/address-space.png)
Image source udacity.com:

Before we finish, let's briefly discuss tow more important terms that often come up when we talk about memory management:

1: **Memory page**: A memory page is number of directly successive memory locations in virtual memory. All memory is divided into equally sized memory pages. The os uses memory pages to perform virtual memory management. Each memory pageis interpreted as a logical address and mapped to a physcial address if necessary.
2. **Memory frame**: A memory frame is the same as a memory page, but it actually lies in physical not virtual memory.

That's about as far as the basics are concerned :)
