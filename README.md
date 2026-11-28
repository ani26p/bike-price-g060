# MP295 - Used Two-Wheeler Price (Dehradun)

**Course:** SCSE3040 MLOps (Mini Project)
**Group ID:** G060
**Problem ID:** MP295
**Faculty:** Avantika Saklani | **Batch:** 90

## Team members

| Name | Enrolment No. | GitHub username |
|---|---|---|
| Vaishnavi Tyagi | S24CSEU0142 | vtyagi-22 |
| Aniket Pandit | S24CSEU1574 | ani26p |
| Vivan Rawat | S24CSEU1259 | lowkeydumb |
| Parija Sharma Rajni Jangra | S24CSEU1826 | ParijaSharma |

## Project summary

The Dehradun Second-Hand Bike Market wants a fair price estimate for each used
two-wheeler. This project predicts `resale_thousand_rs` (price in thousand
rupees) from age, km driven, engine size, owners, service records, accidents,
brand tier and city zone. It is a regression problem scored with MAE.

The repo contains the full MLOps pipeline: DVC data versioning, data cleaning,
MLflow tracking and registry, a FastAPI service, Docker, GitHub Actions CI,
Kubernetes files, JSON logging, drift monitoring (PSI) and retraining.

## Repository structure

- `src/bikeprice/` - data checks, cleaning, training, monitoring code
- `tests/` - pytest tests
- `app/main.py` - FastAPI service (`POST /predict`, `GET /health`)
- `models/model.joblib` - champion model loaded by the API
- `data/raw/` - DVC-tracked data files
- `k8s/` - Kubernetes deployment and service files
- `reports/findings.yaml` - data issues, tracking and monitoring results
- `predictions/holdout_predictions.csv` - final predictions
- `params.yaml` - paths and model settings
- `mlflow.db` - MLflow tracking database

## Setup

```bash
git clone https://github.com/<owner>/bike-price-g060.git
cd bike-price-g060
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
dvc pull                         # fetches the data files
```

## How to run

```bash
pytest                                       # run tests
uvicorn app.main:app --port 8000             # start the API
docker build -t mp295-api:1.0 .              # build the image
```

## Team contributions

- **Member 1 (name):** <what they built>
- **Member 2 (name):** <what they built>
- **Member 3 (name):** <what they built>
- **Member 4 (name):** <what they built>
