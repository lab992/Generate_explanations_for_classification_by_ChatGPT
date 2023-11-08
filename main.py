# from util import FileReader, FeatureSelection
from util import FileReader, FeatureSelection, GPTExecutor, DecisionTree, ContextGenerator, QueryTransformer

def pipeline():
    # X_train, X_test, y_train, y_test = FileReader.read_file_acc()

    X_train, X_test, y_train, y_test = FileReader.read_file_basket()

    # X_train, X_test, y_train, y_test = FileReader.read_file_HMP()

    FEATURE_AMOUNT = 3
    train_set, test_set = FeatureSelection.feature_selection(X_train, X_test, y_train, FEATURE_AMOUNT)
    
    # DecisionTree.graph_and_accuracy(train_set, test_set, y_train, y_test)

    context, lookup_table = ContextGenerator.gen_context("basketball", train_set, y_train)

    query = QueryTransformer.gen_query(test_set, lookup_table)
    
    print("ok")

    GPTExecutor.gpt_execution(context, query)

if __name__ == "__main__":
    pipeline()