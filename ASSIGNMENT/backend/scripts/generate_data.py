from backend.learning.dataset_generator import generate_synthetic_dataset

if __name__ == "__main__":
    print("Generating synthetic dataset for campus helpdesk...")
    df = generate_synthetic_dataset()
    print(f"Dataset generated successfully with {len(df)} records.")
