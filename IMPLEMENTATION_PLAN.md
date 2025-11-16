# Modern Record Linkage Implementation Plan

## Overview
A modern, ML-powered record linkage system with interactive UI for demonstrating entity matching with explainability.

---

## System Architecture

### Three-Tier Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (React)                │
│  - Match Visualization                  │
│  - Dataset Upload/Selection             │
│  - Explainability Dashboard             │
│  - Confidence Score Display             │
└────────────────┬────────────────────────┘
                 │ REST API
┌────────────────▼────────────────────────┐
│       Backend (FastAPI/Python)          │
│  - API Endpoints                        │
│  - Business Logic                       │
│  - Data Preprocessing                   │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         ML Pipeline Layer               │
│  - BERT-based Entity Matching           │
│  - Model Training/Inference             │
│  - SHAP Explainability                  │
│  - Feature Engineering                  │
└─────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **UI Library**: Material-UI (MUI) or Ant Design
- **Visualization**:
  - D3.js or Recharts for match confidence visualization
  - Custom components for explainability (SHAP force plots, feature importance)
- **State Management**: React Query + Zustand
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (async Python web framework)
- **API Documentation**: Auto-generated OpenAPI/Swagger
- **Data Validation**: Pydantic v2
- **CORS**: For React development server

### ML/AI Stack
- **Core**: PyTorch 2.x
- **Transformers**: Hugging Face `transformers` library
- **Pre-trained Models**:
  - `sentence-transformers/all-MiniLM-L6-v2` (lightweight, fast)
  - `ditto-bert-base` or fine-tuned BERT models
- **Explainability**:
  - `shap` - SHapley Additive exPlanations
  - `transformers-interpret` - BERT-specific interpretability (optional)
- **Data Processing**: pandas, numpy, scikit-learn
- **Record Linkage**: `recordlinkage` library (traditional methods baseline)

### Data Storage
- **Development**: SQLite or JSON files
- **Production-ready**: PostgreSQL with vector extensions (pgvector)
- **Caching**: Redis (optional, for model predictions)

### Deployment
- **Backend**: Docker container with FastAPI + uvicorn
- **Frontend**: Nginx or served via CDN
- **Model Serving**: Separate service or integrated with backend

---

## Datasets for Demo

### Primary Datasets (Recommended)

1. **UCI Record Linkage Comparison Patterns**
   - Source: https://archive.ics.uci.edu/ml/datasets/record+linkage+comparison+patterns
   - Type: Personal data comparisons
   - Size: ~574,000 record pairs
   - Features: 12 comparison patterns
   - Use case: Classic benchmark for record linkage

2. **DBLP-ACM (Academic Publications)**
   - Type: Bibliographic data from two databases
   - Size: ~2,600 records from DBLP, ~2,300 from ACM
   - Fields: Title, authors, venue, year
   - Use case: Clean, structured data - good for initial demo

3. **DBLP-Scholar (Dirty)**
   - Type: Same as above but with data quality issues
   - Use case: Demonstrates robustness to real-world data issues

4. **Walmart-Amazon Product Matching**
   - Type: E-commerce product data
   - Size: ~10,000+ product pairs
   - Fields: Title, description, brand, price, category
   - Use case: Real-world commercial application demo

### Secondary/Alternative Datasets

5. **Abt-Buy (Products)**
   - Type: Product specifications from two retailers
   - Size: ~1,000+ records each
   - Use case: Smaller dataset for quick demonstrations

6. **Restaurant Data (Fodors-Zagat)**
   - Type: Restaurant information
   - Fields: Name, address, city, cuisine type, phone
   - Use case: Geographic/location-based matching

---

## ML Approach: BERT-based Entity Matching

### Model Architecture

**Option 1: Sentence-BERT Siamese Network** (Recommended for Demo)
```python
# Pseudo-architecture
Input: [Record A fields] [SEP] [Record B fields]
  ↓
BERT Encoder (sentence-transformers)
  ↓
Pooling Layer (mean/CLS token)
  ↓
Similarity Computation (cosine/dot product)
  ↓
Classification Layer (match/no-match)
  ↓
Output: Match probability + confidence score
```

**Option 2: Ditto-style Approach**
- Domain knowledge injection
- Data augmentation
- Dual-objective training (matching + attribute-specific classification)

### Training Strategy

1. **Pre-trained Model**: Start with `sentence-transformers/all-MiniLM-L6-v2`
2. **Fine-tuning**:
   - Train on labeled pairs from dataset
   - Use contrastive learning or binary classification
   - 80/10/10 train/validation/test split
3. **Evaluation Metrics**:
   - Precision, Recall, F1-score
   - Precision-Recall curves
   - ROC-AUC

### Inference Pipeline

```python
# Simplified pipeline
def predict_match(record_a, record_b):
    # 1. Preprocess records
    text_a = serialize_record(record_a)
    text_b = serialize_record(record_b)

    # 2. Generate embeddings
    embedding_a = model.encode(text_a)
    embedding_b = model.encode(text_b)

    # 3. Compute similarity
    similarity = cosine_similarity(embedding_a, embedding_b)

    # 4. Generate explanations
    shap_values = explainer(text_a, text_b)

    # 5. Return results
    return {
        'match_probability': similarity,
        'is_match': similarity > threshold,
        'explanations': shap_values,
        'feature_contributions': extract_features(shap_values)
    }
```

---

## Explainability Integration

### SHAP (Primary Method)

**Implementation**:
```python
import shap
from transformers import AutoTokenizer, AutoModel

# Create explainer for BERT model
explainer = shap.Explainer(model, tokenizer)

# Generate explanations for a prediction
shap_values = explainer([text_pair])

# Visualizations:
# - Force plot: Show contribution of each token
# - Waterfall plot: Feature importance
# - Summary plot: Overall feature importance across dataset
```

**UI Display**:
- Token-level highlighting (red = push towards no-match, green = push towards match)
- Feature importance bar charts
- Interactive exploration of why pairs matched/didn't match
- Top contributing features

### Custom Explainability Features

1. **Field-level Attribution**:
   - Show which specific fields (name, address, etc.) contributed most
   - Aggregate token-level SHAP values by field

2. **Example-based Explanations**:
   - Show similar pairs from training data
   - "This pair is like these 5 known matches..."

3. **Confidence Calibration**:
   - Display model uncertainty
   - Flag low-confidence predictions for human review

---

## UI/UX Design

### Main Views

#### 1. Dataset Selection View
- Upload custom CSV or select from pre-loaded datasets
- Preview data schema and sample records
- Data quality statistics

#### 2. Matching View
```
┌────────────────────────────────────────────────┐
│  Record Pair Comparison                        │
│                                                │
│  Record A               Record B               │
│  ┌─────────────┐      ┌─────────────┐         │
│  │ Name: John  │      │ Name: J.    │         │
│  │ Smith       │      │ Smith       │         │
│  │             │      │             │         │
│  │ Address:    │      │ Address:    │         │
│  │ 123 Main St │      │ 123 Main    │         │
│  └─────────────┘      └─────────────┘         │
│                                                │
│  Match Probability: 87.3%  [████████░░]        │
│  Confidence: High                              │
│                                                │
│  [View Explanation] [Mark as Correct/Wrong]    │
└────────────────────────────────────────────────┘
```

#### 3. Explainability Dashboard
- SHAP force plots showing token contributions
- Feature importance charts
- Field-by-field comparison with similarity scores
- Interactive: hover over tokens to see contribution values

#### 4. Results Analytics
- Overall matching statistics
- Precision/Recall metrics
- Distribution of confidence scores
- Confusion matrix (if ground truth available)

#### 5. Batch Processing View
- Upload two datasets for deduplication
- Progress tracking
- Export results (CSV, JSON)
- Filter by confidence threshold

### Key Features

- **Real-time Matching**: Type/paste records and see instant results
- **Interactive Explanations**: Click on features to see their impact
- **Comparison Mode**: Side-by-side record comparison with highlighting
- **Feedback Loop**: User can mark predictions as correct/incorrect
- **Export**: Download matching results and explanations

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Set up project structure (monorepo or separate repos)
- [ ] Initialize FastAPI backend with basic endpoints
- [ ] Initialize React frontend with routing
- [ ] Download and prepare UCI dataset
- [ ] Create database schema for storing records and predictions

### Phase 2: ML Pipeline (Week 2-3)
- [ ] Implement data preprocessing pipeline
- [ ] Load pre-trained sentence-transformer model
- [ ] Create basic matching function (cosine similarity)
- [ ] Implement training pipeline for fine-tuning
- [ ] Train baseline model on UCI dataset
- [ ] Evaluate and save best model

### Phase 3: Core Matching Features (Week 3-4)
- [ ] Implement match prediction API endpoint
- [ ] Create batch processing endpoint
- [ ] Build record comparison UI component
- [ ] Implement match results display with confidence scores
- [ ] Add dataset selection/upload functionality

### Phase 4: Explainability (Week 4-5)
- [ ] Integrate SHAP for model explanations
- [ ] Create custom field-level attribution
- [ ] Build explainability visualization components
- [ ] Add interactive explanation features to UI

### Phase 5: Polish & Demo Features (Week 5-6)
- [ ] Build analytics dashboard
- [ ] Add example datasets with descriptions
- [ ] Implement result export functionality
- [ ] Create guided tour/tutorial for users
- [ ] Performance optimization
- [ ] Responsive design for mobile

### Phase 6: Deployment (Week 6-7)
- [ ] Dockerize application
- [ ] Set up CI/CD pipeline
- [ ] Deploy to cloud platform (Heroku, Railway, or AWS)
- [ ] Add monitoring and logging
- [ ] Create demo video and documentation

---

## File Structure

```
record-linkage/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── matching.py     # Matching endpoints
│   │   │   │   ├── datasets.py     # Dataset management
│   │   │   │   └── explanations.py # Explainability endpoints
│   │   ├── core/
│   │   │   ├── config.py           # Configuration
│   │   │   └── security.py         # Security settings
│   │   ├── models/
│   │   │   ├── schemas.py          # Pydantic models
│   │   │   └── database.py         # Database models
│   │   ├── ml/
│   │   │   ├── model.py            # BERT model wrapper
│   │   │   ├── preprocessing.py    # Data preprocessing
│   │   │   ├── training.py         # Training pipeline
│   │   │   ├── inference.py        # Inference pipeline
│   │   │   └── explainability.py   # SHAP/LIME integration
│   │   └── utils/
│   │       ├── data_loader.py      # Dataset utilities
│   │       └── metrics.py          # Evaluation metrics
│   ├── tests/
│   ├── models/                     # Saved ML models
│   ├── data/                       # Datasets
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── RecordComparison.tsx
│   │   │   ├── ExplanationView.tsx
│   │   │   ├── MatchResults.tsx
│   │   │   ├── DatasetSelector.tsx
│   │   │   └── Analytics.tsx
│   │   ├── hooks/
│   │   │   └── useMatching.ts      # API integration
│   │   ├── services/
│   │   │   └── api.ts              # API client
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript types
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── notebooks/                      # Jupyter notebooks for experiments
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_explainability_analysis.ipynb
│
├── scripts/
│   ├── download_datasets.py
│   ├── train_model.py
│   └── evaluate_model.py
│
├── docker-compose.yml
├── .gitignore
├── README.md
├── CLAUDE.md
└── IMPLEMENTATION_PLAN.md          # This file
```

---

## Key Development Commands

### Backend

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Training
python scripts/train_model.py --dataset uci --epochs 10

# Testing
pytest tests/ -v

# Linting
black app/
flake8 app/
mypy app/
```

### Frontend

```bash
# Setup
cd frontend
npm install

# Development
npm run dev

# Build
npm run build

# Testing
npm test

# Linting
npm run lint
```

### Docker

```bash
# Build and run entire stack
docker-compose up --build

# Run backend only
docker-compose up backend

# Run frontend only
docker-compose up frontend
```

---

## Success Metrics

### Technical Metrics
- **Accuracy**: F1-score > 0.90 on UCI test set
- **Latency**: < 200ms per pair prediction
- **Explainability**: SHAP values computed in < 500ms

### User Experience Metrics
- **Intuitiveness**: Users can understand why records matched
- **Interactive**: Real-time feedback on record pairs
- **Visual Clarity**: Clear visualization of match confidence

### Demo Impact
- **Wow Factor**: Impressive explainability visualizations
- **Practical Value**: Demonstrates real-world applicability
- **Technical Depth**: Shows modern ML techniques

---

## Future Enhancements

### Advanced Features
1. **Active Learning**: Let users correct predictions to improve model
2. **Multi-language Support**: Cross-lingual entity matching
3. **Fuzzy Matching**: Enhanced string similarity algorithms
4. **Graph-based Linking**: Use entity relationships for better matching
5. **Automated Threshold Selection**: ROC curve analysis for optimal cutoff

### Scalability
1. **Vector Database**: Use Pinecone/Milvus for large-scale similarity search
2. **Async Processing**: Queue-based batch processing for millions of records
3. **Model Versioning**: MLflow for experiment tracking
4. **A/B Testing**: Compare different model approaches

### Integration
1. **API-first Design**: Easy integration with other systems
2. **Webhooks**: Notify external systems of matches
3. **Export Formats**: Support for various output formats
4. **Plugin System**: Custom preprocessing/postprocessing pipelines

---

## Resources & References

### Academic Papers
- "Deep Learning for Entity Matching: A Design Space Exploration" (2018)
- "Dual-Objective Fine-Tuning of BERT for Entity Matching" (VLDB 2021)
- "Analyzing How BERT Performs Entity Matching" (VLDB 2022)

### Libraries & Tools
- Hugging Face Transformers: https://huggingface.co/docs/transformers
- SHAP: https://shap.readthedocs.io/
- Sentence Transformers: https://www.sbert.net/
- RecordLinkage (Python): https://recordlinkage.readthedocs.io/

### Datasets
- UCI Record Linkage: https://archive.ics.uci.edu/ml/datasets/record+linkage+comparison+patterns
- Entity Matching Benchmarks: https://github.com/anhaidgroup/deepmatcher

### Tutorials
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- React + TypeScript: https://react-typescript-cheatsheet.netlify.app/
- BERT Fine-tuning: https://huggingface.co/course/chapter3
