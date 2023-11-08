from util.RuleGenerator import gen_rules, translation_to_rules

def gen_background(dataset):

    background = ""

    background_acc = ("I will give you a time-series data sample which is acceleration in x-axis dimension. "
               "Your task is to classify my description of samples to 3 gestures (2: 'shake hand', 3: 'move to left', 4: 'move to right'). "
                "I will now describe these 3 classes based on 3 features: changes in the direction, decreasing trend, increasing values.\n")
    background_basket = ("I will give you a time-series data sample which is acceleration in x-axis dimension. "
               "Your task is to classify my description of samples to 3 basketball activities ('dribble', 'hold', 'pass'). "
                "I will now describe these 3 classes based on 2 features: irrgularity, changes in the direction.\n")
    background_HMP = ("I will give you a time-series data sample which is acceleration in x-axis dimension. "
               "Your task is to classify my description of samples to 3 human motions ('comb hair', 'descend stairs', 'lie down bed'). "
                "I will now describe these 3 classes based on 2 features: events at the beginning of the observed period, decreasing trend.\n")
    
    if dataset == "acc":
        background += background_acc
    elif dataset == "basketball":
        background += background_basket
    elif dataset == "HMP":
        background += background_HMP
    
    return background

def gen_context(dataset, train_set, y_train):

    background = gen_background(dataset)

    translations, lookup_table = gen_rules(train_set, y_train)

    rules = translation_to_rules(translations)

    regulation = ("Try to classify the following data sample to these 3 classes. "
             "You must classify according to the description of classes. You should also give me the explaination why this decription can infer to this motion."
             "Don't show me the code. "
             "At the end of your explanation. You must repeat your answer in format: [Class: motion].\n")
    
    return background + rules + regulation, lookup_table
