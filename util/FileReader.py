import os
import glob
import pandas as pd

# In this class, I transform original data to TSFRESH format. 
# If you want to use a new dataset, you need to add a function.
# Since different datasets have different format, I can't program a universal method.

# read dataset AllGestureWiimoteX
def read_file_acc():

    train_data = None
    test_data = None

    train_data = pd.read_table('selected_dataset/acc/AllGestureWiimoteX_TRAIN.txt', sep = '\s+', header=None)
    test_data = pd.read_table('selected_dataset/acc/AllGestureWiimoteX_TEST.txt', sep = '\s+', header=None)

    # transform original dataset to tsfresh format.
    # bias is because I don't select data from the first class.
    # tsfresh demand that the index of dataset should be equal to target, use bias can avoid this error.
    def data_format_acc(data, bias):
        num_rows, num_columns = data.shape
        result = pd.DataFrame(columns=['lable', 'id', 'time', 'acceleration'])
        for i in range(num_rows):
            row = data.iloc[i]
            df = pd.DataFrame({
                'lable': [row[0]] * len(row[1:]),
                'id': [i + bias] * len(row[1:]),
                'time': [i * 0.1 for i in range(len(row[1:]))],
                'acceleration': row[1:]               
            })
            result = pd.concat([result, df])
        result = result.dropna().reset_index(drop=True)
        return result

    # Select Class 2,3,4
    # In original dataset, each class 30 train samples and 70 test samples.
    train_data = train_data.iloc[30:120]
    # test_data = test_data.iloc[70:280]
    test_data = test_data.iloc[list(range(70,90)) + list(range(140,160)) + list(range(210,230))]

    structured_train = data_format_acc(train_data, 30)
    structured_test = data_format_acc(test_data, 70)

    X_train = structured_train.iloc[:, 1:]
    X_test = structured_test.iloc[:, 1:]
    y_train = train_data.iloc[:, 0]
    y_test = test_data.iloc[:, 0]
    
    return X_train, X_test, y_train, y_test
    

# read dataset basketball motion
def read_file_basket():

    train_files = glob.glob(os.path.join('selected_dataset/basket/train', '*.txt'))
    test_files = glob.glob(os.path.join('selected_dataset/basket/test', '*.txt'))

    # split file name
    def file_name_classifier(file_name):
        split = file_name[:-4].split('_')
        user = split[0]
        frequency = split[1][-1]
        label = split[1][:-1]
        return user, frequency, label

    # transform original dataset to tsfresh format.
    def read_dataset(files):

        result = None
        y = []
        for txt_file in files:
            # Get the class name of train set
            file_name = os.path.basename(txt_file)
            user, frequency, label = file_name_classifier(file_name)
            df = pd.read_table(txt_file, skiprows=3, sep = ',')

            num_rows = len(df)
            df['User'] = [user] * num_rows
            df['Frequency'] = [frequency] * num_rows

            result = pd.concat([result, df])
            y.append(label)
        
        result['id'] = (result['Frequency'] != result['Frequency'].shift()).cumsum() - 1
        new_df = result[['id', 'Time (s)', ' X (m/s2)']]
        # uniform column name from 'Time(s)' to time
        new_df.rename(columns={'Time (s)': 'time', ' X (m/s2)': 'x'}, inplace=True)
        new_df = new_df.dropna().reset_index(drop=True)
        result_y = pd.Series(y)

        return new_df, result_y
    
    X_train, y_train = read_dataset(train_files)
    X_test, y_test = read_dataset(test_files)
    
    return X_train, X_test, y_train, y_test


# read dataset HMP
def read_file_HMP():

    train_folders = []
    train_folders.append('selected_dataset/HMP/train/Descend_stairs')
    train_folders.append('selected_dataset/HMP/train/Comb_hair')
    train_folders.append('selected_dataset/HMP/train/Liedown_bed')

    test_folders = []
    test_folders.append('selected_dataset/HMP/test/Descend_stairs')
    test_folders.append('selected_dataset/HMP/test/Comb_hair')
    test_folders.append('selected_dataset/HMP/test/Liedown_bed')

    def read_folders(folders):
        result = None
        y = []
        file_pair = []

        for folder_path in folders:
            folder_name = os.path.basename(folder_path)

            # read all files in the folder
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(folder_path, file_name)
                    file_pair.append((folder_name, file_path))

        # transform original dataset to tsfresh format.
        for i in range(len(file_pair)):
            folder_name, file_path = file_pair[i]
            data = pd.read_table(file_path, sep = ' ', header=None)
            num_rows = len(data)
            df = pd.DataFrame({
                    # 'lable': [folder_name] * num_rows,
                    'id': [i] * num_rows,
                    'time': [i * 0.1 for i in range(num_rows)],
                    'x': data.iloc[:, 0]
                    # 'y': data.iloc[:, 1],
                    # 'z': data.iloc[:, 2]       
                })


            result = pd.concat([result, df])
            y.append(folder_name)

        result = result.dropna().reset_index(drop=True)
        result_y = pd.Series(y)
        return result, result_y
    
    X_train, y_train = read_folders(train_folders)
    X_test, y_test = read_folders(test_folders)
    return X_train, X_test, y_train, y_test



