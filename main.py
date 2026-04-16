from src.preprocess import build_combined_dataset
from src.features import extract_features
from src.train_model import train_and_evaluate
import joblib


def main():
    df = build_combined_dataset(
        rockyou_path="data/rockyou.txt",
        strong_path="data/strong.txt",
        rockyou_sample=50000,
        strong_sample=20000
    )

    print("Combined dataset shape:", df.shape)
    print("\nClass distribution:")
    print(df["label"].value_counts())

    featured_df = extract_features(df)

    print("\nSample rows:")
    print(featured_df.head())

    rf_model, lr_model = train_and_evaluate(featured_df)

    joblib.dump(rf_model, "model_rf_v1.pkl")
    joblib.dump(lr_model, "model_lr_v1.pkl")

    print("\nModels saved successfully:")
    print("- model_rf_v1.pkl")
    print("- model_lr_v1.pkl")


if __name__ == "__main__":
    main()