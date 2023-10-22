import openai
import time
import numpy as np
from data_filter import data_filter

def find_result(text):
    if "Result: Class2" in text:
        return 2
    elif "Result: Class3" in text:
        return 3
    else:
        return 0

def generate_context():
    background = ("I will give you a data sample, which is a time-series data sample. " 
                  "This data sample ranges from 0 to 9. "
                  "Your mission is to tell me which class this sample belongs to with the help of following 2 questions.\n")
    definition2 = (
                    "'Situation1': When there's a 0 in the array, there should be a 9 after 0.\n "
                    "'Situation2': When there's a 9 in the array, there should be a 0 after 9.\n"
                    )

    definition3 = ("'nA' means 0 or 1.\n" 
                    "'nB' means 9 or 10.\n"
                    "'Situation 1' : When the index of 'nA' is smaller than the index of 'nB'.\n "
                    "'Situation 2' : When the index of 'nA' is bigger than the index of 'nB'.\n"
                    )
    question = ("Question1: Is there a 'Situation 1'?\n" 
                "Question2: Is there a 'Situation 2'?\n")
    
    stepA2 = ("You should think Question 1 step by step.\n"
            "Step1: Find a 0 first.\n"
            "Step2: Find if there's a 9 after 0.\n"
            "Step3: Check whether the index of 9 is greater than the index of 0.\n")
    
    stepB2 = ("You should think Question 2 step by step.\n"
            "Step1: Find a 9 first.\n"
            "Step2: Find if there's a 0 after 9.\n"
            "Step3: Check whether the index of 0 is greater than the index of 9.\n")


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
    
    class_pattern_2 = "'Class 2' must satisfy both 'Situation 1' and 'Situation 2'.\n"
    class_pattern_3 = "'Class 3' must only satisfy 'Situation 1'.\n"

    rule = ("Now I will give you one array. You should help me to classify which class this array belongs to. " 
            "Don't show me the code or curve graph.\n"
            "You should answer at the very end. The answer format should be: 'Result: Class2' or 'Result: Class3'.\n")
    return background + definition2 + question + stepA2 + stepB2 + class_pattern_2 + class_pattern_3 + rule
    
def generate_query(number):
    array = data_filter.average(2)
    query = []
    if number == 23:
        query.extend(array[70:120])
        query.extend(array[140:190])
    elif number == 34:
        query.extend(array[140:190])
        query.extend(array[210:260])
    elif number == 24:
        query.extend(array[70:120])
        query.extend(array[210:260])
    return query

def gpt_execution(context, query):

    roll1 = ("You are ChatGPT, a large language model trained by OpenAI.\n"
        "Knowledge cutoff: 2021-09\n"
        "Current date: 2023-10-16\n" )
    roll2 = "You are a data analyst."

    openai.api_key = "sk-jusJclmsI4KD70DqAdFcDe7a97344a898e9791464367Bb36"

    count = 19

    run_times = 100

    while (count < run_times):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": roll1},
                    {"role": "user", "content": context + str(query[count])},
                ]
            )

            gpt_result = completion.choices[0].message["content"]

            result = find_result(gpt_result)

            if (result != 0):
                filename = "class23.txt"

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
    context = generate_context()
    query = generate_query(23)
    gpt_execution(context, query)