# GitHub Trending CLI

Browse GitHub's trending repositories from your terminal with daily star counts and README viewing.

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- View trending repositories with real-time daily star counts
- Support for daily, weekly, and monthly time ranges
- Interactive README viewing with syntax highlighting
- Language indicators and trending level indicators
- Clean terminal interface using Rich

## Installation

```bash
git clone https://github.com/your-username/github-trending-cli.git
cd github-trending-cli

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
# View today's trending repositories
github-trending

# View weekly trending
github-trending --range weekly

# View monthly trending
github-trending -r monthly
```

## Example Output

```
🚀 GitHub Trending Repositories - Daily 📅

 1. microsoft/TypeScript      🔷  ⭐95,234   🔥+1,234
    TypeScript is a superset of JavaScript that compiles to clean JavaScript
    
 2. facebook/react           ⚛️  ⭐201,456  🚀+567  
    A declarative, efficient, and flexible JavaScript library
    
 3. python/cpython           🐍  ⭐45,123   📈+89
    The Python programming language

Enter repo number (1-3), Enter for more, 'q' to quit: 
```

Trending indicators: 🔥 100+ daily stars, 🚀 50+ daily stars, 📈 10+ daily stars

## Architecture

- `scraper.py` - Fetches and parses GitHub's trending page
- `display.py` - Terminal UI using Rich library
- `cli.py` - Command-line interface and argument parsing

## Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `rich` - Terminal formatting
- `lxml` - XML/HTML processing

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests if available
5. Submit a pull request

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -e .` in project directory |
| Connection errors | Check internet connection |
| Empty results | GitHub may be rate limiting, wait a few minutes |

## License

MIT License - see [LICENSE](LICENSE) file for details.
