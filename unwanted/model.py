import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Example: Simulated database logs
data = pd.DataFrame({
    "row_diff": [5, -3, 0, 7, -4],  # +ve for inserts, -ve for deletes, 0 for updates
    "updated_cells": [0, 0, 20, 0, 0],  # Non-zero indicates updates
    "operation": ["insert", "delete", "update", "insert", "delete"]  # Labels
})

# Preprocess
X = data[["row_diff", "updated_cells"]]
y = data["operation"]

# Encode labels
y = y.map({"insert": 0, "delete": 1, "update": 2})

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
#print(classification_report(y_test, y_pred))

# Example real-time detection
new_snapshot = pd.DataFrame({"row_diff": [-2], "updated_cells": [0]})
predicted_op = clf.predict(new_snapshot)
print(f"Predicted Operation: {['insert', 'delete', 'update'][predicted_op[0]]}")