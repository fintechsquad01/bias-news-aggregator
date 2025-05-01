import React from 'react';
import PropTypes from 'prop-types';
import { Box, Typography } from '@mui/material';

/**
 * BiasSpectrum component displays a visual representation of political bias
 * on a spectrum from Left (-1) to Right (+1).
 * 
 * @component
 * @param {Object} props - Component props
 * @param {number} props.biasScore - The bias score between -1 (Left) and +1 (Right)
 * @returns {JSX.Element} A visual representation of the bias spectrum
 */
const BiasSpectrum = ({ biasScore }) => {
  // Validate and clamp the bias score
  const clampedScore = Math.max(-1, Math.min(1, biasScore));
  
  // Calculate the position percentage (0 to 100)
  const position = ((clampedScore + 1) / 2) * 100;

  return (
    <Box sx={{ width: '100%', maxWidth: 400, mx: 'auto', py: 2 }}>
      {/* Spectrum bar */}
      <Box
        sx={{
          position: 'relative',
          height: 8,
          bgcolor: 'grey.200',
          borderRadius: 4,
          overflow: 'hidden',
        }}
      >
        {/* Gradient background */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(90deg, #2196f3 0%, #f5f5f5 50%, #f44336 100%)',
          }}
        />
        
        {/* Position indicator */}
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: `${position}%`,
            transform: 'translate(-50%, -50%)',
            width: 12,
            height: 12,
            bgcolor: 'white',
            border: '2px solid',
            borderColor: 'grey.800',
            borderRadius: '50%',
            boxShadow: 1,
          }}
        />
      </Box>

      {/* Labels */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          mt: 1,
          px: 0.5,
        }}
      >
        <Typography variant="caption" color="text.secondary">
          Left
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Center
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Right
        </Typography>
      </Box>
    </Box>
  );
};

BiasSpectrum.propTypes = {
  biasScore: PropTypes.number.isRequired,
};

export default BiasSpectrum; 