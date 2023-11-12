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

def pure_decision_tree_method(context, query):
    roll2 = "You are a data analyst."

    count = 20

    run_times = 60

    while (count < run_times):
        try:
            for i in range(5):
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0301",
                    messages=[
                        {"role": "system", "content": roll2},
                        {"role": "user", "content": context + query[count]},
                    ]
                )

                gpt_result = completion.choices[0].message["content"]

                if count < 20:
                    with open("shake_hand_" + str(count) + ".txt", "a") as file:
                        file.write(gpt_result)
                        file.write("\n")
                elif count > 39:
                    with open("move_to_right_" + str(count - 40) + ".txt", "a") as file:
                        file.write(gpt_result)
                        file.write("\n")
                else:
                    with open("move_to_left_" + str(count - 20) + ".txt", "a") as file:
                        file.write(gpt_result)
                        file.write("\n")

                print(str(count))
                time.sleep(1)
            count += 1



        except ValueError:
            print("error: " + str(count))
            pass

        except Exception as e:
            raise e
        
def decision_tree_to_gpt(context, query):
    roll2 = "You are a data analyst."

    count = 0

    run_times = 60

    while (count < run_times):
        q = query[count]
        sample = [str(value) for value in q]
        try:
            completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=[
                        {"role": "system", "content": roll2},
                        {"role": "user", "content": context + ''.join(sample)},
                    ])
            gpt_result = completion.choices[0].message["content"]

            with open("transform.txt", "a") as file:
                file.write(gpt_result)
                file.write("\n")

            print(count)
            count += 1
        
        except ValueError:
            print("error: " + str(count))
            pass

        except Exception as e:
            raise e

def gpt_execution(context, query):

    roll1 = ("You are ChatGPT, a large language model trained by OpenAI.\n"
        "Knowledge cutoff: 2021-09\n"
        "Current date: 2023-10-15\n" )
    roll2 = "You are a data analyst."

    openai.api_key = "sk-UPt4ekXsKt94OR9NB3D24eEb05F8462c96D9B0B8CeFa7cE0"

    count = 51

    run_times = 52

    while (count < run_times):
        try:
            for i in range(5):
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=[
                        {"role": "system", "content": roll2},
                        {"role": "user", "content": context + query[count]},
                    ]
                )

                gpt_result = completion.choices[0].message["content"]

                if count < 20:
                    with open("shake_hand_" + str(count) + ".txt", "a") as file:
                        file.write(gpt_result)
                        file.write("\n")
                elif count > 39:
                    with open("move_to_right_" + str(count - 40) + ".txt", "a") as file:
                        file.write(gpt_result)
                        file.write("\n")
                else:
                    with open("move_to_left_" + str(count - 20) + ".txt", "a") as file:
                        file.write(gpt_result)
                        file.write("\n")

                print(str(count))
                time.sleep(0.5)
            count += 1
            
        except ValueError:
            print("error: " + str(count))
            pass

        except Exception as e:
            raise e

    