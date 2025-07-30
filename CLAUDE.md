# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI application that generates random German book titles with matching author names and optionally posts them to Twitter. The project uses ChatGPT integration for generating creative book-author pairs and includes multiple data sources for author name generation.

## Development Commands

### Testing and Quality Assurance

- `nox -s tests` - Run the full test suite across multiple Python versions
- `nox -s tests -- tests/test_specific.py` - Run specific test file
- `nox -s mypy` - Run type checking with mypy
- `nox -s pre-commit` - Run pre-commit linting (ruff, prettier, trailing whitespace checks)
- `nox -s coverage` - Generate coverage report
- `nox -s safety` - Scan dependencies for security vulnerabilities

### Documentation

- `nox -s docs-build` - Build documentation
- `nox -s docs` - Build and serve docs with live reloading

### Installation and Development

- Project uses modern Python packaging with pyproject.toml
- Install in development mode: `pip install -e .`
- Install with dev dependencies: `pip install -e .[dev]`

## Architecture

### Core Structure

- **Entry Point**: `src/pufo_twitter_bot/__main__.py` - CLI interface using Click
- **Models**: `src/pufo_twitter_bot/models.py` - Pydantic models for Author and Book
- **Authors Module**: `src/pufo_twitter_bot/authors/` - Author name generation from multiple sources
  - `opendatanames.py` - Uses local CSV data from Cologne open data
  - `randomnames.py` - Web scraping approach (legacy)
- **Books Module**: `src/pufo_twitter_bot/books/` - Book title generation
  - `chatgpt_generator.py` - ChatGPT API integration (primary method)
  - `randombuch.py` - Web scraping approach (legacy, site is down)
- **Bot Module**: `src/pufo_twitter_bot/bot/twitter.py` - Twitter API integration
- **Config**: `src/pufo_twitter_bot/config.py` - Environment variable management

### Data Sources

- Local CSV files with German first names from Cologne municipal data
- Text file with German last names
- ChatGPT API for creative German book titles
- Twitter API for posting generated content

### Key Dependencies

- **CLI**: Click for command-line interface
- **HTTP**: requests for API calls
- **Data Processing**: pydantic for data models, marshmallow for serialization
- **AI Integration**: openai for ChatGPT API
- **Social Media**: tweepy for Twitter integration
- **Environment**: python-dotenv for configuration

## Environment Configuration

The application requires environment variables:

- `OPENAI_API_KEY` - Required for ChatGPT book generation
- Twitter API credentials for posting functionality

## Testing Strategy

- Uses pytest for testing framework
- Tests are organized by module in `tests/` directory
- Includes test data files for consistent testing
- Coverage reporting with coverage.py
- Type checking with mypy (strict configuration)

## Code Quality

- **Linting**: Uses ruff (modern Python linter/formatter)
- **Type Checking**: mypy with strict settings in mypy.ini
- **Pre-commit**: Automated code quality checks
- **Formatting**: ruff format (Black-compatible)
- **Documentation**: Sphinx for documentation generation

## CLI Usage

Primary command: `pufo-twitter-bot --count 5 --gender a --tweet`

- `--count`: Number of book-author pairs to generate
- `--gender`: Gender filter for author names (m/f/a for all)
- `--tweet`: Whether to post results to Twitter
