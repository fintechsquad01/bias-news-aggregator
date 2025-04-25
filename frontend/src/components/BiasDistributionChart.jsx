import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const BIAS_COLORS = {
  left: '#3f51b5',
  lean_left: '#90caf9',
  center: '#9e9e9e',
  lean_right: '#ffb74d',
  right: '#f44336',
  unknown: '#bdbdbd'
};

const BiasDistributionChart = ({ data }) => {
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
      { name: 'Left', value: data.left_count, percentage: data.left_percentage },
      { name: 'Lean Left', value: data.lean_left_count, percentage: data.lean_left_percentage },
      { name: 'Center', value: data.center_count, percentage: data.center_percentage },
      { name: 'Lean Right', value: data.lean_right_count, percentage: data.lean_right_percentage },
      { name: 'Right', value: data.right_count, percentage: data.right_percentage }
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
    return <Typography variant="body2">No bias data available</Typography>;
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
              const category = entry.name.toLowerCase().replace(' ', '_');
              return <Cell key={`cell-${index}`} fill={BIAS_COLORS[category] || '#bdbdbd'} />;
            })}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default BiasDistributionChart;
