import { useState } from 'react'
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material'
import { useMutation } from '@tanstack/react-query'
import CompareArrowsIcon from '@mui/icons-material/CompareArrows'
import { api } from '../services/api'
import type { RecordPair, RecordBase } from '../types'
import MatchResultDisplay from '../components/MatchResultDisplay'

export default function MatchingPage() {
  const [recordA, setRecordA] = useState<RecordBase>({
    fields: {
      name: '',
      address: '',
      city: '',
      phone: '',
    },
  })

  const [recordB, setRecordB] = useState<RecordBase>({
    fields: {
      name: '',
      address: '',
      city: '',
      phone: '',
    },
  })

  const matchMutation = useMutation({
    mutationFn: (pair: RecordPair) => api.predictMatch(pair, true),
  })

  const handleFieldChange = (
    record: 'A' | 'B',
    field: string,
    value: string
  ) => {
    if (record === 'A') {
      setRecordA((prev) => ({
        ...prev,
        fields: { ...prev.fields, [field]: value },
      }))
    } else {
      setRecordB((prev) => ({
        ...prev,
        fields: { ...prev.fields, [field]: value },
      }))
    }
  }

  const handleMatch = () => {
    matchMutation.mutate({
      record_a: recordA,
      record_b: recordB,
    })
  }

  const handleLoadExample = () => {
    setRecordA({
      fields: {
        name: 'John Smith',
        address: '123 Main Street',
        city: 'New York',
        phone: '555-1234',
      },
    })
    setRecordB({
      fields: {
        name: 'J. Smith',
        address: '123 Main St',
        city: 'New York',
        phone: '5551234',
      },
    })
  }

  const fields = ['name', 'address', 'city', 'phone']

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Match Records
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Enter two records to compare and see if they match. The AI will provide a match
        probability and explain which fields contributed to the decision.
      </Typography>

      <Button
        variant="outlined"
        onClick={handleLoadExample}
        sx={{ mb: 3 }}
      >
        Load Example
      </Button>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3}>
          {/* Record A */}
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom color="primary">
              Record A
            </Typography>
            {fields.map((field) => (
              <TextField
                key={`a-${field}`}
                fullWidth
                label={field.charAt(0).toUpperCase() + field.slice(1)}
                value={recordA.fields[field] || ''}
                onChange={(e) => handleFieldChange('A', field, e.target.value)}
                margin="normal"
              />
            ))}
          </Grid>

          {/* Record B */}
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom color="secondary">
              Record B
            </Typography>
            {fields.map((field) => (
              <TextField
                key={`b-${field}`}
                fullWidth
                label={field.charAt(0).toUpperCase() + field.slice(1)}
                value={recordB.fields[field] || ''}
                onChange={(e) => handleFieldChange('B', field, e.target.value)}
                margin="normal"
              />
            ))}
          </Grid>
        </Grid>

        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
          <Button
            variant="contained"
            size="large"
            onClick={handleMatch}
            disabled={matchMutation.isPending}
            startIcon={
              matchMutation.isPending ? (
                <CircularProgress size={20} />
              ) : (
                <CompareArrowsIcon />
              )
            }
          >
            {matchMutation.isPending ? 'Matching...' : 'Match Records'}
          </Button>
        </Box>
      </Paper>

      {/* Error Display */}
      {matchMutation.isError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error: {(matchMutation.error as Error).message}
        </Alert>
      )}

      {/* Results Display */}
      {matchMutation.data && (
        <MatchResultDisplay result={matchMutation.data} />
      )}
    </Box>
  )
}
