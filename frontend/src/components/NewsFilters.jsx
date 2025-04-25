import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  FormGroup, 
  FormControlLabel, 
  Checkbox,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const NewsFilters = ({ filters, onFilterChange }) => {
  const [expanded, setExpanded] = useState(true);
  const [biasFilters, setBiasFilters] = useState(filters.bias || []);
  const [sentimentFilters, setSentimentFilters] = useState(filters.sentiment || []);

  const handleBiasChange = (event) => {
    const { name, checked } = event.target;
    let newBiasFilters;
    
    if (checked) {
      newBiasFilters = [...biasFilters, name];
    } else {
      newBiasFilters = biasFilters.filter(filter => filter !== name);
    }
    
    setBiasFilters(newBiasFilters);
    onFilterChange({
      ...filters,
      bias: newBiasFilters
    });
  };

  const handleSentimentChange = (event) => {
    const { name, checked } = event.target;
    let newSentimentFilters;
    
    if (checked) {
      newSentimentFilters = [...sentimentFilters, name];
    } else {
      newSentimentFilters = sentimentFilters.filter(filter => filter !== name);
    }
    
    setSentimentFilters(newSentimentFilters);
    onFilterChange({
      ...filters,
      sentiment: newSentimentFilters
    });
  };

  return (
    <Box>
      <Accordion expanded={expanded} onChange={() => setExpanded(!expanded)}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1">Bias Filters</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <FormGroup>
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={biasFilters.includes('left')} 
                  onChange={handleBiasChange} 
                  name="left" 
                  sx={{ color: '#3f51b5', '&.Mui-checked': { color: '#3f51b5' } }}
                />
              } 
              label="Left" 
            />
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={biasFilters.includes('lean_left')} 
                  onChange={handleBiasChange} 
                  name="lean_left" 
                  sx={{ color: '#90caf9', '&.Mui-checked': { color: '#90caf9' } }}
                />
              } 
              label="Lean Left" 
            />
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={biasFilters.includes('center')} 
                  onChange={handleBiasChange} 
                  name="center" 
                  sx={{ color: '#9e9e9e', '&.Mui-checked': { color: '#9e9e9e' } }}
                />
              } 
              label="Center" 
            />
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={biasFilters.includes('lean_right')} 
                  onChange={handleBiasChange} 
                  name="lean_right" 
                  sx={{ color: '#ffb74d', '&.Mui-checked': { color: '#ffb74d' } }}
                />
              } 
              label="Lean Right" 
            />
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={biasFilters.includes('right')} 
                  onChange={handleBiasChange} 
                  name="right" 
                  sx={{ color: '#f44336', '&.Mui-checked': { color: '#f44336' } }}
                />
              } 
              label="Right" 
            />
          </FormGroup>
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1">Sentiment Filters</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <FormGroup>
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={sentimentFilters.includes('bullish')} 
                  onChange={handleSentimentChange} 
                  name="bullish" 
                  sx={{ color: '#4caf50', '&.Mui-checked': { color: '#4caf50' } }}
                />
              } 
              label="Bullish" 
            />
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={sentimentFilters.includes('bearish')} 
                  onChange={handleSentimentChange} 
                  name="bearish" 
                  sx={{ color: '#f44336', '&.Mui-checked': { color: '#f44336' } }}
                />
              } 
              label="Bearish" 
            />
            <FormControlLabel 
              control={
                <Checkbox 
                  checked={sentimentFilters.includes('neutral')} 
                  onChange={handleSentimentChange} 
                  name="neutral" 
                  sx={{ color: '#9e9e9e', '&.Mui-checked': { color: '#9e9e9e' } }}
                />
              } 
              label="Neutral" 
            />
          </FormGroup>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default NewsFilters;
