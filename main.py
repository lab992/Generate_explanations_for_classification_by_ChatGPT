from util import FileReader, FeatureSelection
# from util import FileReader, FeatureSelection, GPTExecutor, DecisionTree, ContextGenerator

def pipeline():
    X_train, X_test, y_train, y_test = FileReader.read_file_acc()

    # X_train, X_test, y_train, y_test = FileReader.read_file_basket()

    # X_train, X_test, y_train, y_test = FileReader.read_file_HMP()

    FEATURE_AMOUNT = 3
    train_set, test_set = FeatureSelection.feature_selection(X_train, X_test, y_train, y_test, FEATURE_AMOUNT)
    
    # DecisionTree.graph_and_accuracy(train_set, test_set, y_train, y_test)

    # context = ContextGenerator.
    

    # GPTExecutor.gpt_execution(context, query)

if __name__ == "__main__":
    pipeline()