from util import FileReader, FeatureSelection

def pipeline():
    # X_train, X_test, y_train, y_test = FileReader.read_file_acc()

    X_train, X_test, y_train, y_test = FileReader.read_file_basket()

    # X_train, X_test, y_train, y_test = FileReader.read_file_HMP()

    FEATURE_AMOUNT = 3
    train_set, test_set = FeatureSelection.feature_selection(X_train, X_test, y_train, y_test, FEATURE_AMOUNT)
    
    print(train_set)


if __name__ == "__main__":
    pipeline()