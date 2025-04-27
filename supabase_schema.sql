-- Bias-Aware News Aggregator - Supabase Database Schema
-- Run this SQL in the Supabase SQL Editor to set up your database schema

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================
-- News Sources Table
-- ==============================================
CREATE TABLE IF NOT EXISTS news_sources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  domain TEXT NOT NULL UNIQUE,
  description TEXT,
  bias_label TEXT NOT NULL CHECK (bias_label IN ('left', 'lean_left', 'center', 'lean_right', 'right')),
  bias_score DECIMAL(3,2) NOT NULL, -- Range from -1.0 (left) to 1.0 (right)
  logo_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS news_sources_bias_label_idx ON news_sources(bias_label);
CREATE INDEX IF NOT EXISTS news_sources_domain_idx ON news_sources(domain);

-- ==============================================
-- Tickers Table
-- ==============================================
CREATE TABLE IF NOT EXISTS tickers (
  symbol TEXT PRIMARY KEY,
  company_name TEXT NOT NULL,
  exchange TEXT,
  sector TEXT,
  industry TEXT,
  market_cap BIGINT,
  description TEXT,
  website_url TEXT,
  logo_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS tickers_sector_idx ON tickers(sector);

-- ==============================================
-- News Articles Table
-- ==============================================
CREATE TABLE IF NOT EXISTS news_articles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  headline TEXT NOT NULL,
  summary TEXT,
  content TEXT,
  url TEXT NOT NULL UNIQUE,
  image_url TEXT,
  published_date TIMESTAMPTZ NOT NULL,
  source_id UUID NOT NULL REFERENCES news_sources(id) ON DELETE CASCADE,
  author TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS news_articles_published_date_idx ON news_articles(published_date DESC);
CREATE INDEX IF NOT EXISTS news_articles_source_id_idx ON news_articles(source_id);

-- ==============================================
-- Article-Ticker Junction Table
-- ==============================================
CREATE TABLE IF NOT EXISTS article_tickers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  article_id UUID NOT NULL REFERENCES news_articles(id) ON DELETE CASCADE,
  ticker_symbol TEXT NOT NULL REFERENCES tickers(symbol) ON DELETE CASCADE,
  relevance_score DECIMAL(3,2), -- Optional relevance score (0.0-1.0)
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(article_id, ticker_symbol)
);

CREATE INDEX IF NOT EXISTS article_tickers_ticker_symbol_idx ON article_tickers(ticker_symbol);
CREATE INDEX IF NOT EXISTS article_tickers_article_id_idx ON article_tickers(article_id);

-- ==============================================
-- Sentiment Analysis Table
-- ==============================================
CREATE TABLE IF NOT EXISTS sentiment_analysis (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  article_id UUID NOT NULL REFERENCES news_articles(id) ON DELETE CASCADE,
  sentiment_label TEXT NOT NULL CHECK (sentiment_label IN ('bullish', 'bearish', 'neutral')),
  sentiment_score DECIMAL(4,3) NOT NULL, -- Range from -1.0 (bearish) to 1.0 (bullish)
  confidence DECIMAL(3,2), -- Confidence of the sentiment analysis (0.0-1.0)
  analyzed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(article_id)
);

CREATE INDEX IF NOT EXISTS sentiment_analysis_sentiment_label_idx ON sentiment_analysis(sentiment_label);
CREATE INDEX IF NOT EXISTS sentiment_analysis_analyzed_at_idx ON sentiment_analysis(analyzed_at DESC);

-- ==============================================
-- User Profiles Table (extends Supabase auth.users)
-- ==============================================
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  bio TEXT,
  avatar_url TEXT,
  preferences JSONB DEFAULT '{}'::JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================
-- User Portfolios Table
-- ==============================================
CREATE TABLE IF NOT EXISTS portfolios (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  is_public BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, name)
);

CREATE INDEX IF NOT EXISTS portfolios_user_id_idx ON portfolios(user_id);

-- ==============================================
-- Portfolio-Ticker Junction Table
-- ==============================================
CREATE TABLE IF NOT EXISTS portfolio_tickers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
  ticker_symbol TEXT NOT NULL REFERENCES tickers(symbol) ON DELETE CASCADE,
  weight DECIMAL(5,2), -- Optional weighting for the ticker in portfolio (percentage)
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(portfolio_id, ticker_symbol)
);

CREATE INDEX IF NOT EXISTS portfolio_tickers_portfolio_id_idx ON portfolio_tickers(portfolio_id);
CREATE INDEX IF NOT EXISTS portfolio_tickers_ticker_symbol_idx ON portfolio_tickers(ticker_symbol);

-- ==============================================
-- Materialized Views for Analysis
-- ==============================================

-- Bias Distribution by Ticker and Date
CREATE MATERIALIZED VIEW IF NOT EXISTS bias_analysis_mv AS
SELECT 
  t.symbol AS ticker_symbol,
  DATE_TRUNC('day', na.published_date) AS date,
  ns.bias_label,
  COUNT(DISTINCT na.id) AS article_count
FROM 
  tickers t
  JOIN article_tickers at ON t.symbol = at.ticker_symbol
  JOIN news_articles na ON at.article_id = na.id
  JOIN news_sources ns ON na.source_id = ns.id
WHERE 
  na.published_date >= NOW() - INTERVAL '90 days'
GROUP BY 
  t.symbol, DATE_TRUNC('day', na.published_date), ns.bias_label
WITH DATA;

CREATE UNIQUE INDEX IF NOT EXISTS bias_analysis_mv_unique_idx 
  ON bias_analysis_mv(ticker_symbol, date, bias_label);

-- Sentiment Distribution by Ticker and Date
CREATE MATERIALIZED VIEW IF NOT EXISTS sentiment_analysis_mv AS
SELECT 
  t.symbol AS ticker_symbol,
  DATE_TRUNC('day', na.published_date) AS date,
  sa.sentiment_label,
  COUNT(DISTINCT na.id) AS analysis_count
FROM 
  tickers t
  JOIN article_tickers at ON t.symbol = at.ticker_symbol
  JOIN news_articles na ON at.article_id = na.id
  JOIN sentiment_analysis sa ON na.id = sa.article_id
WHERE 
  na.published_date >= NOW() - INTERVAL '90 days'
GROUP BY 
  t.symbol, DATE_TRUNC('day', na.published_date), sa.sentiment_label
WITH DATA;

CREATE UNIQUE INDEX IF NOT EXISTS sentiment_analysis_mv_unique_idx 
  ON sentiment_analysis_mv(ticker_symbol, date, sentiment_label);

-- ==============================================
-- Functions
-- ==============================================

-- Function to refresh materialized views
CREATE OR REPLACE FUNCTION refresh_analysis_views()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY bias_analysis_mv;
  REFRESH MATERIALIZED VIEW CONCURRENTLY sentiment_analysis_mv;
END;
$$ LANGUAGE plpgsql;

-- Function to get trending tickers based on article count
CREATE OR REPLACE FUNCTION get_trending_tickers(p_days INTEGER DEFAULT 1, p_limit INTEGER DEFAULT 10)
RETURNS TABLE (
  ticker_symbol TEXT,
  company_name TEXT,
  article_count BIGINT,
  bullish_percentage DECIMAL(5,2),
  bearish_percentage DECIMAL(5,2),
  neutral_percentage DECIMAL(5,2)
) AS $$
BEGIN
  RETURN QUERY
  WITH article_counts AS (
    SELECT 
      t.symbol,
      t.company_name,
      COUNT(DISTINCT na.id) AS total_articles
    FROM 
      tickers t
      JOIN article_tickers at ON t.symbol = at.ticker_symbol
      JOIN news_articles na ON at.article_id = na.id
    WHERE 
      na.published_date >= NOW() - (p_days || ' days')::INTERVAL
    GROUP BY 
      t.symbol, t.company_name
    ORDER BY 
      COUNT(DISTINCT na.id) DESC
    LIMIT p_limit
  ),
  sentiment_counts AS (
    SELECT 
      t.symbol,
      sa.sentiment_label,
      COUNT(DISTINCT na.id) AS label_count
    FROM 
      tickers t
      JOIN article_tickers at ON t.symbol = at.ticker_symbol
      JOIN news_articles na ON at.article_id = na.id
      JOIN sentiment_analysis sa ON na.id = sa.article_id
    WHERE 
      na.published_date >= NOW() - (p_days || ' days')::INTERVAL
      AND t.symbol IN (SELECT symbol FROM article_counts)
    GROUP BY 
      t.symbol, sa.sentiment_label
  )
  SELECT 
    ac.symbol,
    ac.company_name,
    ac.total_articles,
    COALESCE(ROUND((CAST(bullish.label_count AS DECIMAL) / ac.total_articles) * 100, 2), 0) AS bullish_percentage,
    COALESCE(ROUND((CAST(bearish.label_count AS DECIMAL) / ac.total_articles) * 100, 2), 0) AS bearish_percentage,
    COALESCE(ROUND((CAST(neutral.label_count AS DECIMAL) / ac.total_articles) * 100, 2), 0) AS neutral_percentage
  FROM 
    article_counts ac
    LEFT JOIN sentiment_counts bullish ON ac.symbol = bullish.symbol AND bullish.sentiment_label = 'bullish'
    LEFT JOIN sentiment_counts bearish ON ac.symbol = bearish.symbol AND bearish.sentiment_label = 'bearish'
    LEFT JOIN sentiment_counts neutral ON ac.symbol = neutral.symbol AND neutral.sentiment_label = 'neutral'
  ORDER BY 
    ac.total_articles DESC;
END;
$$ LANGUAGE plpgsql;

-- ==============================================
-- Row Level Security (RLS) Policies
-- ==============================================

-- Enable RLS on tables that need access control
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolios ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_tickers ENABLE ROW LEVEL SECURITY;

-- Policy for user profiles (users can only read/update their own profile)
CREATE POLICY user_profiles_select_policy 
  ON user_profiles FOR SELECT 
  USING (auth.uid() = id);

CREATE POLICY user_profiles_update_policy 
  ON user_profiles FOR UPDATE 
  USING (auth.uid() = id);

-- Policies for portfolios 
-- Users can read their own portfolios or public portfolios
CREATE POLICY portfolios_select_policy 
  ON portfolios FOR SELECT 
  USING (auth.uid() = user_id OR is_public = true);

-- Users can only insert/update/delete their own portfolios
CREATE POLICY portfolios_insert_policy 
  ON portfolios FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY portfolios_update_policy 
  ON portfolios FOR UPDATE 
  USING (auth.uid() = user_id);

CREATE POLICY portfolios_delete_policy 
  ON portfolios FOR DELETE 
  USING (auth.uid() = user_id);

-- Policies for portfolio_tickers
-- Users can read tickers in their own portfolios or public portfolios
CREATE POLICY portfolio_tickers_select_policy 
  ON portfolio_tickers FOR SELECT 
  USING (EXISTS (
    SELECT 1 FROM portfolios 
    WHERE id = portfolio_tickers.portfolio_id 
    AND (user_id = auth.uid() OR is_public = true)
  ));

-- Users can only insert/update/delete tickers in their own portfolios
CREATE POLICY portfolio_tickers_insert_policy 
  ON portfolio_tickers FOR INSERT 
  WITH CHECK (EXISTS (
    SELECT 1 FROM portfolios 
    WHERE id = portfolio_tickers.portfolio_id 
    AND user_id = auth.uid()
  ));

CREATE POLICY portfolio_tickers_update_policy 
  ON portfolio_tickers FOR UPDATE 
  USING (EXISTS (
    SELECT 1 FROM portfolios 
    WHERE id = portfolio_tickers.portfolio_id 
    AND user_id = auth.uid()
  ));

CREATE POLICY portfolio_tickers_delete_policy 
  ON portfolio_tickers FOR DELETE 
  USING (EXISTS (
    SELECT 1 FROM portfolios 
    WHERE id = portfolio_tickers.portfolio_id 
    AND user_id = auth.uid()
  ));

-- ==============================================
-- Triggers
-- ==============================================

-- Trigger to update the updated_at timestamp
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for all tables with updated_at column
CREATE TRIGGER set_news_sources_updated_at
  BEFORE UPDATE ON news_sources
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER set_tickers_updated_at
  BEFORE UPDATE ON tickers
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER set_news_articles_updated_at
  BEFORE UPDATE ON news_articles
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER set_user_profiles_updated_at
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER set_portfolios_updated_at
  BEFORE UPDATE ON portfolios
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ==============================================
-- Sample Data (optional, uncomment to include)
-- ==============================================

/*
-- Insert sample news sources with bias ratings
INSERT INTO news_sources (name, domain, description, bias_label, bias_score, logo_url) VALUES
('Wall Street Journal', 'wsj.com', 'Financial and business news', 'lean_right', 0.4, 'https://example.com/logos/wsj.png'),
('Reuters', 'reuters.com', 'International news organization', 'center', 0.0, 'https://example.com/logos/reuters.png'),
('CNBC', 'cnbc.com', 'Business and financial market news', 'lean_left', -0.2, 'https://example.com/logos/cnbc.png'),
('Bloomberg', 'bloomberg.com', 'Business and market news', 'center', 0.1, 'https://example.com/logos/bloomberg.png'),
('Fox Business', 'foxbusiness.com', 'Business news and financial information', 'right', 0.8, 'https://example.com/logos/foxbusiness.png'),
('MSNBC', 'msnbc.com', 'Political and financial news', 'left', -0.8, 'https://example.com/logos/msnbc.png');

-- Insert sample tickers
INSERT INTO tickers (symbol, company_name, exchange, sector, industry, market_cap) VALUES
('AAPL', 'Apple Inc.', 'NASDAQ', 'Technology', 'Consumer Electronics', 2600000000000),
('MSFT', 'Microsoft Corporation', 'NASDAQ', 'Technology', 'Software', 2400000000000),
('GOOGL', 'Alphabet Inc.', 'NASDAQ', 'Technology', 'Internet Content & Information', 1800000000000),
('AMZN', 'Amazon.com Inc.', 'NASDAQ', 'Technology', 'Internet Retail', 1700000000000),
('TSLA', 'Tesla, Inc.', 'NASDAQ', 'Consumer Discretionary', 'Auto Manufacturers', 800000000000);
*/

-- ==============================================
-- Set up scheduled refresh of materialized views
-- ==============================================

-- Uncomment and run this in the Supabase Dashboard > Database > Functions section
/*
SELECT
  cron.schedule(
    'refresh-analysis-views',  -- Name of the schedule
    '0 */4 * * *',             -- Cron expression (every 4 hours)
    'SELECT refresh_analysis_views()'
  );
*/ 