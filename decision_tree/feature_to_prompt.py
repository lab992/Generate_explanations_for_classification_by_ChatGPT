
def feature_to_prompt(dataset):

    def row_to_sentence(row):
        sentence = ''
        feature_1 = row[0]
        feature_2 = row[1]
        feature_3 = row[2]
        feature_4 = row[3]
        feature_5 = row[4]
        if feature_1 > 4.5:
            sentence += "There's a lot of changes in the direction."
        else:
            sentence += "There's few changes in the direction."
        if feature_2 <= -0.438:
            sentence += "There's a big decreasing trend."
        elif feature_2 > -0.157:
            sentence += "There's a slight decreasing trend."
        else:
            sentence += "There's a medium decreasing trend."
        if feature_3 > 99.5:
            sentence += "There's a lot of increasing values."
        else:
            sentence += "There's few increasing values."
        if feature_4 > 0.249:
            sentence += "The sample is complex."
        elif feature_4 <= 0.204:
            sentence += "The sample is stable."
        else:
            sentence += "The sample is dynamic."
        if feature_5 > 1.737:
            sentence += "There's a significant periodic pattern."
        elif feature_5 > 1.627 and feature_5 <= 1.737:
            sentence += "There's a normal periodic pattern."
        elif feature_5 <= 0.432:
            sentence += "There's no periodic pattern."
        else:
            sentence += "There's a slight periodic pattern."
        sentence += '\n'
        return sentence
    
    sentences = dataset.apply(row_to_sentence, axis=1)
    return sentences

def gen_context():
    mission_3 = ("I will give you a time-series data sample which is acceleration in x-axis dimension. "
               "Your task is to classify my description of samples to 3 gestures ('shake hand', 'move to left', 'move to right'). "
                "I will now describe these 3 classes based on 3 features: changes in the direction, decreasing trend, increasing values.\n")
    mission_5 = ("I will give you a time-series data sample which is acceleration in x-axis dimension. "
                "Your task is to classify my description of samples to 3 gestures ('shake hand', 'move to left', 'move to right'). "
                "I will now describe these 3 classes based on 5 features: changes in the direction, decreasing trend, increasing values, complex or stable, periodic pattern.\n")
    class_description_3 = ("if there's a lot of changes in the direction, then 'shake hand' \n" 
                          "if there's few changes in the direction, a big decreasing trend, then 'move to left'\n"
                          "if there's few changes in the direction, a slight decreasing trend, and a lot of increasing values, then 'move to left'\n"
                          "if there's few changes in the direction, a slight decreasing trend, and few increasing values, then 'move to right'\n"
                          )
    class_description_5 = ("if there's a lot of changes in the direction, then 'shake hand' \n" 
                            "if there's few of changes in the direction, a big decreasing trend, and the sample is stable, then 'move to left'. \n"
                            "if there's few of changes in the direction, a big decreasing trend, and the sample is dynamic or complex, then 'shake hand'. \n"
                            "if there's few of changes in the direction, a slight or medium decreasing trend, a lot of increasing values, and has a significant periodic pattern, then 'move to right'. \n"
                            "if there's few of changes in the direction, a slight or medium decreasing trend, a lot of increasing values, and has no or a normal periodic pattern, then 'move to left'. \n"
                            "if there's few of changes in the direction, a slight or medium decreasing trend, few increasing values, and the sample is complex, then 'shake hand'. \n"
                            "if there's few of changes in the direction, a slight or medium decreasing trend, few increasing values, the sample is stable or dynamic, and has a normal or significant periodic pattern, then 'shake hand'. \n"
                            "if there's few of changes in the direction, a slight decreasing trend, few increasing values, the sample is stable or dynamic, and has no or a slight periodic pattern, then 'move to right'. \n"
                            "if there's few of changes in the direction, a medium decreasing trend, few increasing values, the sample is stable or dynamic, and has a slight periodic pattern, then 'move to right'. \n"
                            "if there's few of changes in the direction, a medium decreasing trend, few increasing values, the sample is stable or dynamic, and has no periodic pattern, then 'move to left'. \n"
                            )
    rules = ("Try to classify the following data sample to these 3 classes. "
             "You must classify according to the description of classes. You should also give me the explaination why this decription can infer to this gesture."
             "Don't show me the code. "
             "At the end of your explanation. You must repeat your answer in format: [Class: gesture].\n")
    
    return mission_5 + class_description_5 + rules

def array_to_query(dataset):
    array = dataset.iloc[list(range(0,50)) + list(range(70,120)) + list(range(140,190))].to_numpy()
    result = []
    for i in range(10):
        sentence = ""
        for x in range(0 + 5 * i, 5 + 5 * i):
            sentence += array[x]
        for y in range(50 + 5 * i, 55 + 5 * i):
            sentence += array[y]
        for z in range(100 + 5 * i, 105 + 5 * i):
            sentence += array[z]
        result.append(sentence)
    return result


