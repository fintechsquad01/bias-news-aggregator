import React from 'react';
import { Box, Typography, Chip, Paper, Grid } from '@mui/material';

const BiasLegend = () => {
  return (
    <Box>
      <Typography variant="subtitle2" gutterBottom>Bias Categories</Typography>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Box display="flex" alignItems="center" mb={0.5}>
            <Box 
              sx={{ 
                width: 16, 
                height: 16, 
                bgcolor: '#3f51b5', 
                borderRadius: '50%',
                mr: 1 
              }} 
            />
            <Typography variant="body2">Left</Typography>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box display="flex" alignItems="center" mb={0.5}>
            <Box 
              sx={{ 
                width: 16, 
                height: 16, 
                bgcolor: '#90caf9', 
                borderRadius: '50%',
                mr: 1 
              }} 
            />
            <Typography variant="body2">Lean Left</Typography>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box display="flex" alignItems="center" mb={0.5}>
            <Box 
              sx={{ 
                width: 16, 
                height: 16, 
                bgcolor: '#9e9e9e', 
                borderRadius: '50%',
                mr: 1 
              }} 
            />
            <Typography variant="body2">Center</Typography>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box display="flex" alignItems="center" mb={0.5}>
            <Box 
              sx={{ 
                width: 16, 
                height: 16, 
                bgcolor: '#ffb74d', 
                borderRadius: '50%',
                mr: 1 
              }} 
            />
            <Typography variant="body2">Lean Right</Typography>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box display="flex" alignItems="center" mb={0.5}>
            <Box 
              sx={{ 
                width: 16, 
                height: 16, 
                bgcolor: '#f44336', 
                borderRadius: '50%',
                mr: 1 
              }} 
            />
            <Typography variant="body2">Right</Typography>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BiasLegend;
