# GitHub Trending CLI

We like browsing GitHub's trending page, so we made a CLI version.

![GitHub Trending CLI Screenshot](github-trending-screenshot.png)

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What it does

- Shows trending repositories with daily star counts
- Supports daily, weekly, and monthly views
- Click on any repo to read its README
- Simple terminal interface

## Installation

```bash
git clone https://github.com/your-username/github-trending-cli.git
cd github-trending-cli

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
github-trending                 # today's trending
github-trending --range weekly  # this week
github-trending -r monthly      # this month
```

Enter a repo number to read its README, or press Enter to see more repos.

## How it works

Scrapes GitHub's trending page and displays it in your terminal. That's it.

- `scraper.py` - Gets the trending page HTML and parses it
- `display.py` - Shows the data nicely in terminal
- `cli.py` - Handles the command line stuff

Uses `requests`, `beautifulsoup4`, `rich`, and `lxml`.

## Contributing

Fork it, make changes, send a PR.

## License

MIT
