#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch translate markdown files in a directory using local Ollama models.

Usage:
    python translate_with_ollama.py <directory> [--model MODEL] [--lang LANG]
    python translate_with_ollama.py <directory> [--output-dir OUTPUT_DIR]

Example:
    python translate_with_ollama.py .github/prompts --model deepseek-r1:32b
    python translate_with_ollama.py .github/prompts --output-dir .temp
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import requests

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Available models optimized for translation
RECOMMENDED_MODELS = [
    "deepseek-r1:32b",  # Best reasoning and translation quality
    "qwen2.5-coder:7b",  # Good for code and technical content
    "llama3.2:latest",  # General purpose
    "qwen3:8b",  # Good multilingual support
]


def check_ollama_health() -> bool:
    """Check if Ollama service is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_available_models() -> list:
    """Get list of available Ollama models."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
    except Exception as e:
        print(f"Warning: Could not fetch model list: {e}")
    return []


def select_model(preferred_model: Optional[str] = None) -> str:
    """Select the best available model for translation."""
    available = get_available_models()

    if not available:
        print("Error: No Ollama models available. Please run 'ollama pull <model>'")
        sys.exit(1)

    # If preferred model specified and available
    if preferred_model and preferred_model in available:
        return preferred_model

    # Try recommended models in order
    for model in RECOMMENDED_MODELS:
        if model in available:
            print(f"Using model: {model}")
            return model

    # Fallback to first available model
    selected = available[0]
    print(f"Using model: {selected}")
    return selected


def translate_text(  # noqa: C901
    text: str, model: str, target_lang: str = "en", chunk_size: int = 2000, verbose: bool = False
) -> str:
    """
    Translate text using Ollama.

    Args:
        text: Text to translate
        model: Ollama model name
        target_lang: Target language (default: English)
        chunk_size: Max characters per request (Ollama has limits)
        verbose: Print debug information

    Returns:
        Translated text
    """
    if not text.strip():
        return text

    # For very long texts, split into chunks
    chunks = []
    current_chunk = ""

    for line in text.split("\n"):
        if len(current_chunk) + len(line) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    if verbose:
        print(f"  DEBUG: Splitting into {len(chunks)} chunk(s)")

    # Translate each chunk
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"  Translating chunk {i + 1}/{len(chunks)}...", end=" ", flush=True)

        prompt = f"""Translate the following Chinese text to English.
Keep the formatting, markdown syntax, code blocks, and special characters exactly as is.
Only translate the actual content, not the code or technical keywords that should remain in English.

Text to translate:
{chunk}

English translation:"""

        try:
            if verbose:
                print(f"\n    DEBUG: Sending request to Ollama (model: {model})", file=sys.stderr)

            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,  # Lower temperature for more consistent translations
                },
                timeout=180,  # Increased timeout
            )

            if verbose:
                print(f"    DEBUG: Response status: {response.status_code}", file=sys.stderr)

            if response.status_code == 200:
                result = response.json()
                translated_text = result.get("response", "").strip()

                if verbose:
                    print(f"    DEBUG: Response length: {len(translated_text)}", file=sys.stderr)

                # Clean up the response
                if translated_text.startswith("English translation:"):
                    translated_text = translated_text[len("English translation:") :].strip()

                if translated_text:
                    translated_chunks.append(translated_text)
                    print("✓")
                else:
                    print("✗ (empty response)")
                    translated_chunks.append(chunk)  # Keep original
            else:
                print(f"✗ (HTTP {response.status_code})")
                if verbose:
                    print(f"    DEBUG: Response: {response.text[:200]}", file=sys.stderr)
                translated_chunks.append(chunk)  # Keep original on error

        except requests.exceptions.Timeout:
            print("✗ (timeout)")
            translated_chunks.append(chunk)
        except Exception as e:
            print(f"✗ ({str(e)[:50]})")
            if verbose:
                print(f"    DEBUG: Error: {e}", file=sys.stderr)
            translated_chunks.append(chunk)

    result = "\n".join(translated_chunks)
    if verbose:
        print(f"  DEBUG: Total output length: {len(result)}", file=sys.stderr)
    return result


def translate_file(  # noqa: C901
    file_path: Path,
    model: str,
    target_lang: str = "en",
    dry_run: bool = False,
    output_dir: Optional[Path] = None,
    verbose: bool = False,
) -> bool:
    """
    Translate a single file.

    Args:
        file_path: Path to the file to translate
        model: Ollama model name
        target_lang: Target language (default: English)
        dry_run: If True, don't save changes
        output_dir: If specified, save to this directory instead of overwriting
        verbose: Print debug information

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if verbose:
            print(f"  DEBUG: File size: {len(content)} bytes", file=sys.stderr)

        # Check if file contains Chinese
        has_chinese = any("\u4e00" <= char <= "\u9fff" for char in content)

        if verbose:
            print(f"  DEBUG: Has Chinese: {has_chinese}", file=sys.stderr)

        if not has_chinese:
            print("  Skipped (no Chinese content)")
            return True

        # Translate
        print("  Translating...", flush=True)
        translated_content = translate_text(content, model, target_lang, verbose=verbose)

        # Verify translation happened
        if translated_content == content:
            print("  ⚠️  Warning: No changes detected (translation may have failed)")

        # Determine output path
        if output_dir:
            output_dir = Path(output_dir).resolve()  # Convert to absolute path
            output_dir.mkdir(parents=True, exist_ok=True)
            # Replace .cn.md with .en.md, or append .en.md
            if file_path.name.endswith(".cn.md"):
                output_name = file_path.name.replace(".cn.md", ".en.md")
            elif file_path.name.endswith(".md"):
                output_name = file_path.name.replace(".md", ".en.md")
            else:
                output_name = file_path.name + ".en"
            output_path = output_dir / output_name
        else:
            output_path = file_path

        # Save
        if not dry_run:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(translated_content)
            if output_dir:
                try:
                    rel_path = output_path.relative_to(Path.cwd())
                    print(f"  ✓ Saved to {rel_path}")
                except ValueError:
                    # If not in current working directory, use absolute path
                    print(f"  ✓ Saved to {output_path}")
            else:
                print("  ✓ Saved")
        else:
            print("  [DRY RUN] Would save to", output_path)

        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        if verbose:
            import traceback

            print(f"    DEBUG: {traceback.format_exc()}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Batch translate markdown files using local Ollama models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate all .md files in .github/prompts
  python translate_with_ollama.py .github/prompts

  # Use specific model
  python translate_with_ollama.py .github/prompts --model deepseek-r1:32b

  # Output to .temp directory instead of overwriting
  python translate_with_ollama.py .github/prompts --output-dir .temp

  # Dry run (don't save changes)
  python translate_with_ollama.py .github/prompts --dry-run

  # Debug mode (verbose output)
  python translate_with_ollama.py .github/prompts --verbose
        """,
    )

    parser.add_argument("directory", help="Directory containing files to translate")
    parser.add_argument(
        "--model",
        default=None,
        help=f"Ollama model to use (default: auto-select from {RECOMMENDED_MODELS[0]})",
    )
    parser.add_argument("--lang", default="en", help="Target language (default: en)")
    parser.add_argument("--ext", default=".md", help="File extension to translate (default: .md)")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for translated files (default: overwrite originals)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't save changes, just show what would be translated",
    )
    parser.add_argument("--verbose", action="store_true", help="Print debug information")

    args = parser.parse_args()

    # Check if directory exists
    target_dir = Path(args.directory)
    if not target_dir.exists():
        print(f"Error: Directory '{args.directory}' does not exist")
        sys.exit(1)

    # Check Ollama health
    print("Checking Ollama service...", end=" ", flush=True)
    if not check_ollama_health():
        print("✗")
        print("Error: Ollama service is not running")
        print("Please start Ollama with: ollama serve")
        sys.exit(1)
    print("✓")

    # Select model
    model = select_model(args.model)
    print()

    # Find files to translate
    files_to_translate = list(target_dir.rglob(f"*{args.ext}"))

    if not files_to_translate:
        print(f"No {args.ext} files found in {args.directory}")
        sys.exit(0)

    print(f"Found {len(files_to_translate)} {args.ext} file(s) to translate")
    if args.output_dir:
        print(f"Output directory: {args.output_dir}")
    print()

    # Translate files
    success_count = 0
    for i, file_path in enumerate(files_to_translate, 1):
        print(f"[{i}/{len(files_to_translate)}] {file_path.relative_to(target_dir)}")

        if translate_file(
            file_path,
            model,
            args.lang,
            args.dry_run,
            Path(args.output_dir) if args.output_dir else None,
            args.verbose,
        ):
            success_count += 1

    # Summary
    print()
    print(f"Summary: {success_count}/{len(files_to_translate)} files processed successfully")

    if args.dry_run:
        print("(Dry run - no files were modified)")


if __name__ == "__main__":
    main()
