import pickle
import sklearn
import pandas as pd
import joblib
from datetime import date


model_filename = 'model.mod'
df_filename = 'pickled_df'


def load_model(filename):
    # Load model from file
    model = joblib.load(filename)
    return model

def load_df(file_name):
    return pd.read_pickle(file_name)


def make_prediction(latitude, longitude, speed_over_ground_knots, heading_true_course, epoch_ts):
    # method return a prediciton type float, based on provided features
    features = [[latitude, longitude, speed_over_ground_knots, heading_true_course, epoch_ts]]
    prediciton = model.predict(features)
    return prediciton[0]


if __name__ == "__main__":
    model = load_model(model_filename)
    df = load_df(df_filename)
    print(make_prediction(48.152675,	11.534113,	0.379,	0.00,	1618219659.0))