import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

import TickerPage from '../src/pages/TickerPage';

// Create a mock for axios
const mockAxios = new MockAdapter(axios);

// Mock data for testing
const mockTickerAnalysis = {
  ticker: 'AAPL',
  days: 7,
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
    is_biased: false
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
    overall_sentiment: 'bullish'
  },
  diversity_warning: null,
  sentiment_summary: 'News sentiment for AAPL is predominantly bullish (50.0% positive) over the past 7 days.'
};

const mockNewsArticles = [
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
    ticker: 'AAPL',
    headline: 'Apple Faces Regulatory Scrutiny',
    summary: 'Regulators are examining Apple\'s latest product.',
    url: 'https://example.com/article2',
    source: 'Wall Street Journal',
    bias_label: 'lean_right',
    sentiment_label: 'bearish',
    published_date: '2025-04-16T09:15:00Z'
  }
];

// Mock the useParams hook
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({
    symbol: 'AAPL'
  })
}));

describe('TickerPage Component', () => {
  beforeEach(() => {
    // Reset mock
    mockAxios.reset();
    
    // Mock the API responses
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';
    mockAxios.onGet(`${API_BASE_URL}/analysis/ticker/AAPL/analysis`).reply(200, mockTickerAnalysis);
    mockAxios.onGet(`${API_BASE_URL}/news?ticker=AAPL&limit=10`).reply(200, mockNewsArticles);
  });

  test('renders ticker information', async () => {
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
    
    // Check if ticker symbol is rendered
    expect(screen.getByText('AAPL')).toBeInTheDocument();
    expect(screen.getByText('Apple Inc.')).toBeInTheDocument();
  });

  test('renders bias distribution chart', async () => {
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
    
    // Check if bias distribution section is rendered
    expect(screen.getByText('Bias Distribution (Last 7 Days)')).toBeInTheDocument();
  });

  test('renders sentiment distribution chart', async () => {
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
    
    // Check if sentiment distribution section is rendered
    expect(screen.getByText('Sentiment Distribution (Last 7 Days)')).toBeInTheDocument();
  });

  test('renders news articles', async () => {
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
    
    // Check if news articles are rendered
    expect(screen.getByText('Recent News')).toBeInTheDocument();
    expect(screen.getByText('Apple Reports Strong Quarterly Earnings')).toBeInTheDocument();
    expect(screen.getByText('Apple Faces Regulatory Scrutiny')).toBeInTheDocument();
  });

  test('renders bias explanation', async () => {
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
    
    // Check if bias explanation is rendered
    expect(screen.getByText('About Bias Analysis')).toBeInTheDocument();
  });

  test('renders sentiment explanation', async () => {
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
    
    // Check if sentiment explanation is rendered
    expect(screen.getByText('About Sentiment Analysis')).toBeInTheDocument();
  });

  test('shows loading state initially', async () => {
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Check if loading indicator is shown initially
    const loadingElement = screen.getByRole('progressbar');
    expect(loadingElement).toBeInTheDocument();
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
  });

  test('displays diversity warning when present', async () => {
    // Override the mock to include a diversity warning
    const warningAnalysis = {
      ...mockTickerAnalysis,
      diversity_warning: 'Warning: News coverage for AAPL is predominantly from left sources (66.6%).'
    };
    
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';
    mockAxios.onGet(`${API_BASE_URL}/analysis/ticker/AAPL/analysis`).reply(200, warningAnalysis);
    
    render(
      <BrowserRouter>
        <TickerPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(mockAxios.history.get.length).toBe(2);
    });
    
    // Check if warning is displayed
    expect(screen.getByText(/predominantly from left sources/i)).toBeInTheDocument();
  });
});
