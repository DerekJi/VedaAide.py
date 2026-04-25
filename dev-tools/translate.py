#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch translate markdown files in a directory using translatepy.

Usage:
    python translate.py <directory> [--lang LANG] [--output-dir OUTPUT_DIR]

Example:
    python translate.py .github/prompts --lang en
    python translate.py docs/planning --ext .cn.md --output-dir .temp
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    from translatepy import Translator
except ImportError:
    print("Error: translatepy not installed")
    print("Install it with: pip install translatepy")
    sys.exit(1)


def translate_text(text: str, target_lang: str = "en", verbose: bool = False) -> str:
    """
    Translate text using translatepy.

    Args:
        text: Text to translate
        target_lang: Target language code (default: English)
        verbose: Print debug information

    Returns:
        Translated text
    """
    if not text.strip():
        return text

    try:
        translator = Translator()
        result = translator.translate(text, target_lang)
        # translatepy returns a TranslationResult object, convert to string
        translated = str(result) if result else text

        if verbose:
            print(
                f"    DEBUG: Original length: {len(text)}, Translated length: {len(translated)}",
                file=sys.stderr,
            )

        return translated
    except Exception as e:
        print(f"    Warning: Translation failed: {e}")
        if verbose:
            import traceback

            print(f"    DEBUG: {traceback.format_exc()}", file=sys.stderr)
        return text  # Return original text on failure


def translate_file(  # noqa: C901
    file_path: Path,
    target_lang: str = "en",
    dry_run: bool = False,
    output_dir: Optional[Path] = None,
    verbose: bool = False,
) -> bool:
    """
    Translate a single file.

    Args:
        file_path: Path to the file to translate
        target_lang: Target language code (default: English)
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

        # Translate with better error handling
        print("  Translating...", flush=True)
        try:
            translated_content = translate_text(content, target_lang, verbose)
        except Exception as e:
            print(f"  ✗ Translation error: {e}")
            if verbose:
                import traceback

                print(f"    DEBUG: {traceback.format_exc()}", file=sys.stderr)
            # Continue with original text
            translated_content = content

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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch translate markdown files using translatepy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate all .md files in .github/prompts
  python translate.py .github/prompts

  # Translate .cn.md files
  python translate.py docs/planning --ext .cn.md

  # Output to .temp directory instead of overwriting
  python translate.py docs/planning --ext .cn.md --output-dir .temp

  # Dry run (don't save changes)
  python translate.py .github/prompts --dry-run

  # Debug mode (verbose output)
  python translate.py .github/prompts --verbose
        """,
    )

    parser.add_argument("directory", help="Directory containing files to translate")
    parser.add_argument("--lang", default="en", help="Target language code (default: en)")
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
