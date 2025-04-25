import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const SENTIMENT_COLORS = {
  bullish: '#4caf50',
  bearish: '#f44336',
  neutral: '#9e9e9e'
};

const SentimentDistributionChart = ({ data }) => {
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!data) {
      setLoading(true);
      return;
    }

    setLoading(false);

    // Transform data for chart
    const transformedData = [
      { name: 'Bullish', value: data.bullish_count, percentage: data.bullish_percentage },
      { name: 'Bearish', value: data.bearish_count, percentage: data.bearish_percentage },
      { name: 'Neutral', value: data.neutral_count, percentage: data.neutral_percentage }
    ].filter(item => item.value > 0);

    setChartData(transformedData);
  }, [data]);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <Box sx={{ bgcolor: 'background.paper', p: 2, border: '1px solid #ccc', borderRadius: 1 }}>
          <Typography variant="body2">{`${payload[0].name}: ${payload[0].value} articles`}</Typography>
          <Typography variant="body2">{`${payload[0].payload.percentage.toFixed(1)}% of coverage`}</Typography>
        </Box>
      );
    }
    return null;
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (chartData.length === 0) {
    return <Typography variant="body2">No sentiment data available</Typography>;
  }

  return (
    <Box sx={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            nameKey="name"
          >
            {chartData.map((entry, index) => {
              const category = entry.name.toLowerCase();
              return <Cell key={`cell-${index}`} fill={SENTIMENT_COLORS[category] || '#bdbdbd'} />;
            })}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default SentimentDistributionChart;
