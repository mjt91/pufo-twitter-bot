# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI application that generates random German book titles with matching author names and optionally posts them to Twitter. The project uses ChatGPT integration for generating creative book-author pairs and includes multiple data sources for author name generation.

**Python Support**: 3.8-3.9 (testing via nox)

## Development Commands

### Testing and Quality Assurance

- `nox -s tests` - Run the full test suite across Python 3.8 and 3.9
- `nox -s tests -- tests/test_specific.py` - Run specific test file
- `nox -s tests -- tests/test_file.py::test_function` - Run specific test function
- `nox -s mypy` - Run type checking with mypy (strict mode enabled)
- `nox -s pre-commit` - Run pre-commit linting (ruff, prettier, trailing whitespace checks)
- `nox -s coverage` - Generate coverage report (automatically runs after tests in interactive mode)
- `nox -s safety` - Scan dependencies for security vulnerabilities
- `nox -s typeguard` - Runtime type checking using Typeguard
- `nox -s xdoctest` - Run docstring examples

### Documentation

- `nox -s docs-build` - Build documentation
- `nox -s docs` - Build and serve docs with live reloading (opens browser automatically)

### Installation and Development

- Project uses modern Python packaging with pyproject.toml
- Install in development mode: `pip install -e .`
- Install with dev dependencies: Use `pip install -e .` and then install from `[dependency-groups]` section
- Docker deployment: `docker build -t pufo-bot . && docker run --env-file .env pufo-bot`

## Architecture

### Core Structure

- **Entry Point**: `src/pufo_twitter_bot/__main__.py` - CLI interface using Click
  - Combines ChatGPT-generated book titles with locally-generated author names
  - Handles the main flow: generate authors → generate books → print/tweet results
- **Models**: `src/pufo_twitter_bot/models.py` - Pydantic v2 models for Author and Book
  - Includes rich metadata fields (birth_date, nationality, biography, etc.)
  - Uses forward references for circular relationships
- **Authors Module**: `src/pufo_twitter_bot/authors/` - Author name generation from multiple sources
  - `opendatanames.py` - Primary method using local CSV data from Cologne open data
  - `randomnames.py` - Defines Author/AuthorList dataclasses (legacy web scraping, still used for models)
- **Books Module**: `src/pufo_twitter_bot/books/` - Book title generation
  - `chatgpt_generator.py` - **Primary method** using ChatGPT API (gpt-4.1-nano-2025-04-14)
  - `randombuch.py` - Legacy web scraping (deprecated, site is down)
- **Bot Module**: `src/pufo_twitter_bot/bot/twitter.py` - Twitter API integration
- **Config**: `src/pufo_twitter_bot/config.py` - Environment variable management

### Data Flow

1. CLI receives request for N book-author pairs with gender filter
2. Author names generated from local CSV data (`data/first-names.json`, `data/last-names.txt`)
3. Book titles generated via ChatGPT API (uses JSON mode for structured output)
4. Results combined and printed to stdout
5. Optionally posted to Twitter if `--tweet` flag is set

### Data Sources

- **Local files** (bundled in `src/pufo_twitter_bot/data/`):
  - `first-names.json` - German first names from Cologne municipal data with gender tags
  - `last-names.txt` - German last names
- **ChatGPT API** - Creative German book title generation
- **Twitter API** - Posting functionality (requires credentials)

### Key Dependencies

- **CLI**: Click for command-line interface
- **HTTP**: requests for API calls
- **Data Processing**: pydantic for data models, marshmallow + desert for serialization
- **AI Integration**: openai for ChatGPT API (primary book generation method)
- **Social Media**: tweepy for Twitter integration
- **Environment**: python-dotenv for configuration
- **Testing**: pytest with pytest-mock for unit testing

## Environment Configuration

The application requires environment variables (typically in `.env` file):

- `OPENAI_API_KEY` - **Required** for ChatGPT book generation
- Twitter API credentials - Required only if using `--tweet` flag

## Testing Strategy

- Uses pytest for testing framework
- Tests are organized by module in `tests/` directory
- Test fixtures in `tests/conftest.py`
- Includes test data files for consistent testing
- Coverage reporting with coverage.py (parallel mode enabled)
- Type checking with mypy using very strict configuration (see mypy.ini)
- All test sessions install package in editable mode first

## Code Quality

- **Linting**: ruff (modern Python linter/formatter replacing black/flake8)
- **Type Checking**: mypy with strict settings enabled (disallow_untyped_defs, disallow_any_generics, etc.)
- **Pre-commit**: Automated code quality checks via `.pre-commit-config.yaml`
  - ruff linter and formatter
  - prettier for non-Python files
  - trailing whitespace checks, YAML validation, large file detection
- **Formatting**: ruff format (Black-compatible)
- **Documentation**: Sphinx with RTD theme

## CLI Usage

Primary command: `pufo-twitter-bot --count 5 --gender a --tweet`

- `--count` / `-c`: Number of book-author pairs to generate (default: 5)
- `--gender` / `-g`: Gender filter for author names - `m` (male), `f` (female), `a` (all) (default: `a`)
- `--tweet` / `--no-tweet`: Whether to post results to Twitter (default: `--no-tweet`)

Output format: `1. 'Book Title' von Firstname Lastname`

## Conventions

### Code Style

- Follow PEP 8 conventions
- Use type hints for all functions and methods
- Maintain test coverage for new functionality
- Update docstrings when modifying functions

### Naming Conventions

- Use snake_case for functions and variables
- Use PascalCase for classes
- Prefix test functions with `test_`
- Use descriptive names that reflect purpose

### Commit Message Format

Follow conventional commits format:

```
<type>: <description>

[optional body]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `test`: Adding or modifying tests
- `docs`: Documentation changes
- `chore`: Maintenance tasks (deps, config, etc.)

## Commit Rules

**IMPORTANT:** When working on tasks that modify code, you should commit changes at logical breakpoints:

- Create atomic commits that represent complete, logical units of work
- Only commit files modified in the current task — never commit unrelated changes
- Use descriptive commit messages following the conventional commits format above
- Always include `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>` in commit messages
- If there are no changes to commit, skip the commit step
- Do not push unless explicitly asked by the user
