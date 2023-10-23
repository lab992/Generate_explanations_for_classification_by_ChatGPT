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

def gen_query(query, i):
    query_array = ''
    for i in range(0, len(query), 20):
        start_index = i
        end_index = min(i + 4, len(array) - 1)
    return query_array

def gpt_execution(context, query):

    roll1 = ("You are ChatGPT, a large language model trained by OpenAI.\n"
        "Knowledge cutoff: 2021-09\n"
        "Current date: 2023-10-15\n" )
    roll2 = "You are a data analyst."

    openai.api_key = "sk-jusJclmsI4KD70DqAdFcDe7a97344a898e9791464367Bb36"

    count = 0

    run_times = 10

    while (count < run_times):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": roll2},
                    {"role": "user", "content": context + query[count]},
                ]
            )

            gpt_result = completion.choices[0].message["content"]

            answer = [2,2,2,2,2,3,3,3,3,3,4,4,4,4,4]

            with open("explain.txt", "a") as file:
                file.write(gpt_result)
                file.write("  " + judge_correctness(gpt_result_to_array(gpt_result), answer))
                file.write("\n")

            count += 1
            print("OK")
            time.sleep(22)

        except ValueError:
            print("error: " + str(count))
            pass

        except Exception as e:
            raise e