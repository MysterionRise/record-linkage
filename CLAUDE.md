# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository focuses on **record linkage** - the process of identifying pairs of records that refer to the same entity (typically people) across datasets. It includes research, documentation, and planned implementations of various approaches to this problem.

### Key Concepts

**Record Linkage**: Identifying which records in a dataset (or across multiple datasets) refer to the same real-world entity. Common use cases:
- Deduplication (avoiding sending mail to the same person multiple times)
- Patient tracking across hospital visits
- Cross-dataset entity resolution

**Entity Linking**: A subset of record linkage focused specifically on linking entities based on their names (e.g., "John Kennedy", "J. F. K", "Джон Кеннеди" as the same person).

## Implementation Approach

The repository implements a **modern, ML-powered record linkage system** with an interactive UI for demonstrating entity matching with explainability.

### Architecture

**Three-tier system**:
- **Frontend**: React 18+ with TypeScript, Material-UI/Ant Design
- **Backend**: FastAPI (Python async web framework)
- **ML Pipeline**: BERT-based entity matching with SHAP explainability

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for complete architecture details.

## Technology Stack

### Backend (Python)
- **Framework**: FastAPI with Pydantic v2 for validation
- **ML Libraries**:
  - `transformers` - Hugging Face transformers library
  - `sentence-transformers` - For BERT-based embeddings
  - `torch` - PyTorch 2.x
  - `shap` - Model explainability
- **Data**: pandas, numpy, scikit-learn, recordlinkage

### Frontend (TypeScript)
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Visualization**: D3.js or Recharts for match confidence
- **State**: React Query + Zustand

### Datasets
Primary datasets for development and demo:
1. **UCI Record Linkage Comparison Patterns** (~574K pairs) - benchmark dataset
2. **DBLP-ACM** - academic publications (clean data)
3. **DBLP-Scholar (Dirty)** - same with data quality issues
4. **Walmart-Amazon** - e-commerce product matching (~10K pairs)

## Development Commands

### Backend Setup and Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Train model
python scripts/train_model.py --dataset uci --epochs 10

# Run tests
pytest tests/ -v

# Code quality
black app/
flake8 app/
mypy app/
```

### Frontend Setup and Development
```bash
cd frontend
npm install

# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Linting
npm run lint
```

### Docker
```bash
# Build and run entire stack
docker-compose up --build

# Run specific service
docker-compose up backend
docker-compose up frontend
```

## Key Implementation Details

### BERT-based Entity Matching
The system uses sentence-transformers with a Siamese network architecture:
1. Serialize record pairs into text format
2. Generate embeddings using pre-trained BERT
3. Compute similarity (cosine/dot product)
4. Fine-tune on labeled dataset for domain adaptation

**Model**: `sentence-transformers/all-MiniLM-L6-v2` (lightweight) or `ditto-bert-base`

### Explainability
**SHAP**: Token-level attribution showing why records matched
- Force plots for individual predictions
- Feature importance aggregated by field
- UI shows highlighted tokens (green = match evidence, red = no-match)
- Top contributing features with detailed breakdowns

### File Structure
```
record-linkage/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── ml/       # ML models and training
│   │   └── core/     # Configuration
│   └── tests/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   └── services/
├── notebooks/         # Jupyter notebooks for experiments
├── scripts/          # Utility scripts
└── data/             # Datasets
```

## ML Approach

**Approach**: BERT-based entity matching (state-of-the-art as of 2024-2025)
- Pre-trained language models fine-tuned on record pairs
- Contrastive learning or binary classification
- Training metrics: Precision, Recall, F1-score, ROC-AUC
- Inference: < 200ms per pair, SHAP explanations in < 500ms

**Training Pipeline**: See `backend/app/ml/training.py`
**Inference Pipeline**: See `backend/app/ml/inference.py`
**SHAP Explainability**: See `backend/app/ml/explainability.py`

## Development Notes

- **API Documentation**: Auto-generated at `http://localhost:8000/docs` (Swagger UI)
- **Model Files**: Saved in `backend/models/` directory
- **Datasets**: Downloaded via `scripts/download_datasets.py`
- **Notebooks**: Use for experimentation before integrating into main codebase
- **Code Style**:
  - Python: Black formatter, type hints required
  - TypeScript: ESLint + Prettier
- **Testing**: Write tests for all ML pipeline components

## UI Features

1. **Dataset Selection**: Upload CSV or select from pre-loaded datasets
2. **Record Comparison**: Side-by-side view with match probability
3. **Explainability Dashboard**: Interactive SHAP visualizations
4. **Batch Processing**: Upload two datasets for deduplication
5. **Analytics**: Precision/recall metrics, confidence distributions

## Key Resources

Academic foundations (see README.md for full list):
- "Deep Learning for Entity Matching: A Design Space Exploration" (2018)
- "Dual-Objective Fine-Tuning of BERT for Entity Matching" (VLDB 2021)
- "Analyzing How BERT Performs Entity Matching" (VLDB 2022)
- UCI Machine Learning Repository: Record Linkage datasets

Modern approaches:
- BERT-based entity matching (replacing traditional text/graph methods)
- Transformer architectures for contextualized embeddings
- SHAP for model interpretability
