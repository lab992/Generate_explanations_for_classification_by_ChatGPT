def feature_to_prompt(dataset, rules):

    def row_to_sentence(row):
        sentence = ''
        feature_1 = row[0]
        feature_2 = row[1]
        feature_3 = row[2]
        feature_4 = row[3]
        if feature_1 > 4.5:
            sentence += 'the value of ' + 'number_crossing_m__m_1' + ' is high.'
        else:
            sentence += 'the value of ' + 'number_crossing_m__m_1' + ' is low.'
        if feature_2 > -0.438:
            sentence += 'the value of ' + 'agg_linear_trend__attr_"intercept"__chunk_len_5__f_agg_"min"' + ' is high.'
        else:
            sentence += 'the value of ' + 'agg_linear_trend__attr_"intercept"__chunk_len_5__f_agg_"min"' + ' is low.'
        if feature_3 > 99.5:
            sentence += 'the value of ' + 'range_count__max_1000000000000.0__min_0' + ' is high.'
        else:
            sentence += 'the value of ' + 'range_count__max_1000000000000.0__min_0' + ' is low.'
        if feature_4 > 0.193:
            sentence += 'the value of ' + 'approximate_entropy__m_2__r_0.7' + ' is high.'
        else:
            sentence += 'the value of ' + 'approximate_entropy__m_2__r_0.7' + ' is low.'
        sentence += '\n'
        return sentence
    
    sentences = dataset.apply(row_to_sentence, axis=1)
    return sentences

def gen_context():
    mission = ("Your task is to classify my description of samples to 3 classes (Class 2, Class 3, Class 4). Each sample has 4 features. "
    "I will now describe these 3 classes based on these 4 features.\n")
    class_description = ("Class 2:\n"
                         "Situation1: The value of 'number_crossing_m__m_1' is high.\n"
                         "Situation2: The value of 'number_crossing_m__m_1' is low."
                         "The value of 'agg_linear_trend__attr_'intercept'__chunk_len_5__f_agg_'min'' is low,"
                         "The value of 'approximate_entropy__m_2__r_0.7' is high.\n"
                         "Class 3:\n"
                         "Situation1: The value of 'number_crossing_m__m_1' is low."
                         "The value of 'agg_linear_trend__attr_'intercept'__chunk_len_5__f_agg_'min'' is high,"
                         "The value of 'acceleration__range_count__max_1000000000000.0__min_0' is high.\n"
                         "Situation2: The value of 'number_crossing_m__m_1' is low."
                         "The value of 'agg_linear_trend__attr_'intercept'__chunk_len_5__f_agg_'min'' is low,"
                         "The value of 'approximate_entropy__m_2__r_0.7' is low.\n"
                         "Class 4:\n"
                         "The value of 'number_crossing_m__m_1' is low."
                         "The value of 'agg_linear_trend__attr_'intercept'__chunk_len_5__f_agg_'min'' is high,"
                         "The value of 'acceleration__range_count__max_1000000000000.0__min_0' is low.\n"
                         )
    rules = ("Try to classify following 15 data to these 3 classes. You must classify according to the description of classes. "
             "Don't show me the code but give the answer directly. "
             "You must give me the answer in format: [sample 1, sample 2, ..., sample 15]. For example: [2,2,2,2,2,3,3,3,3,3,4,4,4,4,4]"
             "You must check whether there are exactly 15 samples in your answer.\n")
    
    return mission + class_description + rules

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


