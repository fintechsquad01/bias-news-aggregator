#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('Debugging Vercel Deployment Issues');
console.log('==================================');

// Check for vercel.json
try {
  const vercelJsonPath = path.join(process.cwd(), 'vercel.json');
  if (fs.existsSync(vercelJsonPath)) {
    const vercelJson = require(vercelJsonPath);
    console.log('✅ vercel.json exists');
    
    // Validate vercel.json structure
    if (!vercelJson.version) {
      console.log('❌ vercel.json is missing "version" field');
    }
    
    if (!vercelJson.builds || !Array.isArray(vercelJson.builds) || vercelJson.builds.length === 0) {
      console.log('❌ vercel.json is missing or has empty "builds" array');
    }
    
    if (!vercelJson.routes || !Array.isArray(vercelJson.routes) || vercelJson.routes.length === 0) {
      console.log('❌ vercel.json is missing or has empty "routes" array');
    }
  } else {
    console.log('❌ vercel.json does not exist');
  }
} catch (error) {
  console.log(`❌ Error checking vercel.json: ${error.message}`);
}

// Check for vite.config.js
try {
  const viteConfigPath = path.join(process.cwd(), 'frontend', 'vite.config.js');
  if (fs.existsSync(viteConfigPath)) {
    const viteConfig = fs.readFileSync(viteConfigPath, 'utf8');
    console.log('✅ frontend/vite.config.js exists');
    
    // Check if it's JavaScript, not JSON
    if (viteConfig.includes('"plugins":') && !viteConfig.includes('export default')) {
      console.log('❌ vite.config.js appears to be in JSON format instead of JavaScript');
    }
  } else {
    console.log('❌ frontend/vite.config.js does not exist');
  }
} catch (error) {
  console.log(`❌ Error checking vite.config.js: ${error.message}`);
}

// Check for index.html
try {
  const indexHtmlPath = path.join(process.cwd(), 'frontend', 'index.html');
  if (fs.existsSync(indexHtmlPath)) {
    console.log('✅ frontend/index.html exists');
    
    // Check if it has root div
    const indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');
    if (!indexHtml.includes('id="root"')) {
      console.log('❌ frontend/index.html is missing div with id="root"');
    }
  } else {
    console.log('❌ frontend/index.html does not exist');
  }
} catch (error) {
  console.log(`❌ Error checking index.html: ${error.message}`);
}

// Check for backend main.py
try {
  const mainPyPath = path.join(process.cwd(), 'backend', 'app', 'main.py');
  if (fs.existsSync(mainPyPath)) {
    console.log('✅ backend/app/main.py exists');
  } else {
    console.log('❌ backend/app/main.py does not exist');
  }
} catch (error) {
  console.log(`❌ Error checking main.py: ${error.message}`);
}

// Check for package.json
try {
  const packageJsonPath = path.join(process.cwd(), 'frontend', 'package.json');
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = require(packageJsonPath);
    console.log('✅ frontend/package.json exists');
    
    // Check build script
    if (!packageJson.scripts || !packageJson.scripts.build) {
      console.log('❌ frontend/package.json is missing "build" script');
    }
    
    // Check for Vite dependency
    const hasVite = packageJson.dependencies?.vite || packageJson.devDependencies?.vite;
    if (!hasVite) {
      console.log('❌ frontend/package.json is missing Vite dependency');
    }
  } else {
    console.log('❌ frontend/package.json does not exist');
  }
} catch (error) {
  console.log(`❌ Error checking package.json: ${error.message}`);
}

// Check for requirements.txt
try {
  const requirementsPath = path.join(process.cwd(), 'backend', 'requirements.txt');
  if (fs.existsSync(requirementsPath)) {
    console.log('✅ backend/requirements.txt exists');
  } else {
    console.log('❌ backend/requirements.txt does not exist');
  }
} catch (error) {
  console.log(`❌ Error checking requirements.txt: ${error.message}`);
}

// Check Vercel CLI installation
try {
  const vercelVersion = execSync('vercel --version').toString().trim();
  console.log(`✅ Vercel CLI is installed (${vercelVersion})`);
} catch (error) {
  console.log('❌ Vercel CLI is not installed or not in PATH');
}

console.log('\nDeployment Recommendations:');
console.log('1. Fix any issues marked with ❌');
console.log('2. Run "vercel" locally to test deployment');
console.log('3. Check deployment logs with "vercel logs <deployment-url>"');
console.log('4. For production deployment, use "vercel --prod"'); 