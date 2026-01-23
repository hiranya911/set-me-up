# Testing Guide

This document outlines the testing strategy and best practices for this project.

## Overview

Testing is a critical part of our development process. This guide covers the different types of tests we use and how to run them.

## Types of Tests

### Unit Tests

Unit tests verify individual components in isolation. They should be:
- Fast to execute
- Independent from each other
- Easy to understand

### Integration Tests

Integration tests verify that different components work together correctly.

### End-to-End Tests

E2E tests verify complete user workflows from start to finish.

## Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Best Practices

1. **Write tests first**: Consider using TDD (Test-Driven Development)
2. **Keep tests simple**: Each test should verify one thing
3. **Use descriptive names**: Test names should clearly state what they verify
4. **Maintain test isolation**: Tests should not depend on each other
5. **Mock external dependencies**: Use mocks/stubs for external services

## Continuous Integration

All tests run automatically on every pull request. PRs must pass all tests before merging.

## Coverage Goals

We aim for at least 80% code coverage across the project.
