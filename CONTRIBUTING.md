# Contributing Guide

This document provides guidelines for contributing to the Bias-Aware U.S. Stock Market News Aggregator project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. By participating, you are expected to uphold this code.

- Be respectful and inclusive
- Be collaborative
- Be open to constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/bias-news-aggregator.git`
3. Set up the development environment as described in the README.md
4. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name`

## Development Workflow

1. **Choose an issue**: Start by selecting an open issue from the issue tracker or create a new one.
2. **Discuss**: For significant changes, open an issue for discussion before starting work.
3. **Branch**: Create a feature branch from the `develop` branch.
4. **Develop**: Make your changes, following the coding standards.
5. **Test**: Ensure all tests pass and add new tests for your changes.
6. **Document**: Update documentation as needed.
7. **Commit**: Make atomic commits with clear messages.
8. **Pull Request**: Submit a pull request to the `develop` branch.

## Coding Standards

### Backend (Python)

- Follow PEP 8 style guide
- Use type hints
- Document functions and classes with docstrings
- Maximum line length of 100 characters
- Use meaningful variable and function names

Example:
```python
def get_news_by_ticker(
    db: Session, 
    ticker: str, 
    limit: int = 20, 
    offset: int = 0
) -> List[Article]:
    """
    Retrieve news articles for a specific ticker.
    
    Args:
        db: Database session
        ticker: Stock ticker symbol
        limit: Maximum number of articles to return
        offset: Number of articles to skip
        
    Returns:
        List of Article objects
    """
    return db.query(Article).filter(Article.ticker == ticker).offset(offset).limit(limit).all()
```

### Frontend (JavaScript/React)

- Follow Airbnb JavaScript Style Guide
- Use functional components with hooks
- Use PropTypes for component props
- Use meaningful component and variable names
- Use CSS-in-JS with styled-components or Material UI styling

Example:
```jsx
import React from 'react';
import PropTypes from 'prop-types';
import { Typography, Box } from '@mui/material';

const BiasLegend = ({ showTitle = true }) => {
  return (
    <Box>
      {showTitle && (
        <Typography variant="subtitle2" gutterBottom>
          Bias Categories
        </Typography>
      )}
      <Box display="flex" flexDirection="column" gap={1}>
        <Box display="flex" alignItems="center">
          <Box width={16} height={16} bgcolor="error.main" mr={1} borderRadius={1} />
          <Typography variant="body2">Left</Typography>
        </Box>
        {/* Additional categories */}
      </Box>
    </Box>
  );
};

BiasLegend.propTypes = {
  showTitle: PropTypes.bool
};

export default BiasLegend;
```

## Testing

### Backend Testing

- Write unit tests for all services and API endpoints
- Use pytest for testing
- Aim for at least 80% code coverage
- Mock external dependencies

### Frontend Testing

- Write unit tests for components using React Testing Library
- Test component rendering and interactions
- Mock API calls using axios-mock-adapter or similar

## Documentation

- Update README.md with any new features or changes
- Document all API endpoints in api.md
- Update user-guide.md for user-facing changes
- Add inline comments for complex logic
- Update project-structure.md when adding new files or directories

## Pull Request Process

1. Ensure your code follows the coding standards
2. Update documentation as needed
3. Add or update tests as needed
4. Make sure all tests pass
5. Submit a pull request to the `develop` branch
6. Request a review from a maintainer
7. Address any feedback from the review
8. Once approved, a maintainer will merge your pull request

## Versioning

This project uses Semantic Versioning (SemVer):

- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward-compatible manner
- PATCH version for backward-compatible bug fixes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
