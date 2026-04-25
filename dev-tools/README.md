#TranslationTools

Automatically translate markdown files in directories.Two options are supported:

## 🔹 Option 1: translate_with_ollama.py (recommended ⭐)

Use native **Ollama models** for translation (completely offline).

### Features
- ✅ Runs completely locally and offline
- ✅ Privacy protection, data never leaves the machine
- ✅ High translation quality (supports large models)
- ❌ Requires Ollama service to run
- ❌ Slow translation (30-60 seconds/file)
- ❌ Requires large models (4-19GB)

### Quick start

```bash
# Start the Ollama service (in another terminal)
ollama serve

# Translate all .md files in the directory
python translate_with_ollama.py .github/prompts

#Specify to use a specific model
python translate_with_ollama.py .github/prompts --model deepseek-r1:32b

# Dry run mode (no changes saved)
python translate_with_ollama.py .github/prompts --dry-run
```

### Recommended model

The script automatically selects available models in order of priority:

| Model | Size | Translation Quality | Speed | Notes |
|------|------|--------|------|------|
| `deepseek-r1:32b` | 19 GB | ⭐⭐⭐ | Slow | Best quality (requires 50GB RAM) |
| `qwen2.5-coder:7b` | 4.7 GB | ⭐⭐ | Medium | ✅ **Recommended** (Use when memory is tight) |
| `llama3.2:latest` | 2.0 GB | ⭐⭐ | Fast | Fast translation |
| `qwen3:8b` | 5.2 GB | ⭐⭐ | Medium | Multi-language support |

**Current system using**: `qwen2.5-coder:7b` (automatically selected due to memory limitations)

---

## 🔹 Option 2: translate.py

Use **translatepy** (online translation service).

### Features
- ✅ Fast translation (a few seconds/file)
- ✅ No need for large models
- ✅ Easy to set up
- ❌ Internet connection required
- ❌ Privacy: Data passes through third-party services
- ❌ Translation quality depends on the backend service

### Quick Start

```bash
# Install dependencies
pip install -r dev-tools/requirements.txt

# Translation directory
python translate.py .github/prompts

# Dry running mode
python translate.py .github/prompts --dry-run
```

### Full options

```
positional arguments:
directory directory to be translated

optional arguments:
--lang LANG target language code (default: en)
--ext EXT file extension (default: .md)
--dry-run Dry run mode, no changes saved
-h, --help display help information
```

---

## Feature comparison

| Features | Ollama | translatepy |
|------|--------|-------------|
| Works offline | ✅ | ❌ |
| Translation quality | ⭐⭐⭐ | ⭐⭐ |
| speed | slow | fast |
| Privacy | ✅ | ❌ |
| Dependency configuration | Complex | Simple |
| Model size | 4-19GB | No need |

---

## Workflow

### Ollama Workflow

1. **Start Ollama service** - `ollama serve`
2. **Check Ollama Status** - Script automatically verifies
3. **Model Selection** - automatically selects the best available model
4. **File Scanning** - Find all files in the directory that need to be translated
5. **Chinese detection** - skip files that do not contain Chinese characters
6. **Chunked Translation** - Chunked processing of large files (2000 characters/chunk)
7. **Save results** - overwrite original file or preview in dry run mode

### translatepy workflow

1. **File Scanning** - Find all files in the directory that need to be translated
2. **Chinese detection** - skip files that do not contain Chinese characters
3. **Online Translation** - Call translatepy (using backends such as Google, Bing, etc.)
4. **Save results** - overwrite original file or preview in dry run mode

---

## Usage example

### Example 1: Using Ollama to translate the VedaAide project

```bash
cd /path/to/VedaAide.py

# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run the translation script
python dev-tools/translate_with_ollama.py .github/prompts
```

Output example:
```
Checking Ollama service... ✓
Using model: deepseek-r1:32b

Found 5 .md file(s) to translate

[1/5] cloud-native.md
Translating chunk 1/3... ✓
Translating chunk 2/3... ✓
Translating chunk 3/3... ✓
✓ Saved

[2/5] rag-development.md
Skipped (no Chinese content)

[3/5] evaluation-strategy.md
Translating chunk 1/2... ✓
Translating chunk 2/2... ✓
✓ Saved

Summary: 3/5 files processed successfully
```

### Example 2: Translate using translatepy (fast mode)

```bash
python dev-tools/translate.py .github/prompts
```

### Example 3: Translating specific file types

```bash
# Translate .cn.md file
python dev-tools/translate_with_ollama.py docs/planning --ext .cn.md

# Use a specific model
python dev-tools/translate_with_ollama.py docs/planning --ext .cn.md --model qwen2.5-coder:7b
```

### Example 4: Dry running mode preview (not saved)

```bash
python dev-tools/translate_with_ollama.py .github/prompts --dry-run
```

---

## Troubleshooting

### Ollama related

#### Problem: Ollama service connection failed

```bash
# Start Ollama service
ollama serve

# Verify that Ollama is running in another terminal
curl http://localhost:11434/api/tags
```

#### Problem: Model is not available

```bash
# View installed models
ollama list

# Pull recommended models
ollama pull deepseek-r1:32b
ollama pull qwen2.5-coder:7b
```

#### Problem: The translation effect is not ideal

Try using a better performing model:
```bash
python dev-tools/translate_with_ollama.py <dir> --model deepseek-r1:32b
```

#### Problem: The file is too large and the translation times out

The program is automatically divided into blocks (2000 characters/block).If it still times out, manually split the file and translate it again.

### translatepy related

#### Problem: Network connection failed

```bash
# Check network connection
ping google.com

# Try to run again (the network may be unstable)
python dev-tools/translate.py <dir>
```

#### Question: "No service has returned a valid result"

translatepy All translation backends (Google, Bing, etc.) are unavailable, usually caused by the following reasons:
- Internet connection issues
- Throttled by the translation service
- Translation service is temporarily unavailable

**Solution**: Switch to Ollama solution

---

## Notes

- ⚠️ After translation, the original file will be **overwritten**. It is recommended to back up important files first.
- ⚠️ Use `--dry-run` to preview the effect before running it officially
- ⚠️ Ollama translation is slow (30-60 seconds/file), please wait patiently
- ⚠️ translatepy requires an internet connection
- ⚠️ Translation quality depends on the selected plan

---

## Developer Notes

### File list

```
dev-tools/
├── translate_with_ollama.py # Ollama translation tool (recommended)
├── translate.py # translatepy translation tool (fast)
├── requirements.txt # Dependency configuration (for translate.py)
└── README.md # This document
```

### Configuration parameters

**Ollama Tools**:
- Temperature: 0.3 to improve translation consistency
- API timeout: 120 seconds/request
- Chunk size: 2000 characters/chunk

**translatepy tool**:
- Automatic retry: built-in retry mechanism
- File encoding: UTF-8
- Supported target languages: all ISO 639-1 codes

### Suggestions for choosing two tools

**Use Ollama if**:
- You want the best translation quality
- You care about data privacy
- You don't care about waiting time
- You have enough disk space (4-19GB)

**Use translatepy if**:
- You want to translate quickly
- Stable network connection
- Translation quality requirements are not high
- You want the simplest setup
