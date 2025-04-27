{
  "version": 2,
  "builds": [
    {
      "src": "backend/app/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "installCommand": "npm ci --prefix frontend --include=dev",
        "buildCommand": "npm run build --prefix frontend",
        "distDir": "frontend/dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/app/main.py"
    },
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/dist/index.html"
    }
  ],
  "env": {
    "NPM_CONFIG_PRODUCTION": "false"
  }
}
