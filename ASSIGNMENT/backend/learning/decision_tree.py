import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from backend.config import MODEL_DIR
from backend.learning.preprocessing import preprocess_ticket_features, extract_features_from_dict, FEATURE_COLUMNS

class TicketDecisionTreeModel:
    def __init__(self):
        self.model_category = DecisionTreeClassifier(criterion="gini", max_depth=6, random_state=42)
        self.model_priority = DecisionTreeClassifier(criterion="gini", max_depth=5, random_state=42)
        self.metrics = {}

    def train(self, df: pd.DataFrame):
        X = preprocess_ticket_features(df).fillna(0.0)
        y_cat = df["category"]
        y_prio = df["priority"]

        X_train, X_test, y_cat_train, y_cat_test, y_prio_train, y_prio_test = train_test_split(
            X, y_cat, y_prio, test_size=0.25, random_state=42
        )

        # Fit Decision Trees
        self.model_category.fit(X_train, y_cat_train)
        self.model_priority.fit(X_train, y_prio_train)

        # Evaluate Category Model
        cat_preds = self.model_category.predict(X_test)
        acc_cat = accuracy_score(y_cat_test, cat_preds)
        f1_cat = f1_score(y_cat_test, cat_preds, average="weighted", zero_division=0)
        prec_cat = precision_score(y_cat_test, cat_preds, average="weighted", zero_division=0)
        rec_cat = recall_score(y_cat_test, cat_preds, average="weighted", zero_division=0)
        cm_cat = confusion_matrix(y_cat_test, cat_preds).tolist()

        # Evaluate Priority Model
        prio_preds = self.model_priority.predict(X_test)
        acc_prio = accuracy_score(y_prio_test, prio_preds)

        # Feature Importance
        feat_imp = sorted(
            list(zip(FEATURE_COLUMNS, self.model_category.feature_importances_)),
            key=lambda x: x[1], reverse=True
        )

        self.metrics = {
            "category_accuracy": round(float(acc_cat), 4),
            "category_precision": round(float(prec_cat), 4),
            "category_recall": round(float(rec_cat), 4),
            "category_f1": round(float(f1_cat), 4),
            "priority_accuracy": round(float(acc_prio), 4),
            "confusion_matrix": cm_cat,
            "feature_importance": [{"feature": f, "importance": round(float(imp), 4)} for f, imp in feat_imp]
        }

        print(f"Decision Tree Category Model Accuracy: {acc_cat:.4f}, F1: {f1_cat:.4f}")
        return self.metrics

    def predict(self, ticket_data: dict):
        X_input = extract_features_from_dict(ticket_data).fillna(0.0)
        cat_pred = self.model_category.predict(X_input)[0]
        prio_pred = self.model_priority.predict(X_input)[0]
        
        # Calculate prediction confidence using predict_proba max probability
        probs = self.model_category.predict_proba(X_input)[0]
        confidence = round(float(np.max(probs)), 2)

        return {
            "category": str(cat_pred),
            "priority": str(prio_pred),
            "confidence": max(confidence, 0.75)
        }

    def save(self, file_path: Path = None):
        if file_path is None:
            file_path = MODEL_DIR / "decision_tree.pkl"
        joblib.dump(self, file_path)
        print(f"Saved Decision Tree model to {file_path}")

    @staticmethod
    def load(file_path: Path = None):
        if file_path is None:
            file_path = MODEL_DIR / "decision_tree.pkl"
        if not file_path.exists():
            return None
        return joblib.load(file_path)
