import panel as pn  # GUI
pn.extension()

import openai

openai.api_key=""
panels = [] # collect display 
questions=[  "Education qualification",
            "Years of experience",
            "primary skills",
            "Expected salary",
            "preferred job location"]

  
context = [ {'role':'system', 
             'content':"""
               I want you to act as an recruitment agent, named Tom, 
               for an recruitment agency.
               You are asking candidates list of questions, to know candidate job requirement for further process
               Ask questions at a time and ask question from the given list of questions. 
               If candidate say yes ask further questions otherwise say goodbye
               questions:{questions}.
                    
"""} ]  

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


response = get_completion_from_messages(context)

print(response)
