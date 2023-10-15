import openai
import time
import numpy as np
from data_filter import data_filter

def find_result(text):
    if "Result: True" in text:
        return 0
    elif "Result: False" in text:
        return 1
    else:
        return 2

def generate_context(number):
    background = ("I will give you a data sample, which is a time-series data sample. " 
                  "This data sample ranges from 0 to 10. "
                  "Your mission is to tell me whether this sample belongs to a class with the help of following 2 questions.\n")
    definition2 = ("'nA' means 0 or 1.\n" 
                    "'nB' means 9 or 10.\n"
                    "When there's a 'nA' in the array, there should be a 'nB' after 'nA'.\n "
                    "When there's a 'nB' in the array, there should be a 'nA' after 'nB'.\n"
                    )

    definition3 = ("'nA' means 0 or 1.\n" 
                    "'nB' means 9 or 10.\n"
                    "'Situation 1' : When the index of 'nA' is smaller than the index of 'nB'.\n "
                    "'Situation 2' : When the index of 'nA' is bigger than the index of 'nB'.\n"
                    )
    question = ("Question1: Is there a 'Situation 1'?\n" 
                "Question2: Is there a 'Situation 2'?\n")
    
    stepA2 = ("You should think Question 1 step by step.\n"
            "Step1: Find a 'nA' first.\n"
            "Step2: Find if there's a 'nB' after 'nA'.\n"
            "Step3: Check whether the index of 'nB' is greater than the index of 'nA'.\n")
    
    stepB2 = ("You should think Question 2 step by step.\n"
            "Step1: Find a 'nB' first.\n"
            "Step2: Find if there's a 'nA' after 'nB'.\n"
            "Step3: Check whether the index of 'nA' is greater than the index of 'nB'.\n")


    stepA3 = ("You should think Question 1 step by step.\n"
            "Step1: List the array with index.\n"
            "Step2: Find 'nA' and 'nB'.\n"
            "Step3: Check whether the index of 'nA' is smaller than the index of 'nB'.\n"
            )
    stepB3 = ("You should think Question 2 step by step.\n"
            "Step1: List the array with index.\n"
            "Step2: Find 'nA' and 'nB'.\n"
            "Step3: Check whether the index of 'nA' is bigger than the index of 'nB'.\n"
            )
    
    class_pattern_2 = "This class must satisfy both 'Situation 1' and 'Situation 2'.\n"
    def class_pattern(number):
        common = "This class should satisfy 2 conditions:\n"
        true1 = "There's a 'Situation 1'.\n"
        true2 = "There's a 'Situation 2'.\n"
        false1 = "There's no 'Situation 1'.\n"
        false2 = "There's no 'Situation 2'.\n"
        if number == 2:
            return common + "1. " + true1 + "2. " + true2
        elif number == 3:
            return common + "1. " + true1 + "2. " + false2
        elif number == 4:
            return common + "1. " + true2 + "2." + false1

    rule = ("Now I will give you one array. You should help me to classify whether this array belongs to this class. " 
            "Don't show me the code or curve graph.\n"
            "You should answer at the very end. The format should be: 'Result: True' or 'Result: False'.\n")
    return background + definition2 + question + stepA2 + stepB2 + class_pattern(number) + rule
    
def generate_query(number):
    array = data_filter.average(2)
    query = []
    if number == 2:
        query.extend(array[70:120])
        query.extend(array[140:165])
        query.extend(array[210:235])
    elif number == 3:
        query.extend(array[140:190])
        query.extend(array[70:95])
        query.extend(array[210:235])
    elif number == 4:
        query.extend(array[210:260])
        query.extend(array[70:95])
        query.extend(array[140:165])
    return query

def gpt_execution(context, query):

    roll1 = ("You are ChatGPT, a large language model trained by OpenAI.\n"
        "Knowledge cutoff: 2021-09\n"
        "Current date: 2023-10-15\n" )
    roll2 = "You are a data analyst."

    openai.api_key = "sk-jusJclmsI4KD70DqAdFcDe7a97344a898e9791464367Bb36"

    count = 0

    run_times = 100

    while (count < run_times):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": roll2},
                    {"role": "user", "content": context + str(query[count])},
                ]
            )

            gpt_result = completion.choices[0].message["content"]

            result = find_result(gpt_result)

            if (result != 2):
                filename = "class4.txt"

                with open(filename, "a") as file:
                    file.write(str(result))
                    file.write("\n")

                print("OK: " + str(count))
                count += 1

            time.sleep(22)

        except ValueError:
            print("error: " + str(count))
            pass

        except Exception as e:
            raise e

if __name__ == "__main__":
    context = generate_context(4)
    query = generate_query(4)
    gpt_execution(context, query)