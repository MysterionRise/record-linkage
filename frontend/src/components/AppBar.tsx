import { AppBar as MuiAppBar, Toolbar, Typography, Button, Box } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'
import LinkIcon from '@mui/icons-material/Link'

export default function AppBar() {
  return (
    <MuiAppBar position="static">
      <Toolbar>
        <LinkIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 0, mr: 4 }}>
          Record Linkage
        </Typography>
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 2 }}>
          <Button color="inherit" component={RouterLink} to="/">
            Home
          </Button>
          <Button color="inherit" component={RouterLink} to="/match">
            Match Records
          </Button>
          <Button color="inherit" component={RouterLink} to="/datasets">
            Datasets
          </Button>
          <Button color="inherit" component={RouterLink} to="/batch">
            Batch Processing
          </Button>
        </Box>
      </Toolbar>
    </MuiAppBar>
  )
}
