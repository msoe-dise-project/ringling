"""
Train a model given a parameter set in Ringling
"""
import datetime
import pickle
import numpy as np
import requests
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


# Set the endpoint url for parameter set get, and trained model create
BASE_URL = "http://localhost:8888"
PARAM_URL = "/v1/parameter_sets"
MODEL_URL = "/v1/trained_models"
PARAM_REQUEST_URL = BASE_URL + PARAM_URL
MODEL_REQUEST_URL = BASE_URL + MODEL_URL

# Set this to the ID of the project you created earlier
PROJECT_ID = 3

# Set this to the ID of the parameter set you created earlier
PARAMETER_SET_ID = 9

# Send the request, get the pickled parameter set
REQUEST_URL = PARAM_REQUEST_URL + "/" + str(PARAMETER_SET_ID)
response = requests.get(REQUEST_URL, timeout=5)
pickled_pipeline = response.json()["training_parameters"]

pipeline = pickle.loads(bytes.fromhex(pickled_pipeline))

# Load in the training data from the heart disease dataset, and split it
# Retrieved from: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
df = pd.read_csv("heart_train.csv")
X = df.drop("target", axis=1)
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the model, and get timestamp
train_timestamp = datetime.datetime.now().isoformat()

# Time based cross validation
# Please note that while this dataset does not indicate times, the following algorithm
# can be used assuming the dataframe is sorted by time to generate test metrics

K_SPLITS = 5
vals = len(X)
partition = vals // K_SPLITS

accuracies = np.zeros(K_SPLITS - 1)
precisions = np.zeros(K_SPLITS - 1)
recalls = np.zeros(K_SPLITS - 1)
areas_under_roc = np.zeros(K_SPLITS - 1)

for split in range(1, K_SPLITS):
    train_end = partition*split
    test_end = partition*(split+1)
    X_train = X.head(train_end)
    y_train = y.head(train_end)
    X_test = X.loc[train_end:test_end]
    y_test = y.loc[train_end:test_end]
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracies[split-1] = accuracy_score(y_test, y_pred)
    precisions[split-1] = precision_score(y_test, y_pred)
    recalls[split-1] = recall_score(y_test, y_pred)
    areas_under_roc[split-1] = roc_auc_score(y_test, y_pred)

test_timestamp = datetime.datetime.now().isoformat()

# Get summary statistics of all metrics generated by time based CV
accuracy = np.mean(accuracies)
accuracy_std = np.std(accuracies)
precision = np.mean(precisions)
precision_std = np.std(precisions)
recall = np.mean(recalls)
recall_std = np.std(recalls)
area_under_roc = np.mean(areas_under_roc)
area_under_roc_std = np.std(areas_under_roc)

print(f"Accuracy: {accuracy:.5f}")
print(f"Accuracy Standard Deviation: {accuracy_std:.5f}")
print(f"Precision: {precision:.5f}")
print(f"Precision Standard Deviation: {precision_std:.5f}")
print(f"Recall: {recall:.5f}")
print(f"Recall Standard Deviation: {recall_std:.5f}")
print(f"AUROC: {area_under_roc:.5f}")
print(f"AUROC Standard Deviation: {area_under_roc_std:.5f}")

passed_testing = bool(area_under_roc > 0.8)

# Prepare metrics to be sent to Ringling
test_metrics = {
    "accuracy" : accuracy,
    "accuracy_std" : accuracy_std,
    "precision" : precision,
    "precision_std" : precision_std,
    "recall" : recall,
    "recall_std" : recall_std,
    "auroc" : area_under_roc,
    "auroc_std" : area_under_roc_std
}

# Now that we have validation metrics, train the model on all available data
pipeline.fit(X, y)
pipeline_object = pickle.dumps(pipeline).hex()

# Save the model to Ringling
model_payload = {"project_id": PROJECT_ID,
                 "parameter_set_id": PARAMETER_SET_ID,
                 "training_data_from": "1988-01-01T00:00:00.000000",
                 "training_data_until": "1988-12-31T23:59:59.999999",
                 "model_object": pipeline_object,
                 "train_timestamp": train_timestamp,
                 "deployment_stage": "testing",
                 "backtest_timestamp": test_timestamp,
                 "backtest_metrics": test_metrics,
                 "passed_backtesting": passed_testing}

response = requests.post(MODEL_REQUEST_URL, json=model_payload, timeout=5)

# Make sure it worked
print(response.json())
