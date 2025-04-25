import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, Chip, Divider } from '@mui/material';
import { useParams } from 'react-router-dom';

// Components to be implemented
import BiasDistributionChart from '../components/BiasDistributionChart';
import NewsArticleList from '../components/NewsArticleList';
import BiasLegend from '../components/BiasLegend';
import NewsFilters from '../components/NewsFilters';

function TickerPage() {
  const { symbol } = useParams();
  
  // State would be managed here with actual API calls
  const [loading, setLoading] = React.useState(false);
  const [tickerData, setTickerData] = React.useState(null);
  const [biasDistribution, setBiasDistribution] = React.useState(null);
  const [articles, setArticles] = React.useState([]);
  const [filters, setFilters] = React.useState({
    bias: [],
    sentiment: [],
  });

  // Mock data for initial UI development
  React.useEffect(() => {
    // This would be replaced with actual API calls
    setLoading(true);
    
    // Simulate API call delay
    setTimeout(() => {
      setTickerData({
        symbol: symbol,
        name: symbol === 'AAPL' ? 'Apple Inc.' : 
              symbol === 'MSFT' ? 'Microsoft Corporation' : 
              symbol === 'GOOGL' ? 'Alphabet Inc.' : 
              symbol === 'AMZN' ? 'Amazon.com Inc.' : 
              symbol === 'TSLA' ? 'Tesla, Inc.' : symbol,
        price: 150.25,
        change: 2.5,
        changePercent: 1.75,
      });
      
      setBiasDistribution({
        ticker: symbol,
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
      
      setArticles([
        {
          id: 1,
          ticker: symbol,
          headline: `${symbol} Reports Strong Quarterly Earnings`,
          summary: `${symbol} exceeded analyst expectations with record revenue and profit growth.`,
          url: 'https://example.com/article1',
          source: 'Financial Times',
          bias_label: 'center',
          sentiment_label: 'bullish',
          published_date: '2025-04-15T14:30:00Z',
        },
        {
          id: 2,
          ticker: symbol,
          headline: `${symbol} Faces Regulatory Scrutiny Over New Product`,
          summary: `Regulators are examining ${symbol}'s latest product for potential compliance issues.`,
          url: 'https://example.com/article2',
          source: 'Wall Street Journal',
          bias_label: 'lean_right',
          sentiment_label: 'bearish',
          published_date: '2025-04-16T09:15:00Z',
        },
        {
          id: 3,
          ticker: symbol,
          headline: `${symbol} Announces Expansion into New Markets`,
          summary: `${symbol} plans to enter emerging markets with innovative products.`,
          url: 'https://example.com/article3',
          source: 'CNN Business',
          bias_label: 'lean_left',
          sentiment_label: 'bullish',
          published_date: '2025-04-17T11:45:00Z',
        },
      ]);
      
      setLoading(false);
    }, 1000);
  }, [symbol]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    // In a real implementation, this would trigger a new API call with the filters
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <Typography>Loading...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', mt: 4 }}>
      {tickerData && (
        <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
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
        </Paper>
      )}

      {biasDistribution && (
        <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>Bias Distribution (Last 7 Days)</Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={8}>
              <BiasDistributionChart data={biasDistribution} />
            </Grid>
            <Grid item xs={12} md={4}>
              <BiasLegend />
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2">
                  {biasDistribution.is_biased 
                    ? `Warning: News coverage for ${symbol} is predominantly from ${biasDistribution.dominant_bias} sources.` 
                    : `News coverage for ${symbol} has a balanced distribution of perspectives.`}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Filters</Typography>
              <Divider sx={{ mb: 2 }} />
              <NewsFilters filters={filters} onFilterChange={handleFilterChange} />
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
}

export default TickerPage;
