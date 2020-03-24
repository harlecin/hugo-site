+++
date = "2020-03-24"
title = "Operations Research 101 with Python"
+++


Recently my sister asked me to help her with some linear programming problems in Excel. I have not used Excel solver for what feels like decades and I was pleasantly surprised how easy it was to setup and solve a linear programming problem with it. But since I am not really an Excel fan, I wanted to check how fast I could solve a linear programming problem with Python. I decided to use Google's [OR Tools Package](https://developers.google.com/optimization), because a former colleague of mine who has quite a lot of experience in OR likes it a lot. So let's get going:

## Problem

A firm wants to supply 550,000 liters of gasonline and has to decide on the optimum number of trucks given a fixed budget of EUR 600,000. There are three trucks available with the following stats:

| Model   | Capacity (l) | Purchase Price (EUR) | Monthly OPEX (EUR) | # Trips/Month |  # Trucks |
|---------|--------------|----------------------|--------------------|---------------|-----------|
|  Super  | 5,000        | 67,000               | 550                | 15            | S         |
| Regular | 2,500        | 55,000               | 425                | 20            | R         |
| Eco     | 1,000        | 45,000               | 350                | 25            | E         |

The company does not want to purchase more than 15 trucks total, at least 3 of the Eco ones and no more than 7 of the Super trucks. The company wants to minimize monthly operating costs, so how many trucks of each type should it purchase?


Let's get started with OR-Tools:)


```python
from __future__ import print_function
from ortools.linear_solver import pywraplp
```

---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
<ipython-input-2-7b3da395caf7> in <module>
      1 from __future__ import print_function
----> 2 from ortools.linear_solver import pywraplp
      3 
      4 

~\Miniconda3\lib\site-packages\ortools\linear_solver\pywraplp.py in <module>
     11 # Import the low-level C/C++ module
     12 if __package__ or "." in __name__:
---> 13     from . import _pywraplp
     14 else:
     15     import _pywraplp

ImportError: DLL load failed: The specified module could not be found.

Ok, I have to admit getting an error this fast was kind of unexpected:) Thankfully, installing Microsoft Visual C++ Redistributable für Visual Studio 2019 from [here](https://aka.ms/vs/16/release/VC_redist.x64.exe) solved the issue for me. So, let's move on to the actual exercise:


```python
solver = pywraplp.Solver('TruckProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    
S = solver.IntVar(0.0, 15, 'S')
R = solver.IntVar(0.0, 15, 'R')
E = solver.IntVar(0.0, 15, 'E')
```


```python
print('Number of variables:', solver.NumVariables())
```

    Number of variables: 3
    


```python
# Budget constraint
solver.Add(67000*S + 55000*R + 45000*E <= 600000)

# Capacity contraint
solver.Add(5000*15*S + 2500*20*R + 1000*25*E >= 550000)

# Truck constraints
solver.Add(S+R+E <= 15)
solver.Add(E >= 3)
solver.Add(S <= 7)
```




    <ortools.linear_solver.pywraplp.Constraint; proxy of <Swig Object of type 'operations_research::MPConstraint *' at 0x000002311F302F90> >




```python
solver.Minimize(550*S + 425*R + 350*E)

status = solver.Solve()
```


```python
if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Minimum Monthly OPEX =', solver.Objective().Value())
        print('S =', S.solution_value())
        print('R =', R.solution_value())
        print('E =', E.solution_value())
else:
        print('The problem does not have an optimal solution.')
```

    Solution:
    Minimum Monthly OPEX = 4650.0
    S = 5.0
    R = 2.0
    E = 3.0
    

Finally:) Apart from the initial problem with setting up or-tools, working with it is super intuitive and Google's examples which I used to setup this toy problem make it very easy to get started. While I liked Excel's intuitive user interface, it is quite easy to make an error somewhere in a cell formula that goes unnoticed, so personally I prefer working with or-tools, even for simple problems like this one.

Hope this post was somewhat helpful or at least helped pass some time during the Corona lock-down. #staysafe #stayhome:)
