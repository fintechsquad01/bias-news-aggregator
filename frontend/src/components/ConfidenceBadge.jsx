import React from 'react';
import PropTypes from 'prop-types';
import { Chip } from '@mui/material';

/**
 * ConfidenceBadge component displays a colored badge indicating the confidence level
 * of a sentiment analysis result.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {string} props.confidenceLevel - The confidence level ("High", "Medium", or "Low")
 * @returns {JSX.Element} A colored badge displaying the confidence level
 */
const ConfidenceBadge = ({ confidenceLevel }) => {
  // Define color mapping based on confidence level
  const getColor = (level) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'success';
      case 'medium':
        return 'warning';
      case 'low':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Chip
      label={confidenceLevel}
      color={getColor(confidenceLevel)}
      size="small"
      sx={{
        fontWeight: 'medium',
        minWidth: '80px',
        '& .MuiChip-label': {
          px: 1,
        },
      }}
    />
  );
};

ConfidenceBadge.propTypes = {
  confidenceLevel: PropTypes.oneOf(['High', 'Medium', 'Low']).isRequired,
};

export default ConfidenceBadge; 