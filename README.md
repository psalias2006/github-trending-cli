# GitHub Trending CLI

We like browsing GitHub's trending page, so we made a CLI version.

![GitHub Trending CLI Screenshot](github-trending-screenshot.png)

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What it does

- Shows trending repositories with daily star counts
- Supports daily, weekly, and monthly views
- Click on any repo to read its README
- Export to CSV or JSON Lines format
- Simple terminal interface

## Installation

### Local
```bash
git clone https://github.com/psalias2006/github-trending-cli.git
cd github-trending-cli
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt && pip install -e .
```

### Docker
```bash
git clone https://github.com/psalias2006/github-trending-cli.git
cd github-trending-cli
docker build -t github-trending-cli .
```

## Usage

### Interactive Mode
```bash
# Local
github-trending                 # today
github-trending -r weekly       # this week
github-trending -r monthly      # this month

# Docker
docker run -it --rm github-trending-cli
docker run -it --rm github-trending-cli -r weekly
```

### Export Mode
```bash
# Local
github-trending -e              # CSV export
github-trending -e -f json      # JSON Lines export
github-trending -e -r weekly    # Weekly data

# Docker (requires volume mount)
docker run --rm -v "$(pwd)/exported:/app/exported" github-trending-cli -e
docker run --rm -v "$(pwd)/exported:/app/exported" github-trending-cli -e -f json
```

## Export Format

Files saved to `exported/` with timestamps: `github_trending_{range}_{datetime}.{csv|jsonl}`

**CSV**: Standard format with headers  
**JSON Lines**: One JSON object per line, ideal for data processing

**Columns**: name, url, description, language, stars, stars_period, range, export_datetime

## Contributing

Fork it, make changes, send a PR.

## License

MIT