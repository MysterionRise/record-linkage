import {
  Paper,
  Typography,
  Box,
  Chip,
  Grid,
  LinearProgress,
  Divider,
} from '@mui/material'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import CancelIcon from '@mui/icons-material/Cancel'
import type { MatchResult } from '../types'
import ExplanationDisplay from './ExplanationDisplay'

interface Props {
  result: MatchResult
}

export default function MatchResultDisplay({ result }: Props) {
  const { prediction, explanation } = result

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Match Result
      </Typography>

      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {prediction.is_match ? (
            <CheckCircleIcon sx={{ fontSize: 48, color: 'success.main', mr: 2 }} />
          ) : (
            <CancelIcon sx={{ fontSize: 48, color: 'error.main', mr: 2 }} />
          )}
          <Box sx={{ flex: 1 }}>
            <Typography variant="h4">
              {prediction.is_match ? 'MATCH' : 'NO MATCH'}
            </Typography>
            <Chip
              label={`${prediction.confidence} Confidence`}
              color={
                prediction.confidence === 'High'
                  ? 'success'
                  : prediction.confidence === 'Medium'
                  ? 'warning'
                  : 'error'
              }
              sx={{ mt: 1 }}
            />
          </Box>
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="body2" color="text.secondary">
              Match Probability
            </Typography>
            <Typography variant="h5">
              {(prediction.match_probability * 100).toFixed(1)}%
            </Typography>
            <LinearProgress
              variant="determinate"
              value={prediction.match_probability * 100}
              sx={{ mt: 1, height: 8, borderRadius: 4 }}
              color={prediction.is_match ? 'success' : 'error'}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="body2" color="text.secondary">
              Similarity Score
            </Typography>
            <Typography variant="h5">
              {(prediction.similarity_score * 100).toFixed(1)}%
            </Typography>
            <LinearProgress
              variant="determinate"
              value={prediction.similarity_score * 100}
              sx={{ mt: 1, height: 8, borderRadius: 4 }}
            />
          </Grid>
        </Grid>
      </Box>

      {explanation && (
        <>
          <Divider sx={{ my: 3 }} />
          <ExplanationDisplay explanation={explanation} />
        </>
      )}
    </Paper>
  )
}
