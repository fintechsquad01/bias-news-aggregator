import React from 'react';
import { Box, Typography, Container, Link } from '@mui/material';

function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[200],
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          {'© '}
          {new Date().getFullYear()}
          {' Bias-Aware Stock News Aggregator | '}
          <Link color="inherit" href="#" underline="hover">
            About
          </Link>
          {' | '}
          <Link color="inherit" href="#" underline="hover">
            Methodology
          </Link>
          {' | '}
          <Link color="inherit" href="#" underline="hover">
            Terms
          </Link>
        </Typography>
        <Typography variant="caption" color="text.secondary" align="center" display="block" sx={{ mt: 1 }}>
          This platform uses bias data from AllSides and is not affiliated with any news organization.
          The bias and sentiment labels are for informational purposes only and do not constitute financial advice.
        </Typography>
      </Container>
    </Box>
  );
}

export default Footer;
