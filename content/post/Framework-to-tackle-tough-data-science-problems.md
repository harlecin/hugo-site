+++
date = "2018-05-20"
title = "A Framework to tackle tough Data Science Problems"
+++

One of the things I particularly like about working in data science, is the science part: Figuring out the right questions to ask, how to frame a problem correctly and finally trying to solve it.

While there are many problems that you can simply solve by `library(caret)` or `from sklearn import *` and dumping your data into an appropriate algorithm those are usually just low-hanging fruits and often not particularly interesting to work on either.

In this post, I want to show you the framework I developed (more correctly: which I am still developing) to help me solve interesting data science problems.

## Understanding the problem

This sounds like a no-brainer, but I fear it is still often underappreciated just how important it is. Imagine for example you get the following request from a business unit at your company:

> We need an accurate prediction of sales volume for sales territory XY.

Some pretty standard follow-up questions that immediately come to mind are:

- We have to define how we measure 'accurary'. Should we use RMSE, MAE, MAPE or some custom metric?
- Do you want your forecast with daily data or are weekly/monthly totals sufficient?
- How much historic data do we have?

While those questions are all relevant they do not really help you in getting a better understanding for the problem in question, because they miss the most important point:

> What is the goal of this analysis, i.e. what do you want to do with the information?

I like to divide the questions I ask into 3 categories:

1. Business questions,
2. data science questions and
3. deployment questions.

Business questions help you understand the "why". Why are we doing the analysis? How are our results going to be used?

At a minimum, I like to ask the following questions:

- What is the goal of the analysis?
- How much time do we have to work on the problem?
- When is a solution good enough?

Without a clear understanding of the goal of your analysis you cannot suggest alternative solution strategies and you cannot check whether your loss function and your accuracy measure are appropriate. 

Imagine that the goal of doing the sales volume forecast is to plan the number of delivery trucks. Each truck has a capacity of 500 goods and you need a minimum of one truck anyway. So as long as your model helps to accurately determine when you need an additional truck or when you can make do without, it is doing its job even if the forecast is off by say 50 goods on average. 

This directly ties in with the question: "When is a solution good enough?". As a rule of thumb, if you cannot act on the additional accuracy your forecast provides, it is probably advisable to stick to a simpler solution. If you only need to forecasts on a monthly level, forecasting on a daily level to produce monthly forecasts is likely going to introduce additional complexity that will likely not substantially change your results, but makes it harder to find a solution quickly.

I then go on to ask 'classic' data science questions that I already stated in the beginning:

- How do we measure accuracy?
- What loss function do we use, i.e. what is the metric we optimize?
- What is the desired level of granularity across all relevant dimensions? (e.g. daily vs. monthly, item level vs. category level, address level vs. zip code level)
- What kind of data is available?
- How much historic information do we have?
- Has someone already tried to answer this or a similar question in the past?

As I already mentioned, we need a thorough understanding of the problem in order come up with an appropriate measure of accuracy and a loss function that is suitable for our problem.

The last question is particularly important for a couple of reasons:

1. If someone tried to solve this or a similar problem in the past we can use this solution as a benchmark.
2. Furthermore, we can incorporate the previous solution into our own framework and potentially avoid re-inventing the wheel.
3. We can learn from errors that were made in the past and hopefully avoid falling into similar traps.
4. Finally, we can use the previous solution to get a feeling for the difficulty of the problem, which is important when we need to estimate how much budget we are likely going to need.

Finally, I go on to discuss deployment questions:

- Is this an ad hoc analysis that is only done once or should it be automated in the future?
- How often do you need an updated forecast?
- When do you need an updated forecast?

Depending on whether this is a one-off or a repeated analysis, we can invest less or more time in building re-usable parts and writing unit tests and so forth.

Forgetting to ask the last question actually nearly tripped me up once. I had to provide a day-ahead forecast every day by around 3 o'clock in the afternoon. Trouble was that the data for my most relevant features was not yet available in the database by that time. So I had to make do with data from the day before.

## Structuring your analysis

Before I dive into the analysis I like to draw up a structure. Doing that helps in two ways:

1. It helps my team and myself to work in a systematic way that allows us to track work items and divide work efficiently.
2. It helps communicate our progress to our clients.


Usually we 
- take a look at the available data
- ask for infos on where to start
- come up with some hypothesis
- MECE
## Getting to know your data
### Signal/Noise ratio

## Starting really simple - Minimum Viable Forecast (MVF)
### Working with an easy sample
### A quick and dirty baseline

## Framing the problem in different ways

## Checking plausibility & feasibility of solution

## Deploying your solution

<Communicating with clients: 
presenting conclusions without showing your work
scatter brained
no visual explanation
correct, but not practical
how to present your results
>