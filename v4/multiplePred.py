import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=42)

# Train RandomForestClassifier
rf = RandomForestClassifier(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)

# Get individual tree predictions
tree_preds = np.array([tree.predict(X_test).astype(int) for tree in rf.estimators_])  # Convert to int

# Get majority vote prediction
final_preds = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=tree_preds)

print("Individual Tree Predictions:\n", tree_preds)
print("Final Predictions:\n", final_preds)
