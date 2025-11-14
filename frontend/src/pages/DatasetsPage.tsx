import { Typography, Box } from '@mui/material'
import { useQuery } from '@tanstack/react-query'
import { api } from '../services/api'

export default function DatasetsPage() {
  const { data: datasets, isLoading } = useQuery({
    queryKey: ['datasets'],
    queryFn: () => api.listDatasets(),
  })

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Datasets
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Available datasets for record linkage experiments.
      </Typography>

      {isLoading && <Typography>Loading datasets...</Typography>}

      {datasets && (
        <Box>
          {datasets.map((dataset) => (
            <Box key={dataset.name} sx={{ mb: 2 }}>
              <Typography variant="h6">{dataset.name}</Typography>
              <Typography variant="body2" color="text.secondary">
                {dataset.description}
              </Typography>
              <Typography variant="body2">
                Records: {dataset.num_records} | Fields: {dataset.fields.join(', ')}
              </Typography>
            </Box>
          ))}
        </Box>
      )}
    </Box>
  )
}
