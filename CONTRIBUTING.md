# Contributing to Docker Tutorial

Thank you for your interest in contributing to this Docker tutorial! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

- Check if the issue already exists
- Provide clear description and steps to reproduce
- Include Docker version information if relevant

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes following our standards
4. Test your changes
5. Commit with clear messages
6. Push to your fork
7. Submit a pull request

## Documentation Standards

### Markdown Formatting

- Use `#` for title, `##` for major sections, `###` for subsections
- Use fenced code blocks with language tags (```bash, ```dockerfile, ```yaml)
- Use admonitions for tips and warnings:
  - `> **Note:** Important information`
  - `> **Warning:** Critical warnings`
  - `> **Tip:** Helpful suggestions`
- Use consistent bullet markers (-)
- Include cross-references to related sections

### Docker Syntax

All examples must use modern Docker syntax:

- Use `docker compose` (not `docker-compose`)
- Use `--mount` instead of `-v` for volume mounts
- Use BuildKit features where applicable
- Use Compose v2 syntax in compose.yaml files
- Avoid deprecated commands and flags

### Content Structure

Each tutorial document should include:

- Clear title and overview
- Prerequisites section (if applicable)
- Main content with practical examples
- Code snippets with explanations
- Summary or next steps
- Links to related topics

## Code Example Requirements

### Dockerfile Examples

- Must build successfully without errors
- Include comments explaining key concepts
- Follow best practices (multi-stage builds, layer optimization)
- Use modern syntax and instructions

### Compose Examples

- Must use compose.yaml (not docker-compose.yml)
- Must start successfully with `docker compose up`
- Include comments explaining configuration
- Use Compose v2 features

### Example Structure

Each example directory should contain:

- README.md explaining the example
- All necessary files (Dockerfile, compose.yaml, app code)
- Clear instructions for running the example

## Style Guide

- Write for developers who know Linux basics but are new to Docker
- Use clear, concise language
- Provide practical, working examples
- Explain the "why" behind best practices
- Keep examples minimal and focused

## Testing Your Changes

Before submitting:

1. Verify all markdown files render correctly
2. Test all code examples build and run
3. Check all internal links work
4. Ensure modern Docker syntax throughout
5. Verify difficulty levels are appropriate

## Questions?

If you have questions about contributing, please open an issue for discussion.

Thank you for helping make this tutorial better!
