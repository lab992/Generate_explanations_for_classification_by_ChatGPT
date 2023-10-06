import openai
import time

def judge_correctness(array1, array2):
    count = sum([1 for a, b in zip(array1, array2) if a == b])
    result = count / len(array1)
    percentage = round(result * 100, 4)
    return f"{percentage}%"

def gpt_result_to_array(string):
    stripped_string = string.strip("[]")
    elements = stripped_string.split(", ")
    array = [float(element) for element in elements]
    return array

def gpt_execution(context, query):
    openai.api_key = "sk-jusJclmsI4KD70DqAdFcDe7a97344a898e9791464367Bb36"

    count = 0

    run_times = 1

    while (count < run_times):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": query},
                ]
            )

            gpt_result = completion.choices[0].message["content"]

            filename = "explain.txt"

            answer = [2,2,2,2,2,2,2,2,2,2,4,4,4,4,4,4,4,4,4,4]

            with open(filename, "a") as file:
                file.write(gpt_result)
                file.write("  " + judge_correctness(gpt_result_to_array(gpt_result), answer))
                file.write("\n")
            
            count += 1
            print("OK")

            time.sleep(22)
        except ValueError:
            print("error")
            pass
        except Exception as e:
            raise e
    return