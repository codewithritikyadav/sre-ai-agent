from sklearn.ensemble import IsolationForest
import numpy as np


def calculate_anomaly(logs):

    error_count = logs.lower().count("error")

    warn_count = logs.lower().count("warn")

    timeout_count = logs.lower().count("timeout")

    failed_count = logs.lower().count("failed")

    features = np.array([
        [
            error_count,
            warn_count,
            timeout_count,
            failed_count
        ]
    ])

    model = IsolationForest(contamination=0.1)

    # Fake training data for MVP
    training_data = np.array([
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [5, 3, 2, 1],
        [10, 5, 4, 3],
    ])

    model.fit(training_data)

    score = model.decision_function(features)[0]

    anomaly_score = round((1 - score) * 100, 2)

    return anomaly_score