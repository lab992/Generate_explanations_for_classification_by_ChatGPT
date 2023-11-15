from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, plot_tree

# generate decision tree graph and accuracy

def graph_and_accuracy(train_set, test_set, y_train, y_test):
    
    model = DecisionTreeClassifier(random_state=42)
    clf = model.fit(train_set, y_train)

    # generate decision tree graph

    fig = plt.figure(figsize=(50, 40))
    _ = plot_tree(
        clf,
        feature_names = train_set.columns.to_list(),
        class_names = list(set(y_train)),
        filled = True
    )

    fig.savefig("decision_tree.png")

    # print accuracy and detailed result of classification
    y_pred = model.predict(test_set)
    print(y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

