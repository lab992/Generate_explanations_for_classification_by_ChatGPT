import openai
import time
import os

# Make folders for separate classes
def makedir(dataset, given_model):
    if dataset == "acc":
        os.makedirs(given_model + "/shake_hand/")
        os.makedirs(given_model + "/move_to_left/")
        os.makedirs(given_model + "/move_to_right/")
    elif dataset == "basketball":
        os.makedirs(given_model + "/dribble/")
        os.makedirs(given_model + "/pass/")
        os.makedirs(given_model + "/hold/")
    elif dataset == "HMP":
        os.makedirs(given_model + "/Comb_hair/")
        os.makedirs(given_model + "/Descend_stairs/")
        os.makedirs(given_model + "/Liedown_bed/")

# Add line to answers. Make the text more readable.
def split_answers(file):
    file.write("\n")
    file.write("-----------------------")
    file.write("\n")

# Output of AllGestureWiimoteX
def acc_output(count, gpt_result, given_model):

    if count < 20:
        with open(given_model + "/shake_hand/shake_hand_" + str(count) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)
    elif count > 39:
        with open(given_model + "/move_to_right/move_to_right_" + str(count - 40) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)
    else:
        with open(given_model + "/move_to_left/move_to_left_" + str(count - 20) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)

# Output of basketball motion
def basket_output(count, gpt_result, given_model):
    if count < 3:
        with open(given_model + "/dribble/dribble_" + str(count) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)
    elif count > 5:
        with open(given_model + "/pass/pass_" + str(count - 6) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)
    else:
        with open(given_model + "/hold/hold_" + str(count - 3) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)

# Output of HMP
def HMP_output(count, gpt_result, given_model):
    if count < 5:
        with open(given_model + "/Comb_hair/Comb_hair_" + str(count) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)
    elif count > 9:
        with open(given_model + "/Liedown_bed/Liedown_bed_" + str(count - 10) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)
    else:
        with open(given_model + "/Descend_stairs/Descend_stairs_" + str(count - 5) + ".txt", "a") as file:
            file.write(gpt_result)
            split_answers(file)

# link to OpenAI API
def gpt_execution(context, query, dataset, given_model):

    roll = "You are a data analyst."

    # Enter API key here.
    openai.api_key = ""

    if openai.api_key == "":
        raise ValueError("Please enter API key!")

    count = 0
    run_times = len(query)

    makedir(dataset, given_model)

    while (count < run_times):
        try:
            # Each sample should be test for 5 times to avoid answer uncertainty.
            for i in range(5):
                completion = openai.ChatCompletion.create(
                    model = given_model,
                    messages=[
                        {"role": "system", "content": roll},
                        {"role": "user", "content": context + query[count]},
                    ]
                )

                gpt_result = completion.choices[0].message["content"]

                if dataset == "acc":
                    acc_output(count, gpt_result, given_model)
                elif dataset == "basketball":
                    basket_output(count, gpt_result, given_model)
                elif dataset == "HMP":
                    HMP_output(count, gpt_result, given_model)

                # Set a time intervall for API
                # Free API's limit is 3 answers/min, Paid API is 500 answers/min
                time.sleep(1)
            count += 1
            
        except ValueError:
            print("error: " + str(count))
            pass

        except Exception as e:
            raise e

    