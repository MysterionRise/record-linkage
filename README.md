# Record Linkage - Modern ML Implementation

[![Backend CI](https://github.com/MysterionRise/record-linkage/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/MysterionRise/record-linkage/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/MysterionRise/record-linkage/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/MysterionRise/record-linkage/actions/workflows/frontend-ci.yml)
[![Docker Build](https://github.com/MysterionRise/record-linkage/actions/workflows/docker.yml/badge.svg)](https://github.com/MysterionRise/record-linkage/actions/workflows/docker.yml)
[![Integration Tests](https://github.com/MysterionRise/record-linkage/actions/workflows/integration.yml/badge.svg)](https://github.com/MysterionRise/record-linkage/actions/workflows/integration.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, ML-powered record linkage system with an interactive UI for demonstrating entity matching with explainability.

## Overview

Record linkage is the process of identifying pairs of records that refer to the same entity. This implementation uses state-of-the-art BERT-based transformers with SHAP/LIME explainability.

**Key Features:**
- BERT-based entity matching with confidence scores
- Interactive React UI with real-time matching
- SHAP and LIME explanations for interpretability
- Multiple pre-loaded datasets (UCI, DBLP-ACM, Walmart-Amazon)
- Batch processing capabilities

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for complete architecture details.

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download datasets
python ../scripts/download_datasets.py

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker (Recommended)

```bash
docker-compose up --build
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

## Architecture

```
record-linkage/
├── backend/          # FastAPI + ML pipeline
│   ├── app/
│   │   ├── api/     # REST API endpoints
│   │   ├── ml/      # BERT models, training, explainability
│   │   └── core/    # Configuration
├── frontend/         # React + TypeScript + Material-UI
│   └── src/
│       ├── components/  # UI components
│       ├── pages/       # Page views
│       └── services/    # API client
├── scripts/          # Dataset download & training
└── data/             # Datasets (raw & processed)
```

## Technology Stack

- **Backend**: FastAPI, PyTorch, Sentence Transformers, SHAP, LIME
- **Frontend**: React 18, TypeScript, Material-UI, Recharts
- **ML**: BERT-based entity matching with `sentence-transformers/all-MiniLM-L6-v2`

## Development

### Requirements
- **Python**: 3.12 or 3.13 (3.14 support coming soon)
- **Node.js**: 20+
- **Docker**: Latest version (optional but recommended)

### Testing
```bash
# Backend tests
cd backend
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend formatting and linting
cd backend
black app/
flake8 app/
mypy app/

# Frontend linting
cd frontend
npm run lint
```

See [CLAUDE.md](./CLAUDE.md) for detailed development guidelines and [.github/workflows/README.md](./.github/workflows/README.md) for CI/CD documentation.

## Background

Record linkage identifies which records in a dataset (or across datasets) refer to the same real-world entity. Common use cases:
- Deduplication (avoiding duplicate mailings)
- Patient tracking across hospital visits
- Cross-dataset entity resolution

**Entity Linking** is a subset focused on name-based matching (e.g., "John Kennedy" = "J. F. K" = "Джон Кеннеди").

## Resources

Academic papers and resources:
- http://www.bristol.ac.uk/media-library/sites/cmm/migrated/documents/problinkage.pdf
- https://arxiv.org/pdf/2003.04238.pdf
- https://cdn.oreillystatic.com/en/assets/1/event/290/New%20directions%20in%20record%20linkage%20Presentation.pdf
- http://axon.cs.byu.edu/~randy/pubs/wilson.ijcnn2011.beyondprl.pdf
- http://www2.stat.duke.edu/~rcs46/linkage/
- https://archive.ics.uci.edu/ml/datasets/Record+Linkage+Comparison+Patterns
- http://users.cecs.anu.edu.au/~Peter.Christen/Febrl/febrl-0.3/febrldoc-0.3/node6.html

## License

MIT 
