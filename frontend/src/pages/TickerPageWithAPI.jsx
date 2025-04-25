import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Alert, Grid, Card, CardContent, Divider } from '@mui/material';
import axios from 'axios';

import BiasDistributionChart from '../components/BiasDistributionChart';
import SentimentDistributionChart from '../components/SentimentDistributionChart';
import NewsArticleList from '../components/NewsArticleList';
import BiasLegend from '../components/BiasLegend';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const TickerPage = ({ ticker }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tickerData, setTickerData] = useState(null);
  const [biasDistribution, setBiasDistribution] = useState(null);
  const [sentimentDistribution, setSentimentDistribution] = useState(null);
  const [articles, setArticles] = useState([]);
  const [diversityWarning, setDiversityWarning] = useState(null);

  useEffect(() => {
    const fetchTickerData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // In a real implementation, these would be API calls
        // For now, we'll simulate API responses
        
        // Fetch ticker analysis
        const analysisResponse = await axios.get(`${API_BASE_URL}/analysis/ticker/${ticker}/analysis`);
        const analysisData = analysisResponse.data;
        
        // Fetch news articles
        const newsResponse = await axios.get(`${API_BASE_URL}/news?ticker=${ticker}&limit=10`);
        const newsData = newsResponse.data;
        
        // Update state with fetched data
        setTickerData({
          symbol: ticker,
          name: getCompanyName(ticker),
          price: 150.25,
          change: 2.5,
          changePercent: 1.75,
        });
        
        setBiasDistribution(analysisData.bias_distribution);
        setSentimentDistribution(analysisData.sentiment_distribution);
        setArticles(newsData);
        setDiversityWarning(analysisData.diversity_warning);
        
      } catch (err) {
        console.error('Error fetching ticker data:', err);
        setError('Failed to load ticker data. Please try again later.');
        
        // For demo purposes, set mock data
        setMockData(ticker);
      } finally {
        setLoading(false);
      }
    };
    
    fetchTickerData();
  }, [ticker]);
  
  // Helper function to get company name from ticker
  const getCompanyName = (ticker) => {
    const companies = {
      'AAPL': 'Apple Inc.',
      'MSFT': 'Microsoft Corporation',
      'GOOGL': 'Alphabet Inc.',
      'AMZN': 'Amazon.com Inc.',
      'TSLA': 'Tesla, Inc.',
    };
    
    return companies[ticker] || ticker;
  };
  
  // Set mock data for demo purposes
  const setMockData = (ticker) => {
    setTickerData({
      symbol: ticker,
      name: getCompanyName(ticker),
      price: 150.25,
      change: 2.5,
      changePercent: 1.75,
    });
    
    setBiasDistribution({
      ticker: ticker,
      total_articles: 50,
      left_count: 15,
      lean_left_count: 10,
      center_count: 10,
      lean_right_count: 8,
      right_count: 7,
      left_percentage: 30,
      lean_left_percentage: 20,
      center_percentage: 20,
      lean_right_percentage: 16,
      right_percentage: 14,
      days: 7,
      is_biased: false,
    });
    
    setSentimentDistribution({
      ticker: ticker,
      total_articles: 50,
      bullish_count: 25,
      bearish_count: 15,
      neutral_count: 10,
      bullish_percentage: 50,
      bearish_percentage: 30,
      neutral_percentage: 20,
      days: 7,
      overall_sentiment: 'bullish',
    });
    
    setArticles([
      {
        id: 1,
        ticker: ticker,
        headline: `${ticker} Reports Strong Quarterly Earnings`,
        summary: `${ticker} exceeded analyst expectations with record revenue and profit growth.`,
        url: 'https://example.com/article1',
        source: 'Financial Times',
        bias_label: 'center',
        sentiment_label: 'bullish',
        published_date: '2025-04-15T14:30:00Z',
      },
      {
        id: 2,
        ticker: ticker,
        headline: `${ticker} Faces Regulatory Scrutiny Over New Product`,
        summary: `Regulators are examining ${ticker}'s latest product for potential compliance issues.`,
        url: 'https://example.com/article2',
        source: 'Wall Street Journal',
        bias_label: 'lean_right',
        sentiment_label: 'bearish',
        published_date: '2025-04-16T09:15:00Z',
      },
      {
        id: 3,
        ticker: ticker,
        headline: `${ticker} Announces Expansion into New Markets`,
        summary: `${ticker} plans to enter emerging markets with innovative products.`,
        url: 'https://example.com/article3',
        source: 'CNN Business',
        bias_label: 'lean_left',
        sentiment_label: 'bullish',
        published_date: '2025-04-17T11:45:00Z',
      },
    ]);
    
    setDiversityWarning(null);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', mt: 4, px: 2 }}>
      {tickerData && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={6}>
                <Typography variant="h4">{tickerData.symbol}</Typography>
                <Typography variant="h6" color="text.secondary">{tickerData.name}</Typography>
              </Grid>
              <Grid item xs={12} md={6} sx={{ textAlign: { md: 'right' } }}>
                <Typography variant="h5">${tickerData.price.toFixed(2)}</Typography>
                <Typography 
                  variant="subtitle1" 
                  color={tickerData.change >= 0 ? 'success.main' : 'error.main'}
                >
                  {tickerData.change >= 0 ? '+' : ''}{tickerData.change.toFixed(2)} ({tickerData.changePercent.toFixed(2)}%)
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {diversityWarning && (
        <Alert severity="warning" sx={{ mb: 4 }}>
          {diversityWarning}
        </Alert>
      )}

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card sx={{ mb: 4, height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Bias Distribution (Last 7 Days)</Typography>
              <BiasDistributionChart data={biasDistribution} />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card sx={{ mb: 4, height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Sentiment Distribution (Last 7 Days)</Typography>
              <SentimentDistributionChart data={sentimentDistribution} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={4}>
        <Grid item xs={12} md={3}>
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>About Bias Analysis</Typography>
              <Typography variant="body2" paragraph>
                We categorize news sources on a political spectrum from Left to Right based on 
                AllSides Media Bias Ratings, a widely respected methodology.
              </Typography>
              <BiasLegend />
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom>About Sentiment Analysis</Typography>
              <Typography variant="body2" paragraph>
                Our sentiment analysis uses natural language processing to determine if an article
                is bullish (positive), bearish (negative), or neutral about a stock.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={9}>
          <Typography variant="h6" gutterBottom>Recent News</Typography>
          <NewsArticleList articles={articles} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default TickerPage;
