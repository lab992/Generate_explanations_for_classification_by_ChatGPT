import pandas as pd

# Find the feature written in the lookup table
# lookup table record the split value
# feature value will be transformed by split value
def find_row(lookup_table, feature_name):
    feature_list = lookup_table['feature']
    row_index = -1
    for i in range(len(feature_list)):
        if feature_list.iloc[i] in feature_name:
            row_index += i + 1
            break
    
    if row_index == -1:
        raise ValueError("Not in lookup table.")

    filtered_rows = lookup_table.iloc[row_index]

    return filtered_rows

# Generate query part
def gen_query(dataset, lookup_table):

    # There's a situation that even I set feature amount as 3, desicion tree use only 2 features to classify
    # Thus, use this function to delete excessive features.
    def dataset_filter(dataset):

        filtered = []
        feature_list = lookup_table['feature']
        for i in range(len(feature_list)):
            filtered_columns = dataset.filter(like=feature_list[i])
            filtered.append(filtered_columns)
        
        result = pd.concat(filtered, axis=1)
        return result

    # transfer array to a sentence according to lookup table
    def row_to_sentence(row):
        sentence = ''
        
        for i in range(len(row)):
            feature_name = filtered_dataset.columns[i]
            filtered_row = find_row(lookup_table, feature_name)
            meaning = filtered_row['meaning']
            value = float(filtered_row['value'])
            type = filtered_row['type']
            tf = filtered_row['tf']
            row_value = row[i]
            if tf == 0:
                if type == 'adj':
                    if row_value <= value:
                        sentence += "There's a slight " + meaning + ". "
                    else:
                        sentence += "There's a big " + meaning + ". "
                elif type == 'n':
                    if row_value <= value:
                        sentence += "There's few " + meaning + ". "
                    else:
                        sentence += "There's a lot of " + meaning + ". "
                else:
                    raise ValueError("Wrong type.")
            elif tf == 1:
                if type == 'adj':
                    if row_value <= value:
                        sentence += "There's a big " + meaning + ". "
                    else:
                        sentence += "There's a slight " + meaning + ". "
                elif type == 'n':
                    if row_value <= value:
                        sentence += "There's a lot of " + meaning + ". "
                    else:
                        sentence += "There's few " + meaning + ". "
                else:
                    raise ValueError("Wrong type.")
            else:
                raise ValueError("Wrong tf.")

        sentence += '\n'
        return sentence
    
    filtered_dataset = dataset_filter(dataset)
    sentences = filtered_dataset.apply(row_to_sentence, axis=1)
    return sentences