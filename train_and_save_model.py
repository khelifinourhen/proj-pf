import joblib
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA  # Uncomment if PCA is needed
import pandas as pd
import os

# ====================
# 1. Load data
# ====================
# Update the path to your IoT CSV dataset
DATA_PATH = r"c:/Users/hp/Desktop/Proj pf/data/iot_dataset.csv"

df = pd.read_csv(DATA_PATH)
X = df.values

# ====================
# 2. Preprocessing
# ====================
imputer = SimpleImputer(strategy="median")
X_imp = imputer.fit_transform(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imp)

# Optional PCA (uncomment if used)
# pca = PCA(n_components=0.95, random_state=42)
# X_processed = pca.fit_transform(X_scaled)
X_processed = X_scaled

# ====================
# 3. Train Isolation Forest
# ====================
model = IsolationForest(
    n_estimators=200,
    max_samples="auto",
    contamination="auto",
    random_state=42,
)
model.fit(X_processed)

# ====================
# 4. Save model and preprocessing objects
# ====================
OUTPUT_DIR = r"c:/Users/hp/Desktop/Proj pf/model"
joblib.dump(model, f"{OUTPUT_DIR}/isolation_forest_model.joblib")

preprocess = {
    "imputer": imputer,
    "scaler": scaler,
    # "pca": pca,  # Uncomment if PCA is used
}
joblib.dump(preprocess, f"{OUTPUT_DIR}/preprocess_pipeline.joblib")

print("Model and preprocessing pipeline saved successfully to", OUTPUT_DIR)

# ====================
# 5. Test inference and save result
# ====================
# Use the first sample from the original dataframe for a quick test
X_sample = df.iloc[[0]]
X_imp = imputer.transform(X_sample)
X_sc = scaler.transform(X_imp)
# Compute anomaly score (IsolationForest returns higher scores for normal points)
score = -float(model.score_samples(X_sc)[0])
# Example threshold – you may replace this with your own saved config
threshold = 0.5
is_anomaly = score >= threshold
# Prepare result dictionary
inference_result = {
    "score": score,
    "threshold": threshold,
    "anomaly": is_anomaly,
    "sample_index": int(X_sample.index[0])
}
# Save the inference result to a joblib file in the same output directory
result_path = os.path.join(OUTPUT_DIR, "inference_result.joblib")
joblib.dump(inference_result, result_path)

print(f"Test inference: score={score:.4f} | seuil={threshold:.4f} | anomalie={is_anomaly}")
print("Inference result saved to", result_path)
