import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Load dataset
df = pd.read_csv("match_data.csv")

print("Dataset Shape:", df.shape)

# Remove missing values
df.dropna(inplace=True)

# Extract winner from result

def extract_winner(result):
    result = str(result)

    if "India won" in result:
        return "India"

    if "Australia won" in result:
        return "Australia"

    return "No Result"

df["winner"] = df["result"].apply(extract_winner)

# Remove no result matches
df = df[df["winner"] != "No Result"]

# Team columns
df["team1"] = "India"
df["team2"] = "Australia"

# Encode categorical features

le_team1 = LabelEncoder()
le_team2 = LabelEncoder()
le_venue = LabelEncoder()
le_target = LabelEncoder()

df["team1"] = le_team1.fit_transform(df["team1"])
df["team2"] = le_team2.fit_transform(df["team2"])
df["venue"] = le_venue.fit_transform(df["venue"])
df["winner"] = le_target.fit_transform(df["winner"])

X = df[["team1", "team2", "venue"]]
y = df["winner"]

# Train/Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Random Forest

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction

y_pred = model.predict(X_test)

# Metrics

accuracy = accuracy_score(y_test, y_pred)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted"
)

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nAccuracy:", round(accuracy, 4))
print("\nF1 Score:", round(f1, 4))

print("\nConfusion Matrix")
print(cm)

print("\nClassification Report")
print(classification_report(y_test, y_pred))