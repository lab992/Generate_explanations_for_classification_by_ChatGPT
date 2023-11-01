from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, plot_tree

def graph_and_accuracy(train_set, test_set, y_train, y_test):
    
    model = DecisionTreeClassifier(random_state=42)
    clf = model.fit(train_set, y_train)

    fig = plt.figure(figsize=(50, 40))
    _ = plot_tree(
        clf,
        feature_names = train_set.columns.to_list(),
        class_names = ["comb_hair","descend_stairs","lie_down_bed"],
        filled = True
    )

    fig.savefig("HMP.png")

    y_pred = model.predict(test_set)
    print(y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

