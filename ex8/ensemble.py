import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# ---- User Inputs ----
filename = input("Enter dataset filename (CSV): ")
n_est = int(input("Enter number of decision trees (n_estimators): "))

# ---- Load Dataset ----
data = np.loadtxt(filename, delimiter=',', skiprows=1)

# Split into features and target
X = data[:, :-1]
y = data[:, -1]

# ---- Splits ----
split_ratios = [0.30, 0.40, 0.25]
split_names = ["70-30", "60-40", "75-25"]

final_results = []

# ---- Loop through splits ----
for i in range(len(split_ratios)):
    print("\n--------------------------------------------")
    print("Split:", split_names[i])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=split_ratios[i], random_state=42
    )

    print("Train samples:", len(X_train))
    print("Test samples :", len(X_test))

    # Model
    rf = RandomForestClassifier(n_estimators=n_est, random_state=42)
    rf.fit(X_train, y_train)

    # Prediction
    y_pred = rf.predict(X_test)

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm.ravel()

    print("\nConfusion Matrix:")
    print("          Predicted 0   Predicted 1")
    print("Actual 0     TN=", TN, "   FP=", FP)
    print("Actual 1     FN=", FN, "   TP=", TP)

    # Metrics
    accuracy = round(accuracy_score(y_test, y_pred), 4)
    precision = round(precision_score(y_test, y_pred), 4)
    recall = round(recall_score(y_test, y_pred), 4)
    f1 = round(f1_score(y_test, y_pred), 4)

    print("\nAccuracy :", accuracy)
    print("Precision:", precision)
    print("Recall   :", recall)
    print("F1 Score :", f1)

    final_results.append([split_names[i], TP, TN, FP, FN, accuracy, precision, recall, f1])

# ---- Final Table ----
print("\n\nFinal Consolidated Results:")
print("Split   TP   TN   FP   FN   Accuracy  Precision  Recall   F1-Score")

for row in final_results:
    print(f"{row[0]}  {row[1]}   {row[2]}    {row[3]}    {row[4]}   {row[5]:.4f}   {row[6]:.4f}   {row[7]:.4f}   {row[8]:.4f}")
