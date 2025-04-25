import React from 'react';
import { AppBar, Toolbar, Typography, Button, TextField, IconButton, Box, Autocomplete } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';

// Mock data for ticker search - would be replaced with API call
const mockTickers = [
  { symbol: 'AAPL', name: 'Apple Inc.' },
  { symbol: 'MSFT', name: 'Microsoft Corporation' },
  { symbol: 'GOOGL', name: 'Alphabet Inc.' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.' },
  { symbol: 'TSLA', name: 'Tesla, Inc.' },
];

function Navbar() {
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = React.useState(null);

  const handleSearch = () => {
    if (searchValue) {
      navigate(`/ticker/${searchValue.symbol}`);
      setSearchValue(null);
    }
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          Bias-Aware Stock News
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
          <Autocomplete
            id="ticker-search"
            options={mockTickers}
            getOptionLabel={(option) => `${option.symbol} - ${option.name}`}
            value={searchValue}
            onChange={(event, newValue) => {
              setSearchValue(newValue);
            }}
            sx={{ width: 300 }}
            renderInput={(params) => (
              <TextField 
                {...params} 
                label="Search Ticker" 
                variant="outlined" 
                size="small"
                sx={{ bgcolor: 'white', borderRadius: 1 }}
              />
            )}
          />
          <IconButton 
            color="inherit" 
            onClick={handleSearch}
            disabled={!searchValue}
          >
            <SearchIcon />
          </IconButton>
        </Box>
        
        <Button color="inherit" onClick={() => navigate('/portfolio')}>
          Portfolio
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
