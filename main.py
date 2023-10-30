from util import FileReader

def pipeline():
    # X_train, X_test, y_train, y_test = FileReader.read_file_acc()
    # X, y = FileReader.read_file_basket()
    X, y = FileReader.read_file_HMP()
    print("OK")

if __name__ == "__main__":
    pipeline()