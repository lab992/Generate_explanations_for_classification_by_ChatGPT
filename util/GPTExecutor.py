import openai
import time

def judge_correctness(array1, array2):
    count = sum([1 for a, b in zip(array1, array2) if a == b])
    result = count / len(array1)
    percentage = round(result * 100, 4)
    return f"{percentage}%"

class GPTExecutor:

    def __init__(self, context, query):
        self.context = context
        self.query = query


    def gpt_execution(context, query):
        openai.api_key = "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"

        count = 0

        run_times = 20

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

                with open(filename, "a") as file:
                    file.write(', '.join(map(str, gpt_result)))
                    file.write("\n")
                
                count += 1

                time.sleep(25)
            except ValueError:
                print("error")
                pass
            except Exception as e:
                raise e
        return