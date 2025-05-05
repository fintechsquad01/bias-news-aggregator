#!/bin/bash

# Script to set up Vercel environment variables
# Make sure to run 'vercel login' before running this script

echo "Setting up Vercel environment variables..."

# Backend variables
vercel env add SUPABASE_URL
vercel env add SUPABASE_SERVICE_ROLE_KEY
vercel env add POLYGON_API_KEY
vercel env add FINANCIAL_DATASETS_API_KEY
vercel env add WHALEWISDOM_API_KEY
vercel env add FINNHUB_API_KEY
vercel env add JWT_SECRET
vercel env add CORS_ORIGINS
vercel env add NODE_ENV

# Frontend variables
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
vercel env add NEXT_PUBLIC_API_BASE_URL
vercel env add NEXT_PUBLIC_DEFAULT_TICKERS

echo "Environment variables setup complete!"
echo "Don't forget to run 'vercel --prod' to deploy with these variables." 