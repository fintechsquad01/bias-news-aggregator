#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('Fixing Common React/Vite Frontend Issues');
console.log('=======================================');

const frontendDir = path.join(process.cwd(), 'frontend');

// Check if we're in the project root
if (!fs.existsSync(frontendDir)) {
  console.log('❌ Not in project root directory. Please run this script from the project root.');
  process.exit(1);
}

// Fix 1: Check and fix vite.config.js
try {
  const viteConfigPath = path.join(frontendDir, 'vite.config.js');
  if (fs.existsSync(viteConfigPath)) {
    const viteConfig = fs.readFileSync(viteConfigPath, 'utf8');
    
    // Check if it's in JSON format instead of JS
    if (viteConfig.includes('"plugins":') && !viteConfig.includes('export default')) {
      console.log('🔧 Fixing vite.config.js (converting from JSON to JS format)...');
      
      // Create proper JS format
      const newConfig = `import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true
  },
  server: {
    port: 3000
  },
  define: {
    'process.env': process.env
  }
});`;
      
      fs.writeFileSync(viteConfigPath, newConfig);
      console.log('✅ Fixed vite.config.js');
    } else {
      console.log('✅ vite.config.js is in correct format');
    }
  } else {
    console.log('❌ vite.config.js does not exist');
  }
} catch (error) {
  console.log(`❌ Error fixing vite.config.js: ${error.message}`);
}

// Fix 2: Check and fix index.html
try {
  const indexHtmlPath = path.join(frontendDir, 'index.html');
  if (fs.existsSync(indexHtmlPath)) {
    const indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');
    
    // Check if it has root div
    if (!indexHtml.includes('id="root"')) {
      console.log('🔧 Fixing index.html (adding root div)...');
      
      // Create proper HTML
      const newHtml = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Bias-Aware News Aggregator</title>
    <meta name="description" content="A bias-aware U.S. stock market news aggregator that analyzes articles for ideological bias and market sentiment" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/index.js"></script>
  </body>
</html>`;
      
      fs.writeFileSync(indexHtmlPath, newHtml);
      console.log('✅ Fixed index.html');
    } else {
      console.log('✅ index.html has root div');
    }
  } else {
    console.log('❌ index.html does not exist, creating it...');
    
    // Create index.html
    const newHtml = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Bias-Aware News Aggregator</title>
    <meta name="description" content="A bias-aware U.S. stock market news aggregator that analyzes articles for ideological bias and market sentiment" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/index.js"></script>
  </body>
</html>`;
    
    fs.writeFileSync(indexHtmlPath, newHtml);
    console.log('✅ Created index.html');
  }
} catch (error) {
  console.log(`❌ Error fixing index.html: ${error.message}`);
}

// Fix 3: Check and fix index.js
try {
  const indexJsPath = path.join(frontendDir, 'src', 'index.js');
  if (fs.existsSync(indexJsPath)) {
    const indexJs = fs.readFileSync(indexJsPath, 'utf8');
    
    // Check for non-existent CSS import
    if (indexJs.includes("import './index.css'") && !fs.existsSync(path.join(frontendDir, 'src', 'index.css'))) {
      console.log('🔧 Fixing index.js (removing non-existent CSS import)...');
      
      // Remove the import
      const newIndexJs = indexJs.replace("import './index.css'", "// import './index.css' // File doesn't exist");
      
      fs.writeFileSync(indexJsPath, newIndexJs);
      console.log('✅ Fixed index.js');
    } else {
      console.log('✅ index.js has no issues with CSS imports');
    }
  } else {
    console.log('❌ src/index.js does not exist');
  }
} catch (error) {
  console.log(`❌ Error fixing index.js: ${error.message}`);
}

// Fix 4: Check package.json for required dependencies
try {
  const packageJsonPath = path.join(frontendDir, 'package.json');
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = require(packageJsonPath);
    
    let needsUpdate = false;
    let missingDeps = [];
    
    // Check for required dependencies
    const requiredDeps = {
      'react': '^18.2.0',
      'react-dom': '^18.2.0',
      'react-router-dom': '^6.11.1'
    };
    
    for (const [dep, version] of Object.entries(requiredDeps)) {
      if (!packageJson.dependencies?.[dep]) {
        needsUpdate = true;
        missingDeps.push(dep);
      }
    }
    
    // Check for required dev dependencies
    const requiredDevDeps = {
      '@vitejs/plugin-react': '^4.0.0',
      'vite': '^4.3.5'
    };
    
    for (const [dep, version] of Object.entries(requiredDevDeps)) {
      if (!packageJson.devDependencies?.[dep] && !packageJson.dependencies?.[dep]) {
        needsUpdate = true;
        missingDeps.push(dep);
      }
    }
    
    if (needsUpdate) {
      console.log(`❌ Missing dependencies: ${missingDeps.join(', ')}`);
      console.log('🔧 Please install missing dependencies with:');
      console.log(`cd ${frontendDir} && npm install ${missingDeps.join(' ')}`);
    } else {
      console.log('✅ All required dependencies are present');
    }
  } else {
    console.log('❌ package.json does not exist');
  }
} catch (error) {
  console.log(`❌ Error checking package.json: ${error.message}`);
}

console.log('\nFrontend Fix Recommendations:');
console.log('1. Address any remaining issues marked with ❌');
console.log('2. Test the frontend build with:');
console.log(`   cd ${frontendDir} && npm run build`);
console.log('3. If build succeeds, test the app with:');
console.log(`   cd ${frontendDir} && npm run preview`); 