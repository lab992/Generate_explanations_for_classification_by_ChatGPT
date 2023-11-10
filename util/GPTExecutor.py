import openai
import time

def acc_output(count, gpt_result):
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

def basket_output(count, gpt_result):
    if count < 3:
        with open("dribble_" + str(count) + ".txt", "a") as file:
            file.write(gpt_result)
            file.write("\n")
    elif count > 5:
        with open("pass_" + str(count - 6) + ".txt", "a") as file:
            file.write(gpt_result)
            file.write("\n")
    else:
        with open("hold_" + str(count - 3) + ".txt", "a") as file:
            file.write(gpt_result)
            file.write("\n")

def HMP_output(count, gpt_result):
    if count < 5:
        with open("Comb_hair_" + str(count) + ".txt", "a") as file:
            file.write(gpt_result)
            file.write("\n")
    elif count > 9:
        with open("Descend_stairs_" + str(count - 10) + ".txt", "a") as file:
            file.write(gpt_result)
            file.write("\n")
    else:
        with open("Liedown_bed_" + str(count - 5) + ".txt", "a") as file:
            file.write(gpt_result)
            file.write("\n")


def gpt_execution(context, query):

    roll = "You are a data analyst."

    openai.api_key = "sk-UPt4ekXsKt94OR9NB3D24eEb05F8462c96D9B0B8CeFa7cE0"

    count = 13
    run_times = len(query)

    while (count < run_times):
        try:
            for i in range(5):
                completion = openai.ChatCompletion.create(
                    # model = "gpt-4"
                    # model = "gpt-3.5-turbo-0301",
                    model = "gpt-3.5-turbo-0613",
                    messages=[
                        {"role": "system", "content": roll},
                        {"role": "user", "content": context + query[count]},
                    ]
                )

                gpt_result = completion.choices[0].message["content"]

                # acc_output(count, gpt_result)
                # basket_output(count, gpt_result)
                HMP_output(count, gpt_result)

                print(str(count))
                time.sleep(1)
            count += 1
            
        except ValueError:
            print("error: " + str(count))
            pass

        except Exception as e:
            raise e

    