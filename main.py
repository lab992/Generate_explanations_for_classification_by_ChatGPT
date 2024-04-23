# from util import FileReader, FeatureSelection
from util import FileReader, FeatureSelection, GPTExecutor, DecisionTree, ContextGenerator, QueryTransformer, GUI

# General pipeline
def pipeline(dataset, model):

    # check if input is invalid
    if dataset == "acc":
        X_train, X_test, y_train, y_test = FileReader.read_file_acc()
    elif dataset == "basketball":
        X_train, X_test, y_train, y_test = FileReader.read_file_basket()
    elif dataset == "HMP":
        X_train, X_test, y_train, y_test = FileReader.read_file_HMP()
    else:
        raise ValueError("Dataset doesn't exist.")
    
    if model != "gpt-3.5-turbo-0301" and model != "gpt-3.5-turbo-0613" and model != "gpt-4":
        raise ValueError("Wrong model.")

    FEATURE_AMOUNT = 3
    train_set, test_set = FeatureSelection.feature_selection(X_train, X_test, y_train, FEATURE_AMOUNT)
    
    # test accuracy of decision tree
    # DecisionTree.graph_and_accuracy(train_set, test_set, y_train, y_test)

    context, lookup_table = ContextGenerator.gen_context(dataset, train_set, y_train)

    query = QueryTransformer.gen_query(test_set, lookup_table)

    GPTExecutor.gpt_execution(context, query, dataset, model)

if __name__ == "__main__":
    dataset = input("Enter the name of dataset: 'acc', 'basketball', or 'HMP'")
    model = input("Enter the name of model: 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613', or 'gpt-4'")
    # GUI.open_gui()
    pipeline(dataset, model)