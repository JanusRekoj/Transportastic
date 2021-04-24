import pickle
import sklearn
import pandas as pd
import joblib
from datetime import date

class Prediction:
    def __init__(self):
        self.model_filename = 'model.mod'
        self.df_filename = 'pickled_df'
        self.load_model()


    def load_model(self):
        # Load model from file
        model = joblib.load(self.model_filename)
        return model

    def load_df(self):
        return pd.read_pickle(self.df_filename)


    def make_prediction(self, latitude, longitude, speed_over_ground_knots, heading_true_course, epoch_ts):
        # method return a prediciton type float, based on provided features
        features = [[latitude, longitude, speed_over_ground_knots, heading_true_course, epoch_ts]]
        prediciton = model.predict(features)
        return prediciton[0]


if __name__ == "__main__":
    pred = Prediction()
    print(pred.make_prediction(48.152675,	11.534113,	0.379,	0.00,	1618219659.0))