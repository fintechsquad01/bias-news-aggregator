import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Alert, Grid, Card, CardContent, Container, Paper } from '@mui/material';
import axios from 'axios';

import FeaturedNews from '../components/FeaturedNews';
import TrendingTickers from '../components/TrendingTickers';
import BiasLegend from '../components/BiasLegend';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const HomePage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [trendingNews, setTrendingNews] = useState([]);

  useEffect(() => {
    const fetchHomeData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // In a real implementation, this would be an API call
        // For now, we'll simulate API response
        
        // Fetch trending news
        const response = await axios.get(`${API_BASE_URL}/news/trending`);
        setTrendingNews(response.data);
        
      } catch (err) {
        console.error('Error fetching home data:', err);
        setError('Failed to load trending news. Please try again later.');
        
        // For demo purposes, set mock data
        setMockData();
      } finally {
        setLoading(false);
      }
    };
    
    fetchHomeData();
  }, []);
  
  // Set mock data for demo purposes
  const setMockData = () => {
    // Mock trending news data
    setTrendingNews([]);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Bias-Aware Stock Market News
        </Typography>
        <Typography variant="h6" component="h2" gutterBottom align="center" color="text.secondary">
          Understand the bias and sentiment behind financial news
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
            <Typography variant="h5" gutterBottom>
              Featured News
            </Typography>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
              <FeaturedNews />
            )}
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
            <TrendingTickers />
          </Paper>
          
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Understanding Media Bias
            </Typography>
            <Typography variant="body2" paragraph>
              News sources often have political leanings that can influence how financial news is presented. 
              Our platform helps you identify these biases to get a more balanced view.
            </Typography>
            <BiasLegend />
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ my: 6 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Bias Analysis
                </Typography>
                <Typography variant="body2">
                  We categorize news sources on a political spectrum from Left to Right based on 
                  AllSides Media Bias Ratings, a widely respected methodology.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Sentiment Analysis
                </Typography>
                <Typography variant="body2">
                  Our AI analyzes whether articles are bullish (positive), bearish (negative), 
                  or neutral about a stock, helping you understand market sentiment.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Portfolio Tracking
                </Typography>
                <Typography variant="body2">
                  Create a watchlist of your favorite stocks and get a comprehensive view of 
                  news coverage and sentiment across your portfolio.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default HomePage;
