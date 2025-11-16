import { Typography, Box, Paper, Grid, Card, CardContent, Button } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import CompareArrowsIcon from '@mui/icons-material/CompareArrows'
import DatasetIcon from '@mui/icons-material/Dataset'
import BatchPredictionIcon from '@mui/icons-material/BatchPrediction'
import TipsAndUpdatesIcon from '@mui/icons-material/TipsAndUpdates'
import { api } from '../services/api'

export default function HomePage() {
  const navigate = useNavigate()

  // Check API health
  const { data: health, isLoading } = useQuery({
    queryKey: ['health'],
    queryFn: () => api.healthCheck(),
  })

  return (
    <Box>
      {/* Hero Section */}
      <Paper
        sx={{
          p: 6,
          mb: 4,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom>
          ML-Powered Record Linkage
        </Typography>
        <Typography variant="h5" sx={{ mb: 3, opacity: 0.9 }}>
          Match records with BERT-based AI and explainable predictions
        </Typography>
        <Typography variant="body1" sx={{ mb: 4, opacity: 0.8 }}>
          Identify duplicate records across datasets using state-of-the-art machine learning
          with transparent, interpretable explanations powered by SHAP.
        </Typography>
        <Box>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/match')}
            sx={{
              mr: 2,
              bgcolor: 'white',
              color: 'primary.main',
              '&:hover': { bgcolor: 'grey.100' },
            }}
          >
            Try It Now
          </Button>
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/datasets')}
            sx={{
              color: 'white',
              borderColor: 'white',
              '&:hover': { borderColor: 'grey.300', bgcolor: 'rgba(255,255,255,0.1)' },
            }}
          >
            Explore Datasets
          </Button>
        </Box>
      </Paper>

      {/* System Status */}
      {!isLoading && health && (
        <Paper sx={{ p: 3, mb: 4, bgcolor: 'success.light', color: 'success.contrastText' }}>
          <Typography variant="h6">
            System Status: {health.status.toUpperCase()}
          </Typography>
          <Typography variant="body2">
            Model: {health.model_loaded ? 'Loaded' : 'Not Loaded'} | Device: {health.device} |
            Version: {health.version}
          </Typography>
        </Paper>
      )}

      {/* Features */}
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Features
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <CompareArrowsIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Smart Matching
              </Typography>
              <Typography variant="body2" color="text.secondary">
                BERT-based entity matching with cosine similarity. Compare records and get
                instant match probabilities with confidence scores.
              </Typography>
              <Button
                sx={{ mt: 2 }}
                onClick={() => navigate('/match')}
                variant="outlined"
              >
                Start Matching
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <TipsAndUpdatesIcon sx={{ fontSize: 48, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Explainability
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Understand why records match with SHAP explanations. See which
                fields and tokens contribute most to each prediction.
              </Typography>
              <Button sx={{ mt: 2 }} variant="outlined" disabled>
                Learn More
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <DatasetIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Multiple Datasets
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Pre-loaded datasets including UCI, DBLP-ACM, and product matching data.
                Upload your own CSV files for custom matching.
              </Typography>
              <Button
                sx={{ mt: 2 }}
                onClick={() => navigate('/datasets')}
                variant="outlined"
              >
                View Datasets
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <BatchPredictionIcon sx={{ fontSize: 48, color: 'warning.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Batch Processing
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Process thousands of record pairs at once. Export results with confidence
                scores and explanations for downstream analysis.
              </Typography>
              <Button
                sx={{ mt: 2 }}
                onClick={() => navigate('/batch')}
                variant="outlined"
              >
                Batch Process
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* How It Works */}
      <Box sx={{ mt: 6 }}>
        <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
          How It Works
        </Typography>
        <Paper sx={{ p: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3}>
              <Typography variant="h6" gutterBottom color="primary">
                1. Input Records
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Provide two records with their fields (name, address, etc.)
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="h6" gutterBottom color="primary">
                2. BERT Encoding
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Records are encoded into embeddings using pre-trained transformers
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="h6" gutterBottom color="primary">
                3. Similarity Computation
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Cosine similarity determines match probability
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="h6" gutterBottom color="primary">
                4. Explainability
              </Typography>
              <Typography variant="body2" color="text.secondary">
                SHAP shows which features drove the prediction
              </Typography>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </Box>
  )
}
