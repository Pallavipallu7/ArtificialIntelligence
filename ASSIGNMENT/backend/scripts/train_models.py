import pandas as pd
from backend.config import DATA_DIR
from backend.learning.dataset_generator import generate_synthetic_dataset
from backend.learning.decision_tree import TicketDecisionTreeModel
from backend.learning.escalation_model import EscalationRiskModel

def train_all_models():
    csv_path = DATA_DIR / "historical_tickets.csv"
    if not csv_path.exists():
        print("Generating dataset first...")
        df = generate_synthetic_dataset(file_path=csv_path)
    else:
        df = pd.read_csv(csv_path)

    print("--- Training Decision Tree Model ---")
    dt_model = TicketDecisionTreeModel()
    dt_metrics = dt_model.train(df)
    dt_model.save()

    print("--- Training Escalation MLP Risk Model ---")
    esc_model = EscalationRiskModel()
    esc_metrics = esc_model.train(df)
    esc_model.save()

    print("All models trained and saved successfully.")
    return dt_metrics, esc_metrics

if __name__ == "__main__":
    train_all_models()
