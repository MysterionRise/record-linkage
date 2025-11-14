import { Routes, Route } from 'react-router-dom'
import { Box, Container } from '@mui/material'
import HomePage from './pages/HomePage'
import MatchingPage from './pages/MatchingPage'
import DatasetsPage from './pages/DatasetsPage'
import BatchProcessingPage from './pages/BatchProcessingPage'
import AppBar from './components/AppBar'

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar />
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flex: 1 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/match" element={<MatchingPage />} />
          <Route path="/datasets" element={<DatasetsPage />} />
          <Route path="/batch" element={<BatchProcessingPage />} />
        </Routes>
      </Container>
    </Box>
  )
}

export default App
