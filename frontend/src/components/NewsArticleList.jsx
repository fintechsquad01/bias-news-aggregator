import React from 'react';
import { Box, Typography, Card, CardContent, Chip, Link, Grid, Divider } from '@mui/material';
import { format } from 'date-fns';
import ConfidenceBadge from './ConfidenceBadge';
import { calculateConfidenceScore } from '../utils/confidenceUtils';

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

const NewsArticleList = ({ articles }) => {
  if (!articles || articles.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="body1">No articles found</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {articles.map((article) => (
        <Card key={article.id} sx={{ mb: 2 }}>
          <CardContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Link 
                  href={article.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  underline="hover"
                  color="inherit"
                >
                  <Typography variant="h6" component="h2">
                    {article.headline}
                  </Typography>
                </Link>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {article.summary}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Divider sx={{ mb: 1 }} />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: { xs: 1, sm: 0 }, gap: 1 }}>
                    <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
                      {article.source}
                    </Typography>
                    <Chip 
                      label={getBiasLabel(article.bias_label)} 
                      size="small" 
                      sx={{ 
                        bgcolor: getBiasColor(article.bias_label),
                        color: ['left', 'right'].includes(article.bias_label) ? 'white' : 'inherit',
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
                    {article.sentiment_confidence !== null && article.sentiment_confidence !== undefined && (
                      <ConfidenceBadge 
                        confidenceLevel={calculateConfidenceScore(article.sentiment_confidence)} 
                      />
                    )}
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {format(new Date(article.published_date), 'MMM d, yyyy')}
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default NewsArticleList;
