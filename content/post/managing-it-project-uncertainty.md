+++
date = "2024-07-23"
title = "Managing Complex <IT/AI/insert domain> Projects"
+++

Complex projects are usually painful to manage, because they involve many stakeholders, a lot of uncertainty and budget and/or time constraints. In this blog post I want to summarize a few recipes that I found very handy for working with complex projects. Before, we begin, we need to define what we actually mean when we say "complex project". How is a complex project different from a normal project?

The Cambridge Dictionary defines ["complexity"](https://dictionary.cambridge.org/dictionary/english/complexity) as:

> "complexity, noun: the state of having many parts and being difficult to understand or find an answer to"

So to make a complex project less complex, we have to do two things:

1. Reduce the number or parts or tackle them separately, so each part is a simple project: Divide and conquer
2. Reduce the complexity of each part and how they relate to each other: Keep it stupid simple

So let's take a look at those two strategies :)

## Divide and conquer
The "divide and conquer" strategy is all about breaking the project apart into small manageable junks. In principle, there are lots of different ways to do that, but some are more suitable to quick development than others. 

Let's say we want to build a pyramide of a given size. We can do it in the following two ways:
![pyramide-building](/img/pyramide-building.png)

I used different colors to show how the pyramides are built.

While both ways give us the same pyramide in the end, the first way of building the pyramide gives us a fully-working pyramide after each iteration while the second way of working is only really accomplishing our goal of building a pyramide at the very end if all building steps are completed. Very often, either budget or time run out more quickly than anticipated and we need to make some compromises. By using a divide-and-conquer strategy that gives us usable sub-products, we are more flexible to change direction and still have a working product. We can also start collecting feedback from end-users much more quickly, which can help us improve our work going further.

Quantity/rapid iteration very often leads to quality, because mistakes can be made more quickly and are easier to recover from which allows us to learn faster. [If something is difficult, do it more often](https://www.amazon.com/dp/0961454733/?tag=codihorr-20) (this is a strategy that we will come back to in the next part)

To understand how to divide a project so that we can incrementally improve the product, it is very important to understand from an end-user perspective, what is necessary for parts to be individually usable. Very often, end-users cannot clearly pin-point the problem or maybe do not even fully realize that there is a problem. 

There are a lot of books, blog posts and courses on how to do requirements engineering properly. Personally, I believe that the key to successful requirements engineering is getting a deep understanding of the actual problem (note: not necessarily the problem users tell you). From an organizational perspective that means that ideally we embed developers in business teams. Since lots of large corporations don't follow that model, an alternative is to do job shadowing and encourage lateral transfers between business and IT. Very often shadowing is not possible short term and there are no lateral transfers who have a deep understanding of all necessary domains. In that case, we need to:

## Keep it simple stupid
Clear communication & transparency about deliverables are key for managing a project. While that sounds super obvious, I see lots of projects were "clear communication" is interpreted as "putting the entire company on CC in emails" and transparency about deliverables means "putting together a PowerPoint deck with a Gantt chart".

From my personal experience to have clear communication and transparency about deliverables we need to:
- have a single source of truth where we document all requirements, comments and decisions and
- small deliverables

While I personally prefer a tool like Jira for managing requirements, comments and tasks you can also do that just fine using Word. The key point is that there needs to be clear and transparent way to track how decisions were made and when deliverables are due.

This brings me to the last part: small deliverables. My rule of thumb is that if you cannot deliver something in a week, you need to make the deliverable smaller. This forces people to think clearly about requirements and gives transparency into project status.

It also allows us to see more quickly if what we think other people need and what they actually need are the same.

Personally, I have a rule that if you cannot provide a visual or a mock-up, there is a very high likelihood that you will be misunderstood. This is why I (very strongly) encourage my project managers to always bring visuals and mock-ups to discussions. Powerpoint and Excel are incredible tools to do mockups especially for non-engineers. I usually recommend to start from visual-only mockups and then built Excel mockups as a next step. (There is a reason Excel is still the #1 productivity tool - it is simply a swiss army knife to solve business problems). 

Providing mock-ups also forces us to make our implicit assumptions transparent.

Seeing is understanding:
![mockup](/img/mock-up.png)

## The Power of Templates
Last but not least: There is a very high likelihood that someone already encountered a similar problem before. If possible, always use existing work as a template and then modify the template if necessary.

Understanding how to find and apply existing templates to your given problem is perhaps the best way to manage complex projects, because it allows you to leverage all the lessons-learned someone else had to discover the hard way. Templates reduce complexity by reducing the amount of parts that you need to manage and by reducing the scope of work. 

I would actually go so far as to say: if possible, adapt to the template and don't adapt the template to your project. Very often, (especially large) companies believe that their processes/problems/what-not are incredibly unique and they need a custom solution to handle those processes. I would argue that if the process/problem you are tackling is not a core competitive advantage of yours (say incident management in IT or payroll processes) stick to standard tools and templates that are readily available. Not only does it help with project implementation, but future maintainence is easier and on-boarding new hires as well.

Hope you found some of the content useful and not too generic :)

