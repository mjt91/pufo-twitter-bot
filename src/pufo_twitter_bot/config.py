"""Configuration module for environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent

    # Try to load .env file from project root
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # If no .env file exists, try to load from current directory
        load_dotenv()

    # Verify required environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            "Please set them in your .env file or environment."
        )


# Load environment variables when module is imported
load_env()
