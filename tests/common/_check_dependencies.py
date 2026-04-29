"""
External dependency checker for integration tests.

This module provides utilities to verify that external services (Qdrant, Ollama, Azure OpenAI)
are available before running integration tests that depend on them.
"""

import os

import requests


class DependencyError(Exception):
    """Raised when an external dependency is not available."""

    pass


def check_qdrant_availability(url: str = "http://localhost:6333", timeout: int = 5) -> bool:
    """
    Check if Qdrant vector database is available.

    Args:
        url: Qdrant server URL (default: http://localhost:6333)
        timeout: Connection timeout in seconds

    Returns:
        True if Qdrant is available, False otherwise

    Raises:
        DependencyError: If check fails with diagnostic info
    """
    try:
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200
    except requests.ConnectionError:
        raise DependencyError(
            f"❌ Qdrant not available at {url}. " "Please run: docker-compose up -d"
        )
    except requests.Timeout:
        raise DependencyError(
            f"❌ Qdrant connection timeout ({timeout}s) at {url}. "
            "Service may be starting, retry in a few seconds."
        )
    except Exception as e:
        raise DependencyError(f"❌ Qdrant check failed: {e}")


def check_ollama_availability(url: str = "http://localhost:11434", timeout: int = 5) -> bool:
    """
    Check if Ollama embedding service is available.

    Args:
        url: Ollama server URL (default: http://localhost:11434)
        timeout: Connection timeout in seconds

    Returns:
        True if Ollama is available, False otherwise

    Raises:
        DependencyError: If check fails with diagnostic info
    """
    try:
        response = requests.get(f"{url}/api/tags", timeout=timeout)
        return response.status_code == 200
    except requests.ConnectionError:
        raise DependencyError(
            f"❌ Ollama not available at {url}. "
            "Please ensure Ollama is running or install from: https://ollama.ai"
        )
    except requests.Timeout:
        raise DependencyError(
            f"❌ Ollama connection timeout ({timeout}s) at {url}. "
            "Service may be starting, retry in a few seconds."
        )
    except Exception as e:
        raise DependencyError(f"❌ Ollama check failed: {e}")


def check_azure_openai_availability() -> bool:
    """
    Check if Azure OpenAI credentials are configured.

    Required environment variables:
    - OPENAI_API_KEY
    - OPENAI_API_VERSION
    - OPENAI_API_BASE

    Returns:
        True if Azure OpenAI is configured

    Raises:
        DependencyError: If required environment variables are missing
    """
    required_vars = ["OPENAI_API_KEY", "OPENAI_API_VERSION", "OPENAI_API_BASE"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise DependencyError(
            f"❌ Azure OpenAI not configured. "
            f"Missing environment variables: {', '.join(missing)}"
        )

    return True


def check_all_services(
    qdrant_url: str = "http://localhost:6333",
    ollama_url: str = "http://localhost:11434",
    timeout: int = 5,
) -> dict[str, bool]:
    """
    Check availability of all integration test dependencies.

    Args:
        qdrant_url: Qdrant server URL
        ollama_url: Ollama server URL
        timeout: Connection timeout in seconds

    Returns:
        Dictionary with service names as keys and availability as values

    Example:
        >>> status = check_all_services()
        >>> if not status['qdrant']:
        ...     print("Qdrant is not available")
    """
    status = {}

    # Check Qdrant
    try:
        check_qdrant_availability(qdrant_url, timeout)
        status["qdrant"] = True
    except DependencyError:
        status["qdrant"] = False

    # Check Ollama
    try:
        check_ollama_availability(ollama_url, timeout)
        status["ollama"] = True
    except DependencyError:
        status["ollama"] = False

    # Check Azure OpenAI
    try:
        check_azure_openai_availability()
        status["azure_openai"] = True
    except DependencyError:
        status["azure_openai"] = False

    return status
