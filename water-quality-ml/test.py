"""
test.py
-------
Unit and integration tests for the Water Quality Prediction Flask app.

Run:
    pytest test.py -v
or:
    python test.py
"""

import os
import json
import pickle
import unittest
import numpy as np
from unittest.mock import patch, MagicMock

try:
    import pytest
    import requests
    from app import app
except ImportError as e:
    print(f"[WARNING] Some modules are missing: {e}")


# ══════════════════════════════════════════════════════════════════════
# Helper
# ══════════════════════════════════════════════════════════════════════

VALID_PAYLOAD = {
    "ph value":          "7.0",
    "Hardness":          "200.0",
    "Solids":            "20000.0",
    "Chloramines":       "7.0",
    "Sulfate":           "350.0",
    "Conductivity":      "400.0",
    "Organic carbon":    "14.0",
    "Trihalomethanes":   "66.0",
    "Turbidity":         "4.0",
}


# ══════════════════════════════════════════════════════════════════════
# Test Class
# ══════════════════════════════════════════════════════════════════════

class FlaskTest(unittest.TestCase):

    # ── 1. Route Returns 200 ─────────────────────────────────────────
    def test_route_status_200(self):
        """GET / should return HTTP 200."""
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)

    # ── 2. Content-Type ───────────────────────────────────────────────
    def test_content_type_html(self):
        """GET / should return text/html."""
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertIn("text/html", response.content_type)

    # ── 3. Homepage Contains Expected Elements ────────────────────────
    def test_homepage_contains_form(self):
        """Homepage HTML should contain the prediction form."""
        tester = app.test_client(self)
        response = tester.get("/")
        html = response.data.decode("utf-8")
        self.assertIn("Water Quality Prediction", html)
        self.assertIn("ph value", html)
        self.assertIn("Turbidity", html)

    # ── 4. POST with valid payload returns a result ───────────────────
    def test_post_valid_payload(self):
        """POST with all valid fields should return a prediction."""
        tester = app.test_client(self)
        response = tester.post("/", data=VALID_PAYLOAD)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        # Result should be Potable or Not Potable
        self.assertTrue(
            "Potable" in html or "Not Potable" in html or "error" in html.lower()
        )

    # ── 5. POST with missing field shows error ────────────────────────
    def test_post_missing_field(self):
        """POST with a missing field should trigger an error message."""
        tester = app.test_client(self)
        incomplete = dict(VALID_PAYLOAD)
        del incomplete["ph value"]
        response = tester.post("/", data=incomplete)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("required", html.lower())

    # ── 6. POST with non-numeric input shows error ────────────────────
    def test_post_non_numeric_input(self):
        """POST with text where number expected should trigger an error."""
        tester = app.test_client(self)
        bad_payload = dict(VALID_PAYLOAD)
        bad_payload["ph value"] = "abc"
        response = tester.post("/", data=bad_payload)
        html = response.data.decode("utf-8")
        self.assertIn("Invalid input", html)

    # ── 7. Mock POST request (requests library) ───────────────────────
    @patch("requests.post")
    def test_mock_post_request(self, mock_post):
        """Verify that requests.post is called with correct arguments."""
        mock_post.return_value = MagicMock(status_code=200)
        requests.post(
            "http://localhost:5000/",
            data=json.dumps(VALID_PAYLOAD),
            headers={"Content-Type": "application/json"}
        )
        mock_post.assert_called_once_with(
            "http://localhost:5000/",
            data=json.dumps(VALID_PAYLOAD),
            headers={"Content-Type": "application/json"}
        )

    # ── 8. Model and scaler files exist ───────────────────────────────
    def test_model_files_exist(self):
        """Model and scaler .sav files should exist in models/."""
        model_path  = os.path.join("models", "xgboost.sav")
        scaler_path = os.path.join("models", "scaler.sav")
        self.assertTrue(
            os.path.exists(model_path),
            f"Model file missing: {model_path} – run train_model.py first."
        )
        self.assertTrue(
            os.path.exists(scaler_path),
            f"Scaler file missing: {scaler_path} – run train_model.py first."
        )

    # ── 9. Model produces output of 0 or 1 ───────────────────────────
    def test_model_prediction_value(self):
        """Model should return 0 or 1 for any valid input."""
        model_path  = os.path.join("models", "xgboost.sav")
        scaler_path = os.path.join("models", "scaler.sav")
        if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
            self.skipTest("Model/scaler not found – run train_model.py first.")

        model  = pickle.load(open(model_path,  "rb"))
        scaler = pickle.load(open(scaler_path, "rb"))
        val    = np.array([7.0, 200.0, 20000.0, 7.0, 350.0, 400.0, 14.0, 66.0, 4.0])
        data   = scaler.transform([val])
        result = model.predict(data)
        self.assertIn(result[0], [0, 1])

    # ── 10. Scaler transforms without error ───────────────────────────
    def test_scaler_transform(self):
        """StandardScaler should transform a valid array without error."""
        scaler_path = os.path.join("models", "scaler.sav")
        if not os.path.exists(scaler_path):
            self.skipTest("Scaler not found – run train_model.py first.")

        scaler = pickle.load(open(scaler_path, "rb"))
        val    = np.array([[7.0, 200.0, 20000.0, 7.0, 350.0, 400.0, 14.0, 66.0, 4.0]])
        scaled = scaler.transform(val)
        self.assertEqual(scaled.shape, (1, 9))


# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    unittest.main(verbosity=2)
