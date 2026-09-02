"""
Tests de l API FastAPI - Detection Anomalies IoT
Usage : pytest tests/test_api.py -v
"""
import pytest
import sys
import json
import numpy as np
from pathlib import Path

# Ajout du chemin pour l import
sys.path.insert(0, str(Path(__file__).parent.parent))

# ─────────────────────────────────────────────────────────
# On utilise TestClient de FastAPI (pas besoin de serveur)
# ─────────────────────────────────────────────────────────
try:
    from fastapi.testclient import TestClient
    from api.app import app
    client = TestClient(app)
    HAS_FASTAPI = True
except Exception:
    HAS_FASTAPI = False


# ─────────────────────────────────────────────────────────
# DONNEES DE TEST
# ─────────────────────────────────────────────────────────
SCENARIO_NORMAL = {
    "temperature_c": 24.5, "pressure_hpa": 1013.0,
    "humidity_pct": 52.0, "altitude_m": 3000.0,
    "airspeed_kts": 250.0, "vibration_norm_ms2": 0.12,
    "voltage_v": 3.3, "current_a": 0.85, "power_w": 2.8,
    "rpm": 1450.0, "operating_hours": 1200.0,
    "load_pct": 55.0, "motor_current_temp_c": 45.0,
    "wifi_rssi_dbm": -65.0, "packet_latency_ms": 12.0
}

SCENARIO_LIMITE = {
    "temperature_c": 68.0, "pressure_hpa": 980.0,
    "humidity_pct": 88.0, "altitude_m": 9500.0,
    "vibration_norm_ms2": 1.8, "voltage_v": 3.1,
    "rpm": 2800.0, "operating_hours": 4800.0, "load_pct": 89.0
}

SCENARIO_ANOMALIE = {
    "temperature_c": 142.0, "pressure_hpa": 650.0,
    "vibration_norm_ms2": 15.3, "voltage_v": 2.4,
    "current_a": 4.8, "power_w": 11.5,
    "rpm": 5500.0, "operating_hours": 8900.0,
    "motor_current_temp_c": 148.0
}


# ─────────────────────────────────────────────────────────
# TESTS UNITAIRES
# ─────────────────────────────────────────────────────────

@pytest.mark.skipif(not HAS_FASTAPI, reason="FastAPI non disponible")
class TestHealthEndpoint:
    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_has_status_ok(self):
        resp = client.get("/health")
        data = resp.json()
        assert data["status"] == "ok"

    def test_health_model_loaded(self):
        resp = client.get("/health")
        data = resp.json()
        assert data["model_loaded"] is True


@pytest.mark.skipif(not HAS_FASTAPI, reason="FastAPI non disponible")
class TestInfoEndpoint:
    def test_info_returns_model_name(self):
        resp = client.get("/info")
        assert resp.status_code == 200
        data = resp.json()
        assert data["model"] == "IsolationForest"

    def test_info_has_features(self):
        resp = client.get("/info")
        data = resp.json()
        assert "features" in data
        assert len(data["features"]) == 24

    def test_info_has_threshold(self):
        resp = client.get("/info")
        data = resp.json()
        assert "threshold" in data
        assert isinstance(data["threshold"], float)


@pytest.mark.skipif(not HAS_FASTAPI, reason="FastAPI non disponible")
class TestPredictEndpoint:
    def test_predict_returns_200(self):
        resp = client.post("/predict", json=SCENARIO_NORMAL)
        assert resp.status_code == 200

    def test_predict_scenario_normal(self):
        resp = client.post("/predict", json=SCENARIO_NORMAL)
        data = resp.json()
        assert data["anomaly"] in [0, 1]
        assert data["status"] in ["NORMAL", "ANOMALY"]
        assert isinstance(data["anomaly_score"], float)
        assert data["model"] == "IsolationForest"
        print(f"\n  Scenario NORMAL  : score={data['anomaly_score']:.4f} status={data['status']}")

    def test_predict_scenario_limite(self):
        resp = client.post("/predict", json=SCENARIO_LIMITE)
        data = resp.json()
        assert resp.status_code == 200
        assert data["anomaly"] in [0, 1]
        print(f"\n  Scenario LIMITE  : score={data['anomaly_score']:.4f} status={data['status']}")

    def test_predict_scenario_anomalie(self):
        resp = client.post("/predict", json=SCENARIO_ANOMALIE)
        data = resp.json()
        assert resp.status_code == 200
        assert data["anomaly"] in [0, 1]
        print(f"\n  Scenario ANOMALIE: score={data['anomaly_score']:.4f} status={data['status']}")

    def test_predict_empty_payload(self):
        # Payload vide - le modele doit gerer les NaN via imputer
        resp = client.post("/predict", json={})
        # L API doit repondre 200 (imputer gere les NaN) ou 422 (validation Pydantic)
        assert resp.status_code in [200, 422]

    def test_predict_response_has_all_fields(self):
        resp = client.post("/predict", json=SCENARIO_NORMAL)
        data = resp.json()
        required_fields = ["anomaly", "anomaly_score", "status", "model", "threshold", "timestamp"]
        for field in required_fields:
            assert field in data, f"Champ manquant: {field}"

    def test_predict_anomaly_is_int(self):
        resp = client.post("/predict", json=SCENARIO_NORMAL)
        data = resp.json()
        assert isinstance(data["anomaly"], int)
        assert data["anomaly"] in [0, 1]


@pytest.mark.skipif(not HAS_FASTAPI, reason="FastAPI non disponible")
class TestBatchEndpoint:
    def test_batch_multiple_readings(self):
        batch = {
            "readings": [SCENARIO_NORMAL, SCENARIO_LIMITE, SCENARIO_ANOMALIE]
        }
        resp = client.post("/predict/batch", json=batch)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert len(data["predictions"]) == 3

    def test_batch_empty_returns_error(self):
        resp = client.post("/predict/batch", json={"readings": []})
        assert resp.status_code == 400


@pytest.mark.skipif(not HAS_FASTAPI, reason="FastAPI non disponible")
class TestScenariosEndpoint:
    def test_scenarios_endpoint(self):
        resp = client.get("/scenarios")
        assert resp.status_code == 200
        data = resp.json()
        assert "scenario_1_nominal" in data
        assert "scenario_2_limite" in data
        assert "scenario_3_anomalie" in data


# ─────────────────────────────────────────────────────────
# TEST STANDALONE (sans FastAPI)
# ─────────────────────────────────────────────────────────
class TestModelStandalone:
    """Tests qui fonctionnent meme sans serveur FastAPI."""

    def test_model_pipeline_exists(self):
        model_path = Path(__file__).parent.parent / "model" / "model_pipeline.joblib"
        assert model_path.exists(), f"model_pipeline.joblib introuvable: {model_path}"

    def test_metadata_exists(self):
        meta_path = Path(__file__).parent.parent / "model" / "metadata.json"
        assert meta_path.exists()

    def test_metadata_valid(self):
        meta_path = Path(__file__).parent.parent / "model" / "metadata.json"
        if meta_path.exists():
            with open(meta_path) as f:
                meta = json.load(f)
            assert meta["model"] == "IsolationForest"
            assert len(meta["features"]) == 24
            assert "threshold" in meta

    def test_model_loads_and_predicts(self):
        import joblib
        model_path = Path(__file__).parent.parent / "model" / "model_pipeline.joblib"
        cfg_path   = Path(__file__).parent.parent / "model" / "if_config.joblib"
        if not model_path.exists():
            pytest.skip("model_pipeline.joblib absent")
        pipeline = joblib.load(model_path)
        cfg      = joblib.load(cfg_path)
        import pandas as pd
        X = pd.DataFrame([SCENARIO_NORMAL])
        score = -float(pipeline.score_samples(X)[0])
        assert isinstance(score, float)
        assert 0.0 <= score <= 5.0, f"Score hors plage: {score}"
        print(f"\n  Score standalone test: {score:.4f} (seuil={cfg['threshold']:.4f})")


if __name__ == "__main__":
    import subprocess
    subprocess.run(["pytest", __file__, "-v", "--tb=short"], check=False)
