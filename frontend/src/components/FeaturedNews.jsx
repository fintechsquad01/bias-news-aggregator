import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent, CardActionArea, Grid, Skeleton, Chip } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const getBiasColor = (biasLabel) => {
  const biasColors = {
    left: '#3f51b5',
    lean_left: '#90caf9',
    center: '#9e9e9e',
    lean_right: '#ffb74d',
    right: '#f44336',
    unknown: '#bdbdbd'
  };
  return biasColors[biasLabel] || '#bdbdbd';
};

const getSentimentColor = (sentimentLabel) => {
  const sentimentColors = {
    bullish: '#4caf50',
    bearish: '#f44336',
    neutral: '#9e9e9e'
  };
  return sentimentColors[sentimentLabel] || '#9e9e9e';
};

const getBiasLabel = (biasValue) => {
  const biasLabels = {
    left: 'Left',
    lean_left: 'Lean Left',
    center: 'Center',
    lean_right: 'Lean Right',
    right: 'Right',
    unknown: 'Unknown'
  };
  return biasLabels[biasValue] || 'Unknown';
};

const getSentimentLabel = (sentimentValue) => {
  const sentimentLabels = {
    bullish: 'Bullish',
    bearish: 'Bearish',
    neutral: 'Neutral'
  };
  return sentimentLabels[sentimentValue] || 'Neutral';
};

const FeaturedNews = () => {
  const navigate = useNavigate();
  const [featuredNews, setFeaturedNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real implementation, this would fetch data from the API
    // For now, we'll use mock data
    const mockFeaturedNews = [
      {
        id: 1,
        ticker: 'AAPL',
        headline: 'Apple Reports Record Quarterly Revenue',
        summary: 'Apple Inc. announced financial results for its fiscal 2025 second quarter ended March 29, 2025, with record revenue of $97.3 billion, up 9 percent year over year.',
        source: 'Financial Times',
        bias_label: 'center',
        sentiment_label: 'bullish',
        published_date: '2025-04-15T14:30:00Z'
      },
      {
        id: 2,
        ticker: 'MSFT',
        headline: 'Microsoft Cloud Growth Accelerates',
        summary: 'Microsoft reported strong fiscal third-quarter results, with cloud revenue exceeding analyst expectations as more businesses adopt AI-powered solutions.',
        source: 'Wall Street Journal',
        bias_label: 'lean_right',
        sentiment_label: 'bullish',
        published_date: '2025-04-16T09:15:00Z'
      },
      {
        id: 3,
        ticker: 'TSLA',
        headline: 'Tesla Faces Production Challenges in New Markets',
        summary: 'Tesla is experiencing production delays at its newest factories as it navigates supply chain disruptions and regulatory hurdles in expanding markets.',
        source: 'CNN Business',
        bias_label: 'lean_left',
        sentiment_label: 'bearish',
        published_date: '2025-04-17T11:45:00Z'
      }
    ];

    // Simulate API call delay
    setTimeout(() => {
      setFeaturedNews(mockFeaturedNews);
      setLoading(false);
    }, 1000);
  }, []);

  const handleArticleClick = (ticker) => {
    navigate(`/ticker/${ticker}`);
  };

  return (
    <Box>
      {loading ? (
        <Grid container spacing={3}>
          {[1, 2, 3].map((item) => (
            <Grid item xs={12} key={item}>
              <Skeleton variant="rectangular" height={200} />
            </Grid>
          ))}
        </Grid>
      ) : (
        <Grid container spacing={3}>
          {featuredNews.map((article) => (
            <Grid item xs={12} key={article.id}>
              <Card>
                <CardActionArea onClick={() => handleArticleClick(article.ticker)}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Chip 
                        label={article.ticker} 
                        color="primary" 
                        size="small" 
                        sx={{ mr: 1 }}
                      />
                      <Box>
                        <Chip 
                          label={getBiasLabel(article.bias_label)} 
                          size="small" 
                          sx={{ 
                            bgcolor: getBiasColor(article.bias_label),
                            color: ['left', 'right'].includes(article.bias_label) ? 'white' : 'inherit',
                            mr: 1
                          }} 
                        />
                        <Chip 
                          label={getSentimentLabel(article.sentiment_label)} 
                          size="small" 
                          sx={{ 
                            bgcolor: getSentimentColor(article.sentiment_label),
                            color: article.sentiment_label !== 'neutral' ? 'white' : 'inherit'
                          }} 
                        />
                      </Box>
                    </Box>
                    <Typography variant="h6" component="h2" gutterBottom>
                      {article.headline}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {article.summary}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2" color="text.secondary">
                        {article.source}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(article.published_date).toLocaleDateString()}
                      </Typography>
                    </Box>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default FeaturedNews;
