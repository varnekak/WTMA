"""
app.py
------
Flask web application for Water Quality Potability Prediction.
Loads a pre-trained XGBoost model and StandardScaler from the
models/ directory and exposes a single route for GET and POST.

Run:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# ── Paths ──────────────────────────────────────────────────────────────
MODEL_PATH  = os.path.join("models", "xgboost.sav")
SCALER_PATH = os.path.join("models", "scaler.sav")

# ── Feature order must match training ──────────────────────────────────
FEATURE_NAMES = [
    "ph", "Hardness", "Solids", "Chloramines",
    "Sulfate", "Conductivity", "Organic_carbon",
    "Trihalomethanes", "Turbidity"
]

# ── Form field names (as in index.html) ────────────────────────────────
FORM_FIELDS = [
    "ph value", "Hardness", "Solids", "Chloramines",
    "Sulfate", "Conductivity", "Organic carbon",
    "Trihalomethanes", "Turbidity"
]


def load_artifacts():
    """Load model and scaler from disk. Raises FileNotFoundError if missing."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at '{MODEL_PATH}'. "
            "Run train_model.py first."
        )
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(
            f"Scaler file not found at '{SCALER_PATH}'. "
            "Run train_model.py first."
        )
    model  = pickle.load(open(MODEL_PATH,  "rb"))
    scaler = pickle.load(open(SCALER_PATH, "rb"))
    return model, scaler


@app.route("/", methods=["GET", "POST"])
def home():
    result      = None
    error       = None
    input_vals  = {}          # echo values back to the form on POST

    if request.method == "POST":
        try:
            # ── Parse inputs ──────────────────────────────────────────
            raw = []
            for field in FORM_FIELDS:
                val = request.form.get(field, "").strip()
                if val == "":
                    raise ValueError(f"Field '{field}' is required.")
                raw.append(float(val))
                input_vals[field] = val

            val_array = np.array(raw)

            # ── Load model & scaler ───────────────────────────────────
            model, scaler = load_artifacts()

            # ── Scale then predict ────────────────────────────────────
            data = scaler.transform([val_array])
            pred = model.predict(data)[0]

            result = "Potable ✅" if pred == 1 else "Not Potable ❌"

        except ValueError as ve:
            error = f"Invalid input: {ve}"
        except FileNotFoundError as fe:
            error = str(fe)
        except Exception as ex:
            error = f"An unexpected error occurred: {ex}"

    return render_template(
        "index.html",
        result=result,
        error=error,
        input_vals=input_vals,
        zip=zip,
        form_fields=FORM_FIELDS,
    )


if __name__ == "__main__":
    app.run(debug=True)
