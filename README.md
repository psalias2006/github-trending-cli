# Git Trending

We like browsing GitHub's trending page, so we made a Git extension for it.

Run `git trending` to browse trending repositories right from your terminal (You can export data too 😉)

![Git Trending CLI Screenshot](github-trending-screenshot.png)

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What it does

- Browse GitHub trending repositories as a **Git extension**
- Shows trending repositories with daily star counts
- Supports daily, weekly, and monthly views
- Click on any repo to read its README
- Export to CSV or JSON Lines format
- Simple terminal interface
- Works with `git trending` command!

## Installation

### pipx (Recommended - Global Install)
```bash
# Install pipx if you don't have it
pip install --user pipx
pipx ensurepath

# Install git-trending globally
pipx install git+https://github.com/psalias2006/github-trending-cli.git

# Now you can use it as a git extension!
git trending
```

### Local Development
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
docker build -t git-trending .
```

## Usage

### As Git Extension (Recommended)
```bash
git trending                 # Show today's trending repos
git trending -r weekly       # Show this week's trending repos
git trending -r monthly      # Show this month's trending repos
```

### Docker
```bash
docker run -it --rm git-trending
docker run -it --rm git-trending -r weekly
```

### Export Mode
```bash
# As Git extension
git trending -e              # CSV export
git trending -e -f json      # JSON Lines export
git trending -e -r weekly    # Weekly data

# Docker (requires volume mount)
docker run --rm -v "$(pwd)/exported:/app/exported" git-trending -e
docker run --rm -v "$(pwd)/exported:/app/exported" git-trending -e -f json
```

## How Git Extensions Work

When you install `git-trending`, Git automatically recognizes it as an extension. This means:
- `git trending` → runs `git-trending` 
- `git trending -r weekly` → runs `git-trending -r weekly`
- Works from any directory, just like other git commands!

## Export Format

Files saved to `exported/` with timestamps: `github_trending_{range}_{datetime}.{csv|jsonl}`

**CSV**: Standard format with headers  
**JSON Lines**: One JSON object per line, ideal for data processing

**Columns**: name, url, description, language, stars, stars_period, range, export_datetime

## Contributing

Fork it, make changes, send a PR.

## License

MIT