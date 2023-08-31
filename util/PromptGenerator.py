
def context_gen():
    role = "You are a data analyst, your job is to classify time series by the given features."
    background = ("The gesture acquisition device is a Nintendo Wiimote remote controller with built-in three-axis accelerometer."
                    "Data is acceleration in x-axis dimension. It is classified to 10 gestures"
                    )
    classes = ("The gestures are (class label - English translation): "
                "1 – pick-up"
                "2 – shake"
                "3 – one move to the right"
                "4 – one move to the left"
                "5 – one move to up"
                "6 – one move to down"
                "7 – one left circle"
                "8 – one right circle"
                "9 – one move toward the screen"
                "10 – one move away from the screen")
    features = ("The dataset has 11 columns. The first column is class and the rest are 10 features in order: "
                'standard_deviation, '
                'number_crossing_m__m_1, '
                'fft_coefficient__attr_"angle"__coeff_1, '
                'fourier_entropy__bins_5, linear_trend__attr_"slope", '
                'fourier_entropy__bins_2, '
                'range_count__max_0__min_-1000000000000.0, '
                'autocorrelation__lag_5, '
                'index_mass_quantile__q_0.4, '
                'mean_n_absolute_max__number_of_maxima_7, '
                'kurtosis. ')
                
    data_description = ("Following is the dataset of 300 data. ")
    
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