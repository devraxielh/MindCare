import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from django.conf import settings

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'core', 'ml_models', 'model.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, 'core', 'ml_models', 'encoders.pkl')
DATASET_PATH = os.path.join(os.path.dirname(BASE_DIR), 'Mental Health Dataset.csv')

def train_model():
    print(f"Loading dataset from {DATASET_PATH}...")
    if not os.path.exists(DATASET_PATH):
        print("Dataset not found!")
        return

    df = pd.read_csv(DATASET_PATH)
    
    # Drops
    # Timestamp is irrelevant
    drop_cols = ['Timestamp']
    # If other columns are IDs or names, drop them.
    # The dataset seems to have only categorical features + Country (which is high cardinality potentially)
    
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    # Handle missing values
    df = df.fillna('Missing')
    
    # Target
    target_col = 'treatment'
    if target_col not in df.columns:
        print("Target column 'treatment' not found.")
        return

    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Encoders
    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        # Ensure 'Missing' is handled if it appears in future data by fitting on string conversion
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
        
    # Encode target
    le_target = LabelEncoder()
    y = le_target.fit_transform(y.astype(str))
    encoders['target'] = le_target
    
    # Train
    print("Training model...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    # Save
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(encoders, ENCODERS_PATH)
    print(f"Model saved to {MODEL_PATH}")

def predict_treatment(data_dict):
    """
    data_dict: dict containing values for all features.
    Returns: "Yes" or "No" (or whatever the target classes are)
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODERS_PATH):
        return "Error: Model not trained"
        
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    
    input_data = []
    # Order must match training columns
    # We obtain columns from the encoders keys (excluding 'target')
    # Note: dict keys order is preserved in Python 3.7+, but safest to rely on feature names if we had saved them.
    # Here we assume the input dictionary has all keys.
    
    feature_cols = [c for c in encoders.keys() if c != 'target']
    
    row = []
    for col in feature_cols:
        val = data_dict.get(col)
        le = encoders[col]
        try:
            val_enc = le.transform([str(val)])[0]
        except ValueError:
            # Handle unseen label - assign to most common or just -1 if model handles it?
            # RF doesn't handle -1 well usually unless ordinal.
            # We'll try to map to the first class or a 'Missing' class if it existed.
            # Simple fallback: use the first class
            val_enc = 0 
        row.append(val_enc)
        
    prediction_idx = model.predict([row])[0]
    prediction_label = encoders['target'].inverse_transform([prediction_idx])[0]
    return prediction_label

if __name__ == "__main__":
    train_model()
