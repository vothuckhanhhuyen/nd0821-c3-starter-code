import sys
import os
import pickle
import pandas as pd
from ml.data import process_data
from ml.model import compute_model_metrics, inference

def slice_metrics(model, encoder, lb, data, slice_feature, categorical_features=[]):
    """
    Output the performance of the model on slices of the data

    Inputs
    ------
    model : Machine learning model
        Trained machine learning model.
    encoder : sklearn.preprocessing._encoders.OneHotEncoder
        Trained sklearn OneHotEncoder, only used if training=False.
    lb : sklearn.preprocessing._label.LabelBinarizer
        Trained sklearn LabelBinarizer, only used if training=False.
    data : pd.DataFrame
        Dataframe containing the features and label.
    slice_feature: str
        Name of the feature used to make slices (categorical features)
    categorical_features: list[str]
        List containing the names of the categorical features (default=[])
    Returns
    -------
    None
    """
    original_stdout = sys.stdout
    with open(os.path.join(os.path.dirname(__file__), "slice_output.txt"), "w") as f:
        sys.stdout = f
        print("Performance on slices of data based on", slice_feature)
        print("*****************************************************")
        X, y, _, _ = process_data(
            data, categorical_features=categorical_features, label="salary", training=True
        )
        preds = inference(model, X)

        for slice_value in data[slice_feature].unique():
            slice_index = data.index[data[slice_feature] == slice_value]
            
            print(slice_feature, '=', slice_value)
            print('data size:', len(slice_index))
            print('precision: {}, recall: {}, fbeta: {}'.format(
                *compute_model_metrics(y[slice_index], preds[slice_index])
            ))
            print('-------------------------------------------------')
        sys.stdout = original_stdout

if __name__ == '__main__':
    cat_features = [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
    ]
    file_dir = os.path.dirname(__file__)
    data = pd.read_csv(os.path.join(file_dir, '../data/clean_census.csv'))

    model_path = os.path.join(file_dir, '../model/rf_model.pkl')
    model = pickle.load(open(model_path, 'rb'))

    encoder_path = os.path.join(file_dir, '../model/encoder.pkl')
    encoder = pickle.load(open(encoder_path, 'rb'))

    lb_path = os.path.join(file_dir, '../model/lb.pkl')
    lb = pickle.load(open(lb_path, 'rb'))

    slice_metrics(model, encoder, lb, data, 'workclass', categorical_features=cat_features)