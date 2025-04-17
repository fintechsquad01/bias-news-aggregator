import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Alert, Grid, Card, CardContent, Container, Paper, TextField, Button, Chip, Divider } from '@mui/material';
import axios from 'axios';

import BiasDistributionChart from '../components/BiasDistributionChart';
import SentimentDistributionChart from '../components/SentimentDistributionChart';
import NewsArticleList from '../components/NewsArticleList';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const PortfolioPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [portfolioData, setPortfolioData] = useState(null);
  const [tickerInput, setTickerInput] = useState('');
  const [tickers, setTickers] = useState(['AAPL', 'MSFT', 'GOOGL']);
  const [selectedTicker, setSelectedTicker] = useState(null);
  const [tickerNews, setTickerNews] = useState([]);

  useEffect(() => {
    const fetchPortfolioData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // In a real implementation, this would be an API call
        // For now, we'll simulate API response
        
        // Fetch portfolio analysis
        const tickersParam = tickers.join(',');
        const response = await axios.get(`${API_BASE_URL}/analysis/portfolio?tickers=${tickersParam}`);
        setPortfolioData(response.data);
        
      } catch (err) {
        console.error('Error fetching portfolio data:', err);
        setError('Failed to load portfolio data. Please try again later.');
        
        // For demo purposes, set mock data
        setMockData();
      } finally {
        setLoading(false);
      }
    };
    
    fetchPortfolioData();
  }, [tickers]);

  useEffect(() => {
    const fetchTickerNews = async () => {
      if (!selectedTicker) return;
      
      try {
        // Fetch news for selected ticker
        const response = await axios.get(`${API_BASE_URL}/news?ticker=${selectedTicker}&limit=5`);
        setTickerNews(response.data);
      } catch (err) {
        console.error(`Error fetching news for ${selectedTicker}:`, err);
        // Set mock news data
        setTickerNews(getMockNewsForTicker(selectedTicker));
      }
    };
    
    fetchTickerNews();
  }, [selectedTicker]);
  
  // Set mock data for demo purposes
  const setMockData = () => {
    setPortfolioData({
      tickers: tickers,
      days: 7,
      ticker_results: {
        'AAPL': {
          ticker: 'AAPL',
          bias_distribution: {
            ticker: 'AAPL',
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
          },
          sentiment_distribution: {
            ticker: 'AAPL',
            total_articles: 50,
            bullish_count: 25,
            bearish_count: 15,
            neutral_count: 10,
            bullish_percentage: 50,
            bearish_percentage: 30,
            neutral_percentage: 20,
            days: 7,
            overall_sentiment: 'bullish',
          },
          diversity_warning: null,
          sentiment_summary: 'News sentiment for AAPL is predominantly bullish (50.0% positive) over the past 7 days.'
        },
        'MSFT': {
          ticker: 'MSFT',
          bias_distribution: {
            ticker: 'MSFT',
            total_articles: 40,
            left_count: 5,
            lean_left_count: 5,
            center_count: 10,
            lean_right_count: 10,
            right_count: 10,
            left_percentage: 12.5,
            lean_left_percentage: 12.5,
            center_percentage: 25,
            lean_right_percentage: 25,
            right_percentage: 25,
            days: 7,
            is_biased: false,
          },
          sentiment_distribution: {
            ticker: 'MSFT',
            total_articles: 40,
            bullish_count: 20,
            bearish_count: 10,
            neutral_count: 10,
            bullish_percentage: 50,
            bearish_percentage: 25,
            neutral_percentage: 25,
            days: 7,
            overall_sentiment: 'bullish',
          },
          diversity_warning: null,
          sentiment_summary: 'News sentiment for MSFT is predominantly bullish (50.0% positive) over the past 7 days.'
        },
        'GOOGL': {
          ticker: 'GOOGL',
          bias_distribution: {
            ticker: 'GOOGL',
            total_articles: 45,
            left_count: 15,
            lean_left_count: 15,
            center_count: 5,
            lean_right_count: 5,
            right_count: 5,
            left_percentage: 33.3,
            lean_left_percentage: 33.3,
            center_percentage: 11.1,
            lean_right_percentage: 11.1,
            right_percentage: 11.1,
            days: 7,
            is_biased: true,
          },
          sentiment_distribution: {
            ticker: 'GOOGL',
            total_articles: 45,
            bullish_count: 15,
            bearish_count: 20,
            neutral_count: 10,
            bullish_percentage: 33.3,
            bearish_percentage: 44.4,
            neutral_percentage: 22.2,
            days: 7,
            overall_sentiment: 'bearish',
          },
          diversity_warning: 'Warning: News coverage for GOOGL is predominantly from left sources (66.6%).',
          sentiment_summary: 'News sentiment for GOOGL is predominantly bearish (44.4% negative) over the past 7 days.'
        }
      },
      aggregate: {
        total_articles: 135,
        bias_distribution: {
          left_count: 35,
          lean_left_count: 30,
          center_count: 25,
          lean_right_count: 23,
          right_count: 22,
          left_percentage: 25.9,
          lean_left_percentage: 22.2,
          center_percentage: 18.5,
          lean_right_percentage: 17.0,
          right_percentage: 16.3,
        },
        sentiment_distribution: {
          bullish_count: 60,
          bearish_count: 45,
          neutral_count: 30,
          bullish_percentage: 44.4,
          bearish_percentage: 33.3,
          neutral_percentage: 22.2,
        },
        biased_tickers: ['GOOGL'],
        has_biased_coverage: true
      }
    });
  };
  
  const getMockNewsForTicker = (ticker) => {
    return [
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
    ];
  };

  const handleAddTicker = () => {
    if (!tickerInput || tickers.includes(tickerInput.toUpperCase())) return;
    
    setTickers([...tickers, tickerInput.toUpperCase()]);
    setTickerInput('');
  };

  const handleRemoveTicker = (tickerToRemove) => {
    setTickers(tickers.filter(t => t !== tickerToRemove));
    if (selectedTicker === tickerToRemove) {
      setSelectedTicker(null);
    }
  };

  const handleTickerSelect = (ticker) => {
    setSelectedTicker(ticker);
  };

  if (loading && !portfolioData) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 6 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Your Portfolio
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Track news bias and sentiment across your watchlist
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <TextField
                label="Add Ticker"
                variant="outlined"
                size="small"
                value={tickerInput}
                onChange={(e) => setTickerInput(e.target.value.toUpperCase())}
                sx={{ mr: 2 }}
              />
              <Button 
                variant="contained" 
                onClick={handleAddTicker}
                disabled={!tickerInput}
              >
                Add
              </Button>
            </Box>
            
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {tickers.map((ticker) => (
                <Chip
                  key={ticker}
                  label={ticker}
                  onClick={() => handleTickerSelect(ticker)}
                  onDelete={() => handleRemoveTicker(ticker)}
                  color={selectedTicker === ticker ? "primary" : "default"}
                  variant={selectedTicker === ticker ? "filled" : "outlined"}
                />
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {portfolioData && portfolioData.aggregate && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom>
              Portfolio Overview
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Bias Distribution
                </Typography>
                <BiasDistributionChart data={portfolioData.aggregate.bias_distribution} />
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Sentiment Distribution
                </Typography>
                <SentimentDistributionChart data={portfolioData.aggregate.sentiment_distribution} />
              </CardContent>
            </Card>
          </Grid>
          
          {portfolioData.aggregate.has_biased_coverage && (
            <Grid item xs={12}>
              <Alert severity="warning">
                Some tickers in your portfolio have biased news coverage. Check individual tickers for details.
              </Alert>
            </Grid>
          )}
        </Grid>
      )}

      {selectedTicker && portfolioData && portfolioData.ticker_results && portfolioData.ticker_results[selectedTicker] && (
        <Box sx={{ mt: 6 }}>
          <Divider sx={{ mb: 4 }} />
          
          <Typography variant="h5" gutterBottom>
            {selectedTicker} Details
          </Typography>
          
          {portfolioData.ticker_results[selectedTicker].diversity_warning && (
            <Alert severity="warning" sx={{ mb: 3 }}>
              {portfolioData.ticker_results[selectedTicker].diversity_warning}
            </Alert>
          )}
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Bias Distribution
                  </Typography>
                  <BiasDistributionChart data={portfolioData.ticker_results[selectedTicker].bias_distribution} />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Sentiment Distribution
                  </Typography>
                  <SentimentDistributionChart data={portfolioData.ticker_results[selectedTicker].sentiment_distribution} />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Recent News for {selectedTicker}
              </Typography>
              <NewsArticleList articles={tickerNews} />
            </Grid>
          </Grid>
        </Box>
      )}
    </Container>
  );
};

export default PortfolioPage;
