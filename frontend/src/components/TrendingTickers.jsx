import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent, List, ListItem, ListItemText, Skeleton, Divider, Link } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

const TrendingTickers = () => {
  const navigate = useNavigate();
  const [trendingTickers, setTrendingTickers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real implementation, this would fetch data from the API
    // For now, we'll use mock data
    const mockTrendingTickers = [
      { symbol: 'AAPL', name: 'Apple Inc.', change: 2.5 },
      { symbol: 'MSFT', name: 'Microsoft Corporation', change: 1.2 },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', change: -0.8 },
      { symbol: 'AMZN', name: 'Amazon.com Inc.', change: 3.1 },
      { symbol: 'TSLA', name: 'Tesla, Inc.', change: -2.3 }
    ];

    // Simulate API call delay
    setTimeout(() => {
      setTrendingTickers(mockTrendingTickers);
      setLoading(false);
    }, 1000);
  }, []);

  const handleTickerClick = (ticker) => {
    navigate(`/ticker/${ticker}`);
  };

  return (
    <Box>
      <Box display="flex" alignItems="center" mb={1}>
        <TrendingUpIcon color="primary" sx={{ mr: 1 }} />
        <Typography variant="subtitle1">Trending Tickers</Typography>
      </Box>
      
      {loading ? (
        <List disablePadding>
          {[1, 2, 3, 4, 5].map((item) => (
            <React.Fragment key={item}>
              <ListItem disablePadding sx={{ py: 1 }}>
                <Skeleton variant="rectangular" width="100%" height={40} />
              </ListItem>
              {item < 5 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      ) : (
        <List disablePadding>
          {trendingTickers.map((ticker, index) => (
            <React.Fragment key={ticker.symbol}>
              <ListItem 
                disablePadding 
                sx={{ 
                  py: 1, 
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: 'action.hover',
                  }
                }}
                onClick={() => handleTickerClick(ticker.symbol)}
              >
                <ListItemText 
                  primary={
                    <Box display="flex" justifyContent="space-between">
                      <Typography variant="body1" fontWeight="bold">{ticker.symbol}</Typography>
                      <Typography 
                        variant="body2" 
                        color={ticker.change >= 0 ? 'success.main' : 'error.main'}
                      >
                        {ticker.change >= 0 ? '+' : ''}{ticker.change.toFixed(1)}%
                      </Typography>
                    </Box>
                  }
                  secondary={ticker.name}
                />
              </ListItem>
              {index < trendingTickers.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      )}
    </Box>
  );
};

export default TrendingTickers;
