+++
date = "2024-06-12"
title = "Building a digital financial analyst"
+++

In this post, we are going to explore how to create a digital financial analyst using the [Google Gemini LLM](https://gemini.google.com/app). The digital financial analyst should be able to quickly analyze company performance and financial data and provide summaries of the relevant insights it finds.

A summary might look like this:
```
> Financial Analyst: Last week, we see that sales underperformed vs. budget by 5.4% or 345k. The underperformance was mainly driven by week sales on Friday (-34%) and Saturday (-23%), offsetting the positive development see Monday to Wednesday (+17%).

The main reasons for the poor performance on Friday and Saturday are:
- Promo sales beverage category: 45% of total negative deviation
- Promo sales chips category: 19% of total negative deviation

Regular sales showed strong results the entire week, but could not offset the underperformance in promo on the weekend.
```

There are multiple options how we can go about doing that:

1. Calculate relevant statistics and convert them into text format that is easy for an LLM to understand and summarize (either as natural language or provided as json)
2. Use existing reports and leverage multimodal LLMs to analzyse screenshots of those reports
3. Create an LLM agent that can request company data and has tools that it can use to analyse the data

While option 1) and 2) are quick to implement, they offer some different pros and cons. Option 1 is probably best to avoid hallucinations as the LLM is only asked to summarise the provided information, which is an area where LLMs are strong in. However, all the data needs to be pre-calculated and provided in a format that is easy for the LLM to summarize. The LLM cannot dig deeper beyond what is provided. Option 2 is appealing, because many companies have lots of dashboards that are in principle at least useful to understand the company performance. However, since visual dashboards often do not contain all information that is necessary to interprete them this can potentially lead to very wrong assumptions by the LLM about what the meaning of the report it analyzes. Additionally, design might affect the output of the LLM. In both cases, the LLM is likely to make mistakes when it attempts to do calculations on company data.

Therefore, we are going to explore option 3: we will give our LLM tools to query company data and analyze it using Python functions. The LLM can decide based on the output of the functions if it wants to continue analyzing or not. In theory at least that should give us a lot of flexibility.

We will implement a prototype in Python using Google VertexAI with Gemini-Pro1.5.

## Gemini Function Calling
Google provides a very good overview how function calling is implemented with Gemini models:
![google-gemini-function-calling](/img/function-calling-gemini.png)

Basically, we need to define 'Tools' that Gemini can use. The tool we give Gemini is a collection of (Python) functions it can call. The functions are specified using the [OpenAPI JSON schema](https://spec.openapis.org/oas/v3.0.3#schemawr). Gemini will then pick functions to use based on the provided OpenAPI descriptions and will return the function call it wants to make as text. We can then execute this function call and pass the result back to Gemini.

So let's build a simplified analyst that is tasked to analzye everything about our CAT business. The following code closely follows Googles examples to build a chat bot to [analyse company stocks](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/function-calling/use_case_company_news_and_insights.ipynb):
```
#%%
%load_ext autoreload
%autoreload 2
#%%
import pathlib
import textwrap
import time
from dotenv import load_dotenv, find_dotenv

import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

load_dotenv(find_dotenv(usecwd=True), override=True, verbose=True)
#%%
vertexai.init(project="<your-project-id>", location="europe-north1")
#%%

get_cat_types = FunctionDeclaration(
    name="get_cat_types",
    description="Get all available cat types at a specific location: Black cat, white cat, red cat, etc",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "Cat types at given location"
            }
        }
    }
)

calculate_awesomeness_cat_types = FunctionDeclaration(
    name="calculate_awesomeness_cat_types",
    description="Calculate how awesome a given cat type is",
    parameters={
        "type": "object",
        "properties": {
            "cat_type": {
                "type": "string",
                "description": "Cat type to analyze and calcualte awesomeness index for"
            }
        }
    }
)

# create tool that allows Gemini to select from the defined functions
cat_insights_tool = Tool(
    function_declarations=[
        get_cat_types,
        calculate_awesomeness_cat_types,
    ]
)

# Define the Python functions and a handler
def get_cat_types_api(content):
    location = content["location"]

    cat_types = {
        "Cat Cafe Vilnius": "black, white, grey, red",
        "Cat Cafe Klaipeda": "black, white",
        "Cat Cafe Kaunas": "black, grey, red",
    }

    return cat_types[location]

def calculate_awesomeness_cat_types_api(content):
    cat_type = content["cat_type"]

    awesomeness_index = {
        "black": "super awesome, except on Friday 13th from the left",
        "white": "super duper awesome",
        "grey": "mega awesome",
        "red": "fiery awesome",
    }

    return awesomeness_index[cat_type]

function_handler = {
    "get_cat_types": get_cat_types_api,
    "calculate_awesomeness_cat_types": calculate_awesomeness_cat_types_api
}
##
model = GenerativeModel(
    model_name="gemini-1.5-pro-001", 
    generation_config=GenerationConfig(temperature=0), 
    tools=[cat_insights_tool]
    )

#%%
chat = model.start_chat()
#%%
def start_analysis(prompt):
    prompt += """
    Give a concise, high level sumamry. Only use information that you learn from the functions responses.
    """

    response = chat.send_message(prompt)

    function_calling_in_process = True
    time_out_after_n_calls = 10
    while function_calling_in_process and time_out_after_n_calls > 0:
        function_call = response.candidates[0].content.parts[0].function_call

        if function_call.name in function_handler.keys():
            function_call = response.candidates[0].content.parts[0].function_call

            function_name = function_call.name
            print("predicted function:")
            print(function_name, "\n")

            params = {key: value for key, value in function_call.args.items()}
            print("predicted function parameters")
            print(params, "\n")

            function_api_response = function_handler[function_name](params)[:20000] # stay within input token limit

            print("api response")
            print(function_api_response, "\n")

            time_out_after_n_calls = time_out_after_n_calls - 1

            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={"content": function_api_response}
                )
            )
        else:
            function_calling_in_process = False


    print(response.text)

#%%
start_analysis("analyse how many cat types we have in Cat Cafe Vilnius, Klaipeda and Kaunas and the awesomness of the cat types")
#%%
start_analysis("What is the awesomeness of grey and black cats?")
```

Note that we build in a rather crude safety that stops the model after 10 api calls. We need a smart way to determine if we want to keep analysing (and also investigate having a second Gemini model talk to the first one). 

## Follow-up Work 
It would be interesting to have two models talk to each other to simulate the interaction between business and BI departments. The business agent would ask a question, the BI agent would try to answer it and the business agent would ask a follow-up question. This would mimic the natural exploratory back and forth between those departments.
