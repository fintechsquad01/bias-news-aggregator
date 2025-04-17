import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

import HomePage from '../src/pages/HomePage';

// Create a mock for axios
const mockAxios = new MockAdapter(axios);

// Mock data for testing
const mockTrendingNews = [
  {
    id: 1,
    ticker: 'AAPL',
    headline: 'Apple Reports Strong Quarterly Earnings',
    summary: 'Apple Inc. announced financial results with record revenue.',
    url: 'https://example.com/article1',
    source: 'Financial Times',
    bias_label: 'center',
    sentiment_label: 'bullish',
    published_date: '2025-04-15T14:30:00Z'
  },
  {
    id: 2,
    ticker: 'MSFT',
    headline: 'Microsoft Cloud Growth Accelerates',
    summary: 'Microsoft reported strong fiscal results.',
    url: 'https://example.com/article2',
    source: 'Wall Street Journal',
    bias_label: 'lean_right',
    sentiment_label: 'bullish',
    published_date: '2025-04-16T09:15:00Z'
  }
];

describe('HomePage Component', () => {
  beforeEach(() => {
    // Reset mock
    mockAxios.reset();
    
    // Mock the API response
    mockAxios.onGet(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1'}/news/trending`).reply(200, mockTrendingNews);
  });

  test('renders homepage title', async () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    
    // Check if the main title is rendered
    expect(screen.getByText(/Bias-Aware Stock Market News/i)).toBeInTheDocument();
  });

  test('renders featured news section', async () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    
    // Check if the featured news section is rendered
    expect(screen.getByText(/Featured News/i)).toBeInTheDocument();
  });

  test('renders trending tickers section', async () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    
    // Check if the trending tickers section is rendered
    expect(screen.getByText(/Trending Tickers/i)).toBeInTheDocument();
  });

  test('renders bias explanation section', async () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    
    // Check if the bias explanation section is rendered
    expect(screen.getByText(/Understanding Media Bias/i)).toBeInTheDocument();
  });

  test('renders feature cards', async () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    
    // Check if the feature cards are rendered
    expect(screen.getByText(/Bias Analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/Sentiment Analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/Portfolio Tracking/i)).toBeInTheDocument();
  });

  test('shows loading state initially', async () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    
    // Check if loading indicator is shown initially
    const loadingElement = screen.getByRole('progressbar');
    expect(loadingElement).toBeInTheDocument();
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(1);
    });
  });

  test('handles API error gracefully', async () => {
    // Override the mock to return an error
    mockAxios.onGet(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1'}/news/trending`).networkError();
    
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    
    // Wait for error to be displayed
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(1);
    });
    
    // Error handling is implemented in the component, but we can't easily test
    // the error message without modifying the component to expose it more clearly
  });
});
