
def context_gen():
    role = "You are a data analyst, your job is to classify  time series by the given features."
    background = ("The gesture acquisition device is a Nintendo Wiimote remote controller with built-in three-axis accelerometer."
                    "Time series are of different lengths."
                    "Data is acceleration in x-axis dimension. It is classified to 10 gestures"
                    )
    classes = ("The gestures are (class label. original label - English translation): "
                "1. poteg – pick-up"
                "2. shake – shake"
                "3. desno – one move to the right"
                "4. levo – one move to the left"
                "5. gor – one move to up"
                "6. dol – one move to down"
                "7. kroglevo – one left circle"
                "8. krogdesno – one right circle"
                "9. suneknot – one move toward the screen"
                "10. sunekven – one move away from the screen")
    data_description = ("Following is the dataset. "
                        "The first column of each line is the class, the rest columns are acceleration in x-axis dimension:")
    
    # 528 tokens
    # 预留 1000 token给query和回答
    # 每个数字4 token，大概7位有效数字
    
    feature = feature_gen()

    return role + "\n" + background + "\n" + classes + "\n" + data_description + "\n" + feature

def query_gen():
    mission = "Try to classify following\n"
    mission += feature_gen()
    pass

def feature_gen():
    pass

def explanation_gen():
    pass

class PromptGenerator:

    def __init__(self, X_train, X_test, y_train):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train

    def prompt_generator(context, query):
        pass