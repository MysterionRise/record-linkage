import { Box, Typography, Paper, Chip, Stack } from '@mui/material'
import type { Explanation } from '../types'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer } from 'recharts'

interface Props {
  explanation: Explanation
}

export default function ExplanationDisplay({ explanation }: Props) {
  // Prepare data for chart
  const chartData = explanation.feature_contributions.slice(0, 10).map((fc) => ({
    name: fc.field_name,
    contribution: fc.contribution,
    value_a: fc.value_a,
    value_b: fc.value_b,
  }))

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Explanation ({explanation.method})
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        This shows which fields contributed most to the match decision. Positive values
        indicate evidence for matching, negative values suggest non-matching.
      </Typography>

      {/* Top Contributing Features */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" gutterBottom>
          Top Positive Features
        </Typography>
        <Stack direction="row" spacing={1} flexWrap="wrap">
          {explanation.top_positive_features.map((feature) => (
            <Chip
              key={feature}
              label={feature}
              color="success"
              size="small"
              sx={{ mb: 1 }}
            />
          ))}
        </Stack>
      </Box>

      {explanation.top_negative_features.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Top Negative Features
          </Typography>
          <Stack direction="row" spacing={1} flexWrap="wrap">
            {explanation.top_negative_features.map((feature) => (
              <Chip
                key={feature}
                label={feature}
                color="error"
                size="small"
                sx={{ mb: 1 }}
              />
            ))}
          </Stack>
        </Box>
      )}

      {/* Feature Contributions Chart */}
      <Paper sx={{ p: 2, mt: 3 }}>
        <Typography variant="subtitle2" gutterBottom>
          Feature Contributions
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis type="category" dataKey="name" width={100} />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload
                  return (
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle2">{data.name}</Typography>
                      <Typography variant="body2">
                        Contribution: {data.contribution.toFixed(3)}
                      </Typography>
                      <Typography variant="body2" color="primary">
                        Record A: {data.value_a}
                      </Typography>
                      <Typography variant="body2" color="secondary">
                        Record B: {data.value_b}
                      </Typography>
                    </Paper>
                  )
                }
                return null
              }}
            />
            <Bar dataKey="contribution">
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.contribution > 0 ? '#4caf50' : '#f44336'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Paper>

      {/* Field-by-Field Comparison */}
      <Box sx={{ mt: 3 }}>
        <Typography variant="subtitle2" gutterBottom>
          Field-by-Field Comparison
        </Typography>
        {explanation.feature_contributions.map((fc) => (
          <Paper
            key={fc.field_name}
            sx={{
              p: 2,
              mb: 1,
              borderLeft: 4,
              borderColor: fc.contribution > 0 ? 'success.main' : 'error.main',
            }}
          >
            <Typography variant="subtitle2">{fc.field_name}</Typography>
            <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
              <Box sx={{ flex: 1 }}>
                <Typography variant="caption" color="text.secondary">
                  Record A
                </Typography>
                <Typography variant="body2">{fc.value_a || '(empty)'}</Typography>
              </Box>
              <Box sx={{ flex: 1 }}>
                <Typography variant="caption" color="text.secondary">
                  Record B
                </Typography>
                <Typography variant="body2">{fc.value_b || '(empty)'}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Contribution
                </Typography>
                <Typography
                  variant="body2"
                  color={fc.contribution > 0 ? 'success.main' : 'error.main'}
                  fontWeight="bold"
                >
                  {fc.contribution > 0 ? '+' : ''}
                  {fc.contribution.toFixed(3)}
                </Typography>
              </Box>
            </Box>
          </Paper>
        ))}
      </Box>
    </Box>
  )
}
