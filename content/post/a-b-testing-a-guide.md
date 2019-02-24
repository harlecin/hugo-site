+++
date = "2019-02-09"
title = "Practical Guide to A/B Testing"
+++

<example: drug development>

## Pre-Experiment Phase
- get to know your customers - talk to them, validate later> 
- find out which questions to ask! do not test stuff that does not generate value!

Source: Google Udacity:
A/B testing cannot show you if you are missing something! -> Google
E.g. Premium Service: A/B test useful, but do not rely on it exclusively
stuff that happens rarely is hard to test

- unit of diversion: who do you assign to a or b? 
user_id, anonymous id (cookie), event (eg for ranking algorithms etc), device_id, ip_address

- unit of analysis vs unit of diversion: when they are the same (e.g. both are based on events) variability tends to be lower

cohorts vs populations:
- experiment and control cohort

duration vs exposure:
how long is the experiment running and who participates in the experiment? (e.g. weekend vs weekdays)

learning effects
- time to adapt to change for users: user_id/cookie + cohort
https://classroom.udacity.com/courses/ud257/lessons/4001558669/concepts/39700990310923

- checking invariants

## Experiment Phase
- attention: p-value hacking, problem with not-fixed sample size, ...

## Post-Experiment Phase
- record outcomes