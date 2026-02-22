- NITESH KUMAR ----- 2024AA05143 ----- 100%
- LAWLESH KUMAR ----- 2024AA05149 ----- 100%
- VAIBHAV SAREEN ----- 2024AA05923 ----- 100%
- VIVEK TRIVEDI ----- 2024AA05922 ----- 100%
- BINDU MANOJ ----- 2024AA05979 ----- 100%




# MLOps Assignment 2 - Cat vs Dog Image Classifier API

A production-ready machine learning inference service for classifying cat and dog images, built with FastAPI and PyTorch. The project includes comprehensive MLOps practices including containerization, monitoring, testing, and CI/CD readiness.


## 🎯 Overview

This project implements a complete MLOps pipeline for image classification:

- **Machine Learning**: CNN model trained on cat vs dog dataset using PyTorch
- **API Service**: FastAPI-based REST API for real-time inference
- **Monitoring**: Prometheus metrics collection and Grafana visualization
- **Containerization**: Docker and Docker Compose for easy deployment
- **Testing**: Comprehensive unit and integration tests with pytest
- **Experiment Tracking**: MLflow for model versioning and experiment tracking
- **Data Versioning**: DVC (Data Version Control) for dataset management


---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  FastAPI     │─────▶│  PyTorch    │
│  (Browser)  │      │   Service    │      │   Model     │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Prometheus  │
                     │   Metrics    │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Grafana    │
                     │  Dashboard   │
                     └──────────────┘
```

---

## 📁 Project Structure

```
bitsMtech_MLOps_Assignment_2/
├── app/                              # Main application package
│   ├── __init__.py
│   ├── main.py                       # FastAPI application entry point
│   ├── api/
│   │   └── routes.py                 # API route definitions
│   ├── core/
│   │   └── config.py                 # Configuration settings
│   ├── models/
│   │   └── model.py                  # Model architecture definition
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── prediction.py             # Pydantic schemas
│   └── services/
│       └── inference.py              # Inference logic
│
├── artifacts/                        # Trained model files
│   ├── cnn_model_full.pt             # Complete model with architecture
│   └── cnn_model.pt                  # Model weights only
│
├── DataFiles/                        # Dataset storage (DVC managed)
│   ├── train/                        # Training images
│   ├── test/                         # Test images
│   └── sample_submission.csv
│
├── tests/                            # Test suite
│   ├── conftest.py                   # Pytest configuration
│   ├── test_smoke.py                 # Smoke tests
│   ├── test_deployment.py            # Deployment tests
│   └── run_smoke_tests.sh            # Test execution script
│
├── grafana/                          # Grafana configuration
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml        # Prometheus datasource config
│       └── dashboards/
│           └── dashboard.yml         # Dashboard provisioning
│
├── logs/                             # Application logs
│   └── prometheus/                   # Prometheus logs
│
├── mlruns/                           # MLflow experiment tracking
│
├── htmlcov/                          # Test coverage reports
│
├── dataExploration.ipynb             # EDA notebook
├── modelTraining.ipynb               # Model training notebook
├── docker-compose.yml                # Multi-container Docker setup
├── Dockerfile                        # API service container definition
├── prometheus.yml                    # Prometheus configuration
├── requirements.txt                  # Full Python dependencies
├── requirements_fastapi.txt          # API-only dependencies
├── pytest.ini                        # Pytest configuration
├── coverage.xml                      # Code coverage report
├── DataFiles.dvc                     # DVC data tracking
└── README.md                         # This file
```

